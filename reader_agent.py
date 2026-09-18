"""Reader agent: extracts concepts from chapter text and produces concepts.json

Pair A module (Joey & Simran). Takes raw chapter/syllabus text and outputs
structured concepts in the format that Pair B (Builder) expects.
"""

import json
import sys
import os

# Import the shared LLM client
try:
    from llm_client import call_llm
except ImportError:
    # Fallback if llm_client doesn't exist yet - copy from main branch
    print("WARNING: llm_client.py not found. Copy it from main branch.", file=sys.stderr)
    sys.exit(1)


def extract_topics(chapter_text: str) -> dict:
    """Extract key concepts from chapter text and return concepts.json format.

    Args:
        chapter_text: Raw text from a textbook chapter or syllabus

    Returns:
        Dictionary matching contracts/concepts.json schema:
        {
          "concepts": [
            {
              "id": "c1",
              "name": "Concept Name",
              "summary": "Brief explanation in 1-2 sentences",
              "source_text": "Relevant excerpt from the original chapter"
            },
            ...
          ]
        }
    """

    prompt = f"""You are a study materials extraction agent. Read the chapter text below and extract the key concepts that a student needs to learn.

CHAPTER TEXT:
{chapter_text}

TASK:
Extract 3-8 key concepts from this text. For each concept:
1. Give it a short, clear name (2-5 words)
2. Write a 1-2 sentence summary explaining what it is
3. Include the most relevant excerpt from the source text (1-3 sentences)

RULES:
- Concepts should be distinct topics, not trivial facts
- Summaries should be clear enough that someone could study from them
- Source text excerpts should be actual quotes from the input
- Number the concepts sequentially starting from c1

Return ONLY a JSON object (no markdown fences, no extra text) in this exact format:

{{
  "concepts": [
    {{
      "id": "c1",
      "name": "First Concept Name",
      "summary": "Clear explanation of what this concept is and why it matters.",
      "source_text": "Direct quote from the chapter that introduces or explains this concept."
    }},
    {{
      "id": "c2",
      "name": "Second Concept Name",
      "summary": "Clear explanation of the second concept.",
      "source_text": "Another relevant quote from the source material."
    }}
  ]
}}

Generate the JSON now:"""

    # Call the LLM
    raw_response = call_llm(prompt)

    # Parse the JSON response
    try:
        result = _extract_json(raw_response)
    except Exception as e:
        raise ValueError(f"Failed to parse LLM response as JSON: {e}\nRaw response: {raw_response[:500]}")

    # Validate the output matches our contract
    errors = _validate_concepts(result)
    if errors:
        raise ValueError(
            f"LLM output failed validation:\n  - " + "\n  - ".join(errors) +
            f"\n\nRaw output: {json.dumps(result, indent=2)[:500]}"
        )

    return result


def _extract_json(raw: str) -> dict:
    """Parse the LLM response into a dict, tolerating markdown code fences."""
    text = raw.strip()

    # Remove markdown code fences if present
    if text.startswith("```"):
        lines = text.split("\n")
        text = "\n".join(lines[1:])  # Skip first line (```json or ```)
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3]

    text = text.strip()

    # Find the JSON object
    if not text.startswith("{"):
        start = text.find("{")
        end = text.rfind("}")
        if start == -1 or end == -1:
            raise ValueError(f"No JSON object found in response: {raw[:300]}")
        text = text[start:end + 1]

    return json.loads(text)


def _validate_concepts(output: dict) -> list[str]:
    """Validate that output matches concepts.json schema. Returns list of error messages."""
    errors = []

    if not isinstance(output, dict):
        return [f"Output is {type(output).__name__}, expected dict"]

    if "concepts" not in output:
        return ["Missing 'concepts' key"]

    concepts = output["concepts"]
    if not isinstance(concepts, list):
        errors.append(f"'concepts' must be a list, got {type(concepts).__name__}")
        return errors

    if len(concepts) == 0:
        errors.append("'concepts' list is empty - should have 3-8 concepts")

    seen_ids = set()
    for i, concept in enumerate(concepts):
        if not isinstance(concept, dict):
            errors.append(f"concepts[{i}] is not a dict")
            continue

        # Check required fields
        for field in ["id", "name", "summary", "source_text"]:
            if field not in concept:
                errors.append(f"concepts[{i}] missing required field '{field}'")
            elif not isinstance(concept[field], str):
                errors.append(f"concepts[{i}].{field} must be a string")
            elif not concept[field].strip():
                errors.append(f"concepts[{i}].{field} is empty")

        # Check ID format and uniqueness
        concept_id = concept.get("id", "")
        if concept_id:
            if not concept_id.startswith("c"):
                errors.append(f"concepts[{i}].id should start with 'c' (got '{concept_id}')")
            if concept_id in seen_ids:
                errors.append(f"concepts[{i}].id '{concept_id}' is duplicate")
            seen_ids.add(concept_id)

    return errors


# Test the agent with sample text
if __name__ == "__main__":
    # Sample chapter text for testing
    sample_chapter = """
    Introduction to Neural Networks

    A neural network is a computational model inspired by the way biological neural
    networks in the brain process information. Neural networks consist of interconnected
    nodes (neurons) organized in layers. The basic architecture includes an input layer,
    one or more hidden layers, and an output layer.

    Activation functions are mathematical operations applied to the output of each neuron.
    Common activation functions include sigmoid, tanh, and ReLU (Rectified Linear Unit).
    The choice of activation function affects how the network learns and what kinds of
    patterns it can recognize.

    Backpropagation is the algorithm used to train neural networks. It works by calculating
    the gradient of the loss function with respect to each weight in the network, then
    adjusting the weights to minimize the loss. This process is repeated over many
    iterations until the network's performance converges.

    Overfitting occurs when a neural network learns the training data too well, including
    its noise and peculiarities, rather than learning the underlying patterns. This results
    in poor performance on new, unseen data. Regularization techniques like dropout and
    L2 regularization help prevent overfitting.
    """

    print("Testing reader agent with sample chapter...\n")

    try:
        result = extract_topics(sample_chapter)
        print("SUCCESS! Generated concepts.json:")
        print(json.dumps(result, indent=2))

        # Save to data/ directory for testing
        os.makedirs("data", exist_ok=True)
        with open("data/concepts.json", "w") as f:
            json.dump(result, f, indent=2)
        print("\nSaved to data/concepts.json")

    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)
