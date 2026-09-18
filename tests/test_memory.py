"""Standalone tests for memory.py (Pair C). Run with: python tests/test_memory.py

Uses a temporary store path so it never touches the real data/student_memory.json.
"""
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
import memory  # noqa: E402

QUIZ = [
    {"id": "q1", "concept_id": "c1", "question": "Q1?", "options": ["A. x", "B. y"], "answer": "A"},
    {"id": "q2", "concept_id": "c2", "question": "Q2?", "options": ["A. x", "B. y"], "answer": "B"},
]


def with_temp_store(fn):
    with tempfile.TemporaryDirectory() as tmp:
        original = memory.STORE_PATH
        memory.STORE_PATH = os.path.join(tmp, "student_memory.json")
        try:
            fn()
        finally:
            memory.STORE_PATH = original


def test_grade_quiz_mixed_results():
    graded = memory.grade_quiz(QUIZ, {"q1": "A", "q2": "A"})
    assert graded["score"] == 1
    assert graded["total"] == 2
    assert graded["results"][0]["is_correct"] is True
    assert graded["results"][1]["is_correct"] is False
    print("PASS: test_grade_quiz_mixed_results")


def test_grade_quiz_unanswered_question():
    graded = memory.grade_quiz(QUIZ, {"q1": "A"})  # q2 not submitted
    q2_result = next(r for r in graded["results"] if r["quiz_id"] == "q2")
    assert q2_result["submitted"] is None
    assert q2_result["is_correct"] is False
    print("PASS: test_grade_quiz_unanswered_question")


def test_save_and_get_missed_concepts():
    def run():
        graded = memory.grade_quiz(QUIZ, {"q1": "B", "q2": "B"})  # q1 wrong, q2 correct
        memory.save_results("s1", graded)
        missed = memory.get_missed_concepts("s1")
        assert missed == ["c1"], missed
    with_temp_store(run)
    print("PASS: test_save_and_get_missed_concepts")


def test_later_attempt_overrides_earlier_for_same_concept():
    def run():
        # First attempt: c1 wrong.
        memory.save_results("s1", memory.grade_quiz(QUIZ, {"q1": "B", "q2": "B"}))
        assert memory.get_missed_concepts("s1") == ["c1"]
        # Retake: c1 now correct -> should no longer be "missed".
        memory.save_results("s1", memory.grade_quiz(QUIZ, {"q1": "A", "q2": "B"}))
        assert memory.get_missed_concepts("s1") == [], memory.get_missed_concepts("s1")
    with_temp_store(run)
    print("PASS: test_later_attempt_overrides_earlier_for_same_concept")


def test_students_are_isolated():
    def run():
        memory.save_results("s1", memory.grade_quiz(QUIZ, {"q1": "B", "q2": "B"}))  # s1 misses c1
        memory.save_results("s2", memory.grade_quiz(QUIZ, {"q1": "A", "q2": "A"}))  # s2 misses c2
        assert memory.get_missed_concepts("s1") == ["c1"]
        assert memory.get_missed_concepts("s2") == ["c2"]
    with_temp_store(run)
    print("PASS: test_students_are_isolated")


def test_get_missed_concepts_unknown_student():
    def run():
        assert memory.get_missed_concepts("nobody") == []
    with_temp_store(run)
    print("PASS: test_get_missed_concepts_unknown_student")


def test_build_requiz_filters_by_concept_and_accepts_list_or_dict():
    requiz = memory.build_requiz(["c1"], QUIZ)
    assert [q["id"] for q in requiz["quiz"]] == ["q1"]

    requiz_from_dict = memory.build_requiz(["c2"], {"quiz": QUIZ})
    assert [q["id"] for q in requiz_from_dict["quiz"]] == ["q2"]

    requiz_none_missed = memory.build_requiz([], QUIZ)
    assert requiz_none_missed["quiz"] == []
    print("PASS: test_build_requiz_filters_by_concept_and_accepts_list_or_dict")


def test_persistence_survives_reload():
    def run():
        memory.save_results("s1", memory.grade_quiz(QUIZ, {"q1": "B", "q2": "B"}))
        # Simulate "closing and reopening the app": re-read straight from disk.
        reloaded = memory._load_store()
        assert reloaded["s1"]["history"][0]["concept_id"] == "c1"
        assert memory.get_missed_concepts("s1") == ["c1"]
    with_temp_store(run)
    print("PASS: test_persistence_survives_reload")


if __name__ == "__main__":
    test_grade_quiz_mixed_results()
    test_grade_quiz_unanswered_question()
    test_save_and_get_missed_concepts()
    test_later_attempt_overrides_earlier_for_same_concept()
    test_students_are_isolated()
    test_get_missed_concepts_unknown_student()
    test_build_requiz_filters_by_concept_and_accepts_list_or_dict()
    test_persistence_survives_reload()
    print("\nAll tests passed.")
