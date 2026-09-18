"""Memory/grading agent: grades a quiz, persists per-student history, and
builds a re-quiz containing only previously-missed concepts.

Pair C module. Consumes the materials.json "quiz" contract plus submitted
answers, produces the student_memory.json contract (written to
data/student_memory.json, gitignored, regenerated at runtime).
"""
import json
import os
from datetime import datetime, timezone

STORE_PATH = os.path.join(os.path.dirname(__file__), "data", "student_memory.json")


def grade_quiz(quiz: list, submitted_answers: dict) -> dict:
    """Grade a list of quiz questions against submitted answers.

    quiz: list of {"id", "concept_id", "question", "options", "answer"} (materials.json["quiz"])
    submitted_answers: {"q1": "B", "q2": "A", ...}

    Returns {"results": [...], "score": int, "total": int}, where each result is
    {"quiz_id", "concept_id", "submitted", "correct_answer", "is_correct"}.
    """
    results = []
    score = 0
    for question in quiz:
        qid = question["id"]
        submitted = submitted_answers.get(qid)
        correct_answer = question["answer"]
        is_correct = submitted == correct_answer
        if is_correct:
            score += 1
        results.append({
            "quiz_id": qid,
            "concept_id": question["concept_id"],
            "submitted": submitted,
            "correct_answer": correct_answer,
            "is_correct": is_correct,
        })
    return {"results": results, "score": score, "total": len(quiz)}


def _load_store() -> dict:
    if not os.path.exists(STORE_PATH):
        return {}
    with open(STORE_PATH, "r") as f:
        return json.load(f)


def _write_store(store: dict) -> None:
    os.makedirs(os.path.dirname(STORE_PATH), exist_ok=True)
    with open(STORE_PATH, "w") as f:
        json.dump(store, f, indent=2)


def save_results(student_id: str, graded_results: dict) -> None:
    """Append graded_results["results"] (from grade_quiz) to the student's
    persisted history, timestamping each entry."""
    store = _load_store()
    student = store.setdefault(student_id, {"student_id": student_id, "history": []})
    now = datetime.now(timezone.utc).isoformat()
    for result in graded_results["results"]:
        student["history"].append({**result, "timestamp": now})
    _write_store(store)


def get_missed_concepts(student_id: str) -> list:
    """Return concept_ids the student got wrong on their most recent attempt
    at that concept (later history entries override earlier ones)."""
    store = _load_store()
    student = store.get(student_id)
    if not student:
        return []

    latest_by_concept = {}
    for entry in student["history"]:
        concept_id = entry["concept_id"]
        if concept_id not in latest_by_concept or entry["timestamp"] >= latest_by_concept[concept_id]["timestamp"]:
            latest_by_concept[concept_id] = entry

    return [cid for cid, entry in latest_by_concept.items() if not entry["is_correct"]]


def build_requiz(missed_concept_ids: list, full_quiz) -> dict:
    """Filter a quiz down to only the questions covering missed_concept_ids.

    full_quiz: either materials.json["quiz"] (a list) or the full materials
    dict (containing a "quiz" key) — both are accepted.
    """
    quiz = full_quiz["quiz"] if isinstance(full_quiz, dict) else full_quiz
    missed = set(missed_concept_ids)
    return {"quiz": [q for q in quiz if q["concept_id"] in missed]}


if __name__ == "__main__":
    # Self-test against the fake contract data.
    with open(os.path.join(os.path.dirname(__file__), "contracts", "materials.json")) as f:
        materials = json.load(f)

    quiz = materials["quiz"]
    submitted = {"q1": "B"}  # fake wrong answer (correct is "A")

    graded = grade_quiz(quiz, submitted)
    print("graded:", graded)

    save_results("s1", graded)
    print("missed concepts:", get_missed_concepts("s1"))

    requiz = build_requiz(get_missed_concepts("s1"), materials)
    print("requiz:", requiz)
