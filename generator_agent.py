"""Generator agent: turns concepts.json into materials.json via a single LLM call.

Pair B module. Consumes the concepts.json contract, produces the materials.json
contract. Modes supported so far: "standard".
"""

import json

from llm_client import call_llm

SUPPORTED_MODES = ("standard",)

# Shared across every mode's prompt so the JSON contract is stated once.
_SCHEMA_BLOCK = """Return ONLY a single JSON object, no prose and no markdown fences, shaped exactly like this:

{
  "mode": "<MODE>",
  "concept_map": {
    "nodes": [{"id": "c1", "name": "..."}],
    "edges": [{"from": "c1", "to": "c2", "relation": "leads to"}]
  },
  "review_sheet": [{"concept_id": "c1", "content": "..."}],
  "quiz": [
    {
      "id": "q1", "concept_id": "c1", "question": "...",
      "options": ["A. ...", "B. ...", "C. ...", "D. ..."],
      "answer": "B"
    }
  ]
}

Hard rules (downstream grading code depends on these):
- "answer" is a SINGLE UPPERCASE LETTER ("A", "B", "C" or "D") and must match the
  letter prefix of one of that question's own options. Never put the answer text there.
- Every question has exactly 4 options, prefixed "A. ", "B. ", "C. ", "D. " in that order.
- Quiz ids are "q1", "q2", ... in order.
- "concept_map.nodes" contains exactly one node per input concept, using that concept's
  own id and name. Edge "from"/"to" values must be ids that exist in "nodes".
- Every "concept_id" must be one of the input concept ids.
- Spread the correct answers across the letters; do not make them all the same letter."""


def _format_concepts(concepts_json: dict) -> str:
    """Render the input concepts as a readable block for inclusion in a prompt."""
    lines = []
    for concept in concepts_json.get("concepts", []):
        lines.append(
            f"- id: {concept['id']}\n"
            f"  name: {concept['name']}\n"
            f"  summary: {concept['summary']}\n"
            f"  source_text: {concept['source_text']}"
        )
    return "\n".join(lines)


def build_standard_prompt(concepts_json: dict) -> str:
    """Build the LLM prompt for standard mode: normal paragraphs, one quiz at the end."""
    return f"""You are a study-materials generator. Build a concept map, a review sheet and a
quiz from the concepts below.

CONCEPTS
{_format_concepts(concepts_json)}

STANDARD MODE FORMATTING
- review_sheet: one entry per concept, written as normal flowing paragraphs
  (roughly 100-150 words). No bullet points, no headings, no markdown emphasis.
- quiz: one combined quiz at the end covering all concepts, one question per
  concept, in the same order as the concepts above.
- concept_map: link concepts where the source material actually supports a
  relationship; use an empty "edges" list if none do.

{_SCHEMA_BLOCK.replace("<MODE>", "standard")}"""


# mode -> prompt builder. Add "adhd" / "dyslexia" builders here as they land.
_PROMPT_BUILDERS = {
    "standard": build_standard_prompt,
}


def _extract_json(raw: str) -> dict:
    """Parse the LLM response into a dict, tolerating markdown code fences around it."""
    text = raw.strip()
    if text.startswith("```"):
        # Drop the opening fence (with optional language tag) and the closing fence.
        text = text.split("\n", 1)[1] if "\n" in text else ""
        if text.rstrip().endswith("```"):
            text = text.rstrip()[: -len("```")]
    text = text.strip()
    if not text.startswith("{"):
        # Fall back to the outermost braces in case the model added stray prose.
        start, end = text.find("{"), text.rfind("}")
        if start == -1 or end == -1:
            raise ValueError(f"LLM response contained no JSON object: {raw[:300]!r}")
        text = text[start : end + 1]
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"LLM response was not valid JSON: {exc}\nRaw: {raw[:300]!r}") from exc


def _validation_errors(output: dict, concepts_json: dict | None = None) -> list[str]:
    """Collect every way `output` violates OUTPUT SCHEMA, as human-readable strings."""
    errors = []

    if not isinstance(output, dict):
        return [f"output is {type(output).__name__}, expected dict"]

    if output.get("mode") not in SUPPORTED_MODES:
        errors.append(f"mode {output.get('mode')!r} is not one of {SUPPORTED_MODES}")

    known_ids = None
    if concepts_json is not None:
        known_ids = {c["id"] for c in concepts_json.get("concepts", [])}

    # --- concept_map ---
    concept_map = output.get("concept_map")
    node_ids = set()
    if not isinstance(concept_map, dict):
        errors.append("concept_map is missing or not an object")
    else:
        nodes = concept_map.get("nodes")
        if not isinstance(nodes, list) or not nodes:
            errors.append("concept_map.nodes is missing, not a list, or empty")
        else:
            for i, node in enumerate(nodes):
                if not isinstance(node, dict) or not isinstance(node.get("id"), str) \
                        or not isinstance(node.get("name"), str):
                    errors.append(f"concept_map.nodes[{i}] needs string 'id' and 'name'")
                    continue
                node_ids.add(node["id"])
                if known_ids is not None and node["id"] not in known_ids:
                    errors.append(f"concept_map.nodes[{i}].id {node['id']!r} is not an input concept")

        edges = concept_map.get("edges")
        if not isinstance(edges, list):
            errors.append("concept_map.edges is missing or not a list")
        else:
            for i, edge in enumerate(edges):
                if not isinstance(edge, dict) or not all(
                    isinstance(edge.get(k), str) for k in ("from", "to", "relation")
                ):
                    errors.append(f"concept_map.edges[{i}] needs string 'from', 'to' and 'relation'")
                    continue
                for end in ("from", "to"):
                    if edge[end] not in node_ids:
                        errors.append(
                            f"concept_map.edges[{i}].{end} {edge[end]!r} is not a node id"
                        )

    # --- review_sheet ---
    review_sheet = output.get("review_sheet")
    if not isinstance(review_sheet, list) or not review_sheet:
        errors.append("review_sheet is missing, not a list, or empty")
    else:
        for i, entry in enumerate(review_sheet):
            if not isinstance(entry, dict) or not isinstance(entry.get("concept_id"), str) \
                    or not isinstance(entry.get("content"), str) or not entry["content"].strip():
                errors.append(f"review_sheet[{i}] needs string 'concept_id' and non-empty 'content'")
                continue
            if known_ids is not None and entry["concept_id"] not in known_ids:
                errors.append(
                    f"review_sheet[{i}].concept_id {entry['concept_id']!r} is not an input concept"
                )

    # --- quiz ---
    quiz = output.get("quiz")
    if not isinstance(quiz, list) or not quiz:
        errors.append("quiz is missing, not a list, or empty")
    else:
        for i, question in enumerate(quiz):
            if not isinstance(question, dict):
                errors.append(f"quiz[{i}] is not an object")
                continue
            for key in ("id", "concept_id", "question", "answer"):
                if not isinstance(question.get(key), str) or not question[key].strip():
                    errors.append(f"quiz[{i}].{key} is missing or not a non-empty string")
            if known_ids is not None and question.get("concept_id") not in known_ids:
                errors.append(
                    f"quiz[{i}].concept_id {question.get('concept_id')!r} is not an input concept"
                )

            options = question.get("options")
            if not isinstance(options, list) or len(options) != 4 \
                    or not all(isinstance(o, str) and o.strip() for o in options):
                errors.append(f"quiz[{i}].options must be 4 non-empty strings")
                continue

            # "answer" must be a single letter that prefixes one of this question's options.
            letters = [o.strip()[0] for o in options if o.strip()[:1].isalpha()]
            answer = question.get("answer")
            if not isinstance(answer, str) or len(answer) != 1 or not answer.isalpha() \
                    or not answer.isupper():
                errors.append(f"quiz[{i}].answer {answer!r} must be a single uppercase letter")
            elif answer not in letters:
                errors.append(
                    f"quiz[{i}].answer {answer!r} does not match any option letter {letters}"
                )

    return errors


def validate_materials(output: dict) -> bool:
    """Return True if `output` matches OUTPUT SCHEMA, including single-letter quiz answers."""
    return not _validation_errors(output)


def generate_materials(concepts_json: dict, mode: str) -> dict:
    """Generate a validated materials.json-shaped dict for the given concepts and mode."""
    builder = _PROMPT_BUILDERS.get(mode)
    if builder is None:
        raise ValueError(
            f"Unsupported mode {mode!r}; supported modes are {sorted(_PROMPT_BUILDERS)}"
        )

    output = _extract_json(call_llm(builder(concepts_json)))

    errors = _validation_errors(output, concepts_json)
    if errors:
        raise ValueError(
            "LLM output failed validation:\n  - " + "\n  - ".join(errors)
        )
    return output


if __name__ == "__main__":
    test_concepts = {
        "concepts": [
            {
                "id": "c1",
                "name": "Sample Concept One",
                "summary": "Fake summary for testing.",
                "source_text": "This is fake source text for concept one.",
            },
            {
                "id": "c2",
                "name": "Sample Concept Two",
                "summary": "Fake summary for testing.",
                "source_text": "This is fake source text for concept two.",
            },
        ]
    }
    print(json.dumps(generate_materials(test_concepts, "standard"), indent=2))
