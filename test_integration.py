"""Quick test to verify all agents work together before running Streamlit"""

import json
from reader_agent import extract_topics
from generator_agent import generate_materials
import memory

print("=" * 60)
print("INTEGRATION TEST - Full Pipeline")
print("=" * 60)

# Sample chapter text
chapter_text = """
Introduction to Machine Learning

Machine Learning is a subset of artificial intelligence that enables computers to learn from data without being explicitly programmed. The system improves its performance on a task through experience.

Supervised Learning is a type of machine learning where the algorithm learns from labeled training data. The model is trained on input-output pairs and learns to predict outputs for new inputs. Examples include classification and regression tasks.

Unsupervised Learning works with unlabeled data to find hidden patterns or structures. Common techniques include clustering, where similar data points are grouped together, and dimensionality reduction.

Neural Networks are computing systems inspired by biological neural networks. They consist of layers of interconnected nodes that process information and learn complex patterns through training.
"""

print("\n1. Testing Reader Agent...")
print("-" * 60)
try:
    concepts = extract_topics(chapter_text)
    print(f"✓ Extracted {len(concepts['concepts'])} concepts:")
    for c in concepts['concepts']:
        print(f"  - {c['id']}: {c['name']}")
except Exception as e:
    print(f"✗ Reader agent failed: {e}")
    exit(1)

print("\n2. Testing Generator Agent...")
print("-" * 60)
try:
    materials = generate_materials(concepts, "standard")
    print(f"✓ Generated materials:")
    print(f"  - Concept map nodes: {len(materials['concept_map']['nodes'])}")
    print(f"  - Review sheet entries: {len(materials['review_sheet'])}")
    print(f"  - Quiz questions: {len(materials['quiz'])}")
except Exception as e:
    print(f"✗ Generator agent failed: {e}")
    exit(1)

print("\n3. Testing Memory System...")
print("-" * 60)
try:
    # Simulate wrong answers for first 2 questions
    quiz = materials['quiz']
    submitted = {}
    for i, q in enumerate(quiz):
        if i < 2:
            # Submit wrong answer
            correct = q['answer']
            wrong_options = ['A', 'B', 'C', 'D']
            wrong_options.remove(correct)
            submitted[q['id']] = wrong_options[0]
        else:
            # Submit correct answer
            submitted[q['id']] = q['answer']

    # Grade quiz
    graded = memory.grade_quiz(quiz, submitted)
    print(f"✓ Quiz graded: {graded['score']}/{graded['total']}")

    # Save results
    memory.save_results("test_student", graded)
    print("✓ Results saved to memory")

    # Get missed concepts
    missed = memory.get_missed_concepts("test_student")
    print(f"✓ Missed concepts: {missed}")

    # Build re-quiz
    requiz = memory.build_requiz(missed, materials)
    print(f"✓ Re-quiz generated: {len(requiz['quiz'])} questions")

except Exception as e:
    print(f"✗ Memory system failed: {e}")
    exit(1)

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED - INTEGRATION COMPLETE!")
print("=" * 60)
print("\nYou can now run: streamlit run Streamlit.py")
