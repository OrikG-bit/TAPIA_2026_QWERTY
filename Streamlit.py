import json
from pathlib import Path
import streamlit as st

# Import our agents
from reader_agent import extract_topics
from generator_agent import generate_materials
import memory


# =========================================================
# APP CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Course Study Companion",
    layout="wide",
    initial_sidebar_state="expanded"
)

CONTRACTS_DIR = Path("contracts")
DATA_DIR = Path("data")

# Default student ID for demo
STUDENT_ID = "demo_student"


# =========================================================
# DATA HELPERS
# =========================================================

def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def load_materials():
    """
    During frontend development, load fake contract data.
    Later this can be replaced with data/materials.json.
    """
    return load_json(CONTRACTS_DIR / "materials.json")


def load_student_memory():
    return load_json(CONTRACTS_DIR / "student_memory.json")


def normalize_list(value):
    """
    Converts different JSON shapes into a predictable list.
    """
    if value is None:
        return []

    if isinstance(value, list):
        return value

    if isinstance(value, dict):
        return list(value.values())

    return [value]


def get_item_title(item, default="Study Topic"):
    """
    Works whether item is a string or dictionary.
    Prevents:
    AttributeError: 'str' object has no attribute 'get'
    """
    if isinstance(item, dict):
        return (
            item.get("title")
            or item.get("name")
            or item.get("topic")
            or item.get("concept")
            or item.get("heading")
            or default
        )

    if isinstance(item, str):
        return default

    return default


def get_item_text(item):
    """
    Safely extracts text from multiple possible contract shapes.
    """
    if isinstance(item, str):
        return item

    if isinstance(item, dict):
        return (
            item.get("content")
            or item.get("description")
            or item.get("summary")
            or item.get("text")
            or item.get("explanation")
            or item.get("definition")
            or str(item)
        )

    return str(item)


# =========================================================
# SESSION STATE
# =========================================================

if "stage" not in st.session_state:
    st.session_state.stage = "workspace"

if "materials" not in st.session_state:
    st.session_state.materials = load_materials()

if "learning_mode" not in st.session_state:
    st.session_state.learning_mode = "Standard"

if "current_concept" not in st.session_state:
    st.session_state.current_concept = 0

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False


# =========================================================
# ACCESSIBILITY / DESIGN SYSTEM
# =========================================================

def apply_theme(mode):

    # -----------------------------------------
    # STANDARD
    # -----------------------------------------

    if mode == "Standard":
        font_size = "16px"
        line_height = "1.55"
        letter_spacing = "0"
        content_width = "1150px"
        background = "#F7F8FA"
        card_background = "#FFFFFF"

    # -----------------------------------------
    # ADHD
    # -----------------------------------------

    elif mode == "ADHD":
        font_size = "18px"
        line_height = "1.7"
        letter_spacing = "0.01em"
        content_width = "900px"
        background = "#F5F7F8"
        card_background = "#FFFFFF"

    # -----------------------------------------
    # DYSLEXIA
    # -----------------------------------------

    else:
        font_size = "17px"
        line_height = "1.8"
        letter_spacing = "0.04em"
        content_width = "950px"
        background = "#FAF8F2"
        card_background = "#FFFDF8"

    st.markdown(
        f"""
        <style>

        /* ==========================================
           GLOBAL
        ========================================== */

        .stApp {{
            background: {background};
            color: #17212B;
            font-family: Arial, Verdana, sans-serif;
        }}

        .block-container {{
            max-width: {content_width};
            padding-top: 2.2rem;
            padding-bottom: 4rem;
        }}

        html, body, [class*="css"] {{
            font-size: {font_size};
        }}

        p, li {{
            line-height: {line_height};
            letter-spacing: {letter_spacing};
        }}

        h1, h2, h3 {{
            color: #17212B;
            font-weight: 650;
            letter-spacing: -0.02em;
        }}

        h1 {{
            font-size: 2.25rem;
        }}

        h2 {{
            margin-top: 1rem;
        }}


        /* ==========================================
           SIDEBAR
        ========================================== */

        [data-testid="stSidebar"] {{
            background: #101820;
            border-right: 1px solid #26323D;
        }}

        [data-testid="stSidebar"] * {{
            color: #F4F6F8;
        }}

        [data-testid="stSidebar"] h1,
        [data-testid="stSidebar"] h2,
        [data-testid="stSidebar"] h3 {{
            color: white;
        }}

        [data-testid="stSidebar"] hr {{
            border-color: #34414C;
        }}


        /* ==========================================
           BUTTONS
        ========================================== */

        .stButton > button {{
            border-radius: 8px;
            min-height: 44px;
            font-weight: 600;
            border: 1px solid #CBD2D9;
            background: white;
            color: #17212B;
            transition: 0.15s ease;
        }}

        .stButton > button:hover {{
            border-color: #355D78;
            color: #24465B;
        }}

        .stButton > button[kind="primary"] {{
            background: #214D68;
            color: white;
            border: none;
        }}


        /* ==========================================
           CARDS
        ========================================== */

        .study-card {{
            background: {card_background};
            border: 1px solid #E1E5E8;
            border-radius: 10px;
            padding: 1.4rem 1.5rem;
            margin-bottom: 1rem;
        }}

        .section-label {{
            color: #5E6B75;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            font-weight: 700;
            margin-bottom: 0.4rem;
        }}

        .muted {{
            color: #66737D;
        }}


        /* ==========================================
           METRICS / STATUS
        ========================================== */

        [data-testid="stMetric"] {{
            background: {card_background};
            border: 1px solid #E1E5E8;
            padding: 1rem;
            border-radius: 10px;
        }}


        /* ==========================================
           TABS
        ========================================== */

        button[data-baseweb="tab"] {{
            font-weight: 600;
            padding-left: 18px;
            padding-right: 18px;
        }}


        /* ==========================================
           INPUTS
        ========================================== */

        [data-testid="stFileUploader"] {{
            background: {card_background};
            border-radius: 10px;
        }}


        /* ==========================================
           DYSLEXIA SPECIFIC
        ========================================== */

        {"p, li { max-width: 70ch; }" if mode == "Dyslexia" else ""}


        /* ==========================================
           ADHD SPECIFIC
        ========================================== */

        {"div[data-testid='stVerticalBlock'] { gap: 0.8rem; }" if mode == "ADHD" else ""}

        </style>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("Study Companion")

    st.caption(
        "Adaptive learning workspace"
    )

    st.divider()

    st.subheader("Learning mode")

    learning_mode = st.radio(
        "Choose how study content is presented",
        ["Standard", "ADHD", "Dyslexia"],
        key="learning_mode",
        label_visibility="collapsed"
    )

    st.divider()

    st.subheader("Workspace")

    if st.button("Study workspace", use_container_width=True):
        st.session_state.stage = "workspace"

    if st.button("Missed topics", use_container_width=True):
        st.session_state.stage = "missed"

    st.divider()

    st.subheader("Current mode")

    st.write(learning_mode)

    if learning_mode == "Standard":
        st.caption(
            "Full explanations with a conventional study layout."
        )

    elif learning_mode == "ADHD":
        st.caption(
            "Reduced visual clutter, shorter sections and focused progress."
        )

    else:
        st.caption(
            "Readable spacing, accessible typography and reduced text density."
        )


apply_theme(learning_mode)


# =========================================================
# PAGE HEADER
# =========================================================

st.markdown(
    '<div class="section-label">TAPIA 2026</div>',
    unsafe_allow_html=True
)

st.title("Course Study Companion")

st.markdown(
    """
    Transform course materials into structured study resources,
    adaptive learning experiences and persistent review sessions.
    """
)

st.divider()


# =========================================================
# WORKSPACE PAGE
# =========================================================

if st.session_state.stage == "workspace":

    # -----------------------------------------------------
    # STEP 1 — COURSE MATERIALS
    # -----------------------------------------------------

    st.header("1. Course Materials")

    st.caption(
        "Upload a syllabus and a chapter, research paper or course reading."
    )

    col1, col2 = st.columns(2)

    with col1:
        syllabus_file = st.file_uploader(
            "Syllabus",
            type=["pdf", "txt"],
            key="syllabus"
        )

    with col2:
        chapter_file = st.file_uploader(
            "Chapter or research paper",
            type=["pdf", "txt"],
            key="chapter"
        )

    # Option to paste text directly
    chapter_text_input = st.text_area(
        "Or paste chapter text directly:",
        height=150,
        placeholder="Paste your chapter or reading text here..."
    )

    generate = st.button(
        "Generate Study Materials",
        type="primary",
        use_container_width=True
    )

    if generate:
        try:
            chapter_text = None

            # Get chapter text from uploaded file or text input
            if chapter_file:
                chapter_text = chapter_file.read().decode("utf-8")
            elif chapter_text_input:
                chapter_text = chapter_text_input
            else:
                st.error("Please upload a chapter file or paste chapter text.")
                st.stop()

            # Show progress
            with st.spinner("Extracting concepts from chapter..."):
                # Step 1: Extract concepts using reader agent
                concepts = extract_topics(chapter_text)
                st.session_state.concepts = concepts

            st.success(f"✓ Extracted {len(concepts['concepts'])} concepts")

            # Get learning mode
            learning_mode_map = {
                "Standard": "standard",
                "ADHD": "standard",  # Will format differently in display
                "Dyslexia": "dyslexia"
            }
            mode = learning_mode_map.get(st.session_state.get("learning_mode", "Standard"), "standard")

            with st.spinner(f"Generating study materials in {mode} mode..."):
                # Step 2: Generate materials using generator agent
                materials = generate_materials(concepts, mode)
                st.session_state.materials = materials

            st.success("✓ Study materials generated successfully!")

            # Save concepts and materials to data directory
            DATA_DIR.mkdir(exist_ok=True)
            with open(DATA_DIR / "concepts.json", "w") as f:
                json.dump(concepts, f, indent=2)
            with open(DATA_DIR / "materials.json", "w") as f:
                json.dump(materials, f, indent=2)

        except Exception as e:
            st.error(f"Error generating materials: {str(e)}")
            st.exception(e)

    st.divider()


    # -----------------------------------------------------
    # STEP 2 — STUDY WORKSPACE
    # -----------------------------------------------------

    st.header("2. Study Workspace")

    materials = st.session_state.materials

    tabs = st.tabs(
        [
            "Notes",
            "Concept Map",
            "Critical Review",
            "Quiz",
            "Verification"
        ]
    )


    # =====================================================
    # NOTES
    # =====================================================

    with tabs[0]:

        st.subheader("Study Notes")

        notes = (
            materials.get("notes")
            or materials.get("study_notes")
            or materials.get("content")
            or []
        )

        notes = normalize_list(notes)

        if not notes:
            st.info(
                "Study notes will appear here after generation."
            )

        elif learning_mode == "ADHD":

            # ADHD mode: one concept at a time

            current = st.session_state.current_concept

            if current >= len(notes):
                current = len(notes) - 1

            progress = (current + 1) / len(notes)

            st.progress(progress)

            st.caption(
                f"Topic {current + 1} of {len(notes)}"
            )

            item = notes[current]

            title = get_item_title(
                item,
                f"Topic {current + 1}"
            )

            text = get_item_text(item)

            st.markdown(
                f"""
                <div class="study-card">
                    <div class="section-label">
                        Focus topic
                    </div>
                    <h3>{title}</h3>
                    <p>{text}</p>
                </div>
                """,
                unsafe_allow_html=True
            )

            previous_col, next_col = st.columns(2)

            with previous_col:
                if st.button(
                    "Previous Topic",
                    disabled=current == 0,
                    use_container_width=True
                ):
                    st.session_state.current_concept -= 1
                    st.rerun()

            with next_col:
                if st.button(
                    "Next Topic",
                    disabled=current >= len(notes) - 1,
                    use_container_width=True
                ):
                    st.session_state.current_concept += 1
                    st.rerun()

        else:

            for index, item in enumerate(notes):

                title = get_item_title(
                    item,
                    f"Topic {index + 1}"
                )

                text = get_item_text(item)

                st.markdown(
                    f"""
                    <div class="study-card">
                        <div class="section-label">
                            Topic {index + 1}
                        </div>
                        <h3>{title}</h3>
                        <p>{text}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


    # =====================================================
    # CONCEPT MAP
    # =====================================================

    with tabs[1]:

        st.subheader("Concept Map")

        concept_map = (
            materials.get("concept_map")
            or materials.get("concepts")
            or []
        )

        concept_map = normalize_list(concept_map)

        if not concept_map:

            st.info(
                "The concept map will appear here after generation."
            )

        else:

            st.caption(
                "Major concepts and their relationships."
            )

            for index, concept in enumerate(concept_map):

                title = get_item_title(
                    concept,
                    f"Concept {index + 1}"
                )

                description = get_item_text(concept)

                st.markdown(
                    f"""
                    <div class="study-card">
                        <div class="section-label">
                            Concept {index + 1}
                        </div>
                        <h3>{title}</h3>
                        <p>{description}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


    # =====================================================
    # CRITICAL REVIEW
    # =====================================================

    with tabs[2]:

        st.subheader("Critical Review Sheet")

        review = (
            materials.get("review_sheet")
            or materials.get("critical_review")
            or materials.get("review")
            or []
        )

        review = normalize_list(review)

        if not review:

            st.info(
                "The critical review sheet will appear here."
            )

        else:

            for index, item in enumerate(review):

                title = get_item_title(
                    item,
                    f"Review Point {index + 1}"
                )

                text = get_item_text(item)

                with st.expander(
                    title,
                    expanded=learning_mode == "Dyslexia"
                ):
                    st.write(text)


    # =====================================================
    # QUIZ
    # =====================================================

    with tabs[3]:

        st.subheader("Knowledge Check")

        st.caption(
            "Complete the quiz to identify topics that should be reviewed again."
        )

        quiz = (
            materials.get("quiz")
            or materials.get("questions")
            or []
        )

        quiz = normalize_list(quiz)

        if not quiz:

            st.info(
                "Quiz questions will appear here after generation."
            )

        else:

            submitted_answers = {}

            for index, question in enumerate(quiz):

                if isinstance(question, str):

                    st.markdown(
                        f"""
                        <div class="study-card">
                            <div class="section-label">
                                Question {index + 1}
                            </div>
                            <p>{question}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    continue

                question_id = (
                    question.get("question_id")
                    or question.get("id")
                    or f"q{index + 1}"
                )

                question_text = (
                    question.get("question")
                    or question.get("text")
                    or question.get("prompt")
                    or f"Question {index + 1}"
                )

                options = (
                    question.get("options")
                    or question.get("choices")
                    or []
                )

                st.markdown(
                    f"### Question {index + 1}"
                )

                st.write(question_text)

                if options:

                    submitted_answers[question_id] = st.radio(
                        "Select one answer",
                        options,
                        key=f"quiz_{question_id}",
                        index=None
                    )

                else:

                    submitted_answers[question_id] = st.text_input(
                        "Your answer",
                        key=f"quiz_{question_id}"
                    )

                st.divider()

            if st.button(
                "Submit Quiz",
                type="primary",
                use_container_width=True
            ):

                st.session_state.submitted_answers = submitted_answers
                st.session_state.quiz_submitted = True

                try:
                    # Grade the quiz using memory system
                    quiz_data = materials.get("quiz", [])
                    graded = memory.grade_quiz(quiz_data, submitted_answers)

                    # Save results to persistent memory
                    memory.save_results(STUDENT_ID, graded)

                    # Display results
                    score = graded["score"]
                    total = graded["total"]
                    percentage = (score / total * 100) if total > 0 else 0

                    if score == total:
                        st.balloons()
                        st.success(f"🎉 Perfect score! {score}/{total} ({percentage:.0f}%)")
                    elif score >= total * 0.7:
                        st.success(f"✓ Good job! {score}/{total} ({percentage:.0f}%)")
                    else:
                        st.warning(f"Keep studying! {score}/{total} ({percentage:.0f}%)")

                    # Show which concepts to review
                    missed_count = total - score
                    if missed_count > 0:
                        st.info(f"💡 Review {missed_count} concept(s). Go to 'Missed Topics' to practice them again.")

                    # Show detailed results
                    with st.expander("View detailed results"):
                        for result in graded["results"]:
                            status = "✓" if result["is_correct"] else "✗"
                            st.write(f"{status} Question {result['quiz_id']}: {result['submitted']} (correct: {result['correct_answer']})")

                    # Store in session for display
                    st.session_state.last_quiz_results = graded

                except Exception as e:
                    st.error(f"Error grading quiz: {str(e)}")
                    st.exception(e)


    # =====================================================
    # VERIFICATION
    # =====================================================

    with tabs[4]:

        st.subheader("Content Verification")

        st.write(
            """
            The verifier compares adaptive study content with the
            original source to ensure important information was not
            removed, changed or invented.
            """
        )

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Status",
                "Development"
            )

        with col2:
            st.metric(
                "Source Checked",
                "Pending"
            )

        with col3:
            st.metric(
                "Adaptive Version",
                learning_mode
            )

        st.info(
            "Verifier-agent results will appear here after agent integration."
        )


# =========================================================
# MISSED TOPICS PAGE
# =========================================================

elif st.session_state.stage == "missed":

    st.header("Missed Topics - Spaced Repetition")

    st.write(
        """
        This workspace shows only the concepts you got wrong in previous quizzes.
        Focus your review time on what you need to learn!
        """
    )

    try:
        # Get missed concepts from persistent memory
        missed_concept_ids = memory.get_missed_concepts(STUDENT_ID)

        if not missed_concept_ids:
            st.success("🎉 Great job! You haven't missed any concepts yet.")
            st.info("Complete a quiz in the Study Workspace to track your progress.")

        else:
            st.warning(f"📚 You have {len(missed_concept_ids)} concept(s) to review:")

            # Show which concepts were missed
            if "concepts" in st.session_state.get("concepts", {}):
                concepts = st.session_state.concepts["concepts"]
                missed_concepts = [c for c in concepts if c["id"] in missed_concept_ids]

                for concept in missed_concepts:
                    with st.expander(f"📌 {concept['name']}"):
                        st.write(f"**Summary:** {concept['summary']}")
                        st.write(f"**Source:** {concept['source_text']}")

            st.divider()

            # Generate re-quiz with only missed concepts
            st.subheader("Practice Quiz - Missed Concepts Only")

            if "materials" in st.session_state and st.session_state.materials:
                materials = st.session_state.materials
                requiz = memory.build_requiz(missed_concept_ids, materials)

                if requiz.get("quiz"):
                    st.info(f"This quiz contains {len(requiz['quiz'])} question(s) covering only the concepts you missed.")

                    submitted_answers = {}

                    for index, question in enumerate(requiz["quiz"]):
                        question_id = question.get("id", f"q{index + 1}")
                        question_text = question.get("question", f"Question {index + 1}")
                        options = question.get("options", [])

                        st.markdown(f"### Question {index + 1}")
                        st.write(question_text)

                        if options:
                            submitted_answers[question_id] = st.radio(
                                "Select one answer",
                                options,
                                key=f"requiz_{question_id}",
                                label_visibility="collapsed"
                            )

                        st.divider()

                    if st.button("Submit Re-Quiz", type="primary", use_container_width=True):
                        try:
                            # Grade the re-quiz
                            graded = memory.grade_quiz(requiz["quiz"], submitted_answers)
                            memory.save_results(STUDENT_ID, graded)

                            score = graded["score"]
                            total = graded["total"]
                            percentage = (score / total * 100) if total > 0 else 0

                            if score == total:
                                st.balloons()
                                st.success(f"🎉 Perfect! You've mastered these concepts! {score}/{total}")
                            else:
                                st.warning(f"Score: {score}/{total} ({percentage:.0f}%). Keep practicing!")

                        except Exception as e:
                            st.error(f"Error grading re-quiz: {str(e)}")

                else:
                    st.info("Generate study materials first to practice missed concepts.")
            else:
                st.info("Generate study materials in the Study Workspace first.")

    except Exception as e:
        st.error(f"Error loading missed topics: {str(e)}")
        st.exception(e)

    st.divider()

    st.caption(
        "✨ Student memory persists across sessions - quit the app and relaunch to test it!"
    )