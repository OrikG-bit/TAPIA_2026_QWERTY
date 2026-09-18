# TAPIA 2026 — Course Study Companion

Neurodiversity-Adaptive Study Workspace (Challenge 8)

An agentic system that turns a syllabus + chapter into a concept map, review sheet, and quiz — adapted for standard, ADHD, or dyslexia-friendly learning styles — and remembers what a student got wrong to re-quiz only that, even after closing and reopening the app.

## Team & Ownership

| Pair | Members | Owns | Branch |
| --- | --- | --- | --- |
| A — Reader | *names* | Extract topics from chapter/syllabus | `reader` |
| B — Builder | *names* | Concept map + review sheet + quiz (standard/ADHD/dyslexia) | `builder` |
| C — Memory | *names* | Grading + persistent memory + re-quiz logic | `memory` |
| D — Frontend + Verifier | *names* | Streamlit UI + fact-checking rewritten content | `frontend` |

**Integration Owner:** *name* — does not write agent code; owns `contracts/` accuracy and runs the two checkpoint merges.

## Project Structure

```text
TAPIA_2026_QWERTY/
├── README.md
├── requirements.txt
├── llm_client.py          # shared LLM call wrapper — everyone imports from here
├── reader_agent.py        # Pair A
├── generator_agent.py     # Pair B
├── verifier_agent.py      # Pair D (verifier half)
├── memory.py               # Pair C
├── app.py                  # Pair D (frontend half)
├── contracts/               # FAKE sample JSON — build against these until checkpoints
│   ├── concepts.json
│   ├── materials.json
│   └── student_memory.json
└── data/                    # real chapter/syllabus text + generated output at runtime
    ├── source_chapter.txt
    ├── concepts.json         # Pair A's real output lands here
    ├── materials.json        # Pair B's real output lands here
    └── student_memory.json   # Pair C's real output lands here (or use SQLite instead)
```

**Rule:** the fake files in `contracts/` never get edited during the hackathon — they're the fixed reference shape. Real generated output goes in `data/`, which is gitignored (see below) so we don't spam the repo with regenerated JSON every run.

## Naming Conventions

**Files:** `snake_case.py` — one file per agent (e.g. `reader_agent.py`, not `ReaderAgent.py`)

**Functions:** `snake_case`, verb-first, matching the contract:

- `extract_topics(chapter_text) -> dict`
- `generate_materials(concepts_json, mode) -> dict`
- `verify_content(original_text, rewritten_text) -> dict`
- `grade_quiz(quiz, submitted_answers) -> dict`

**JSON keys:** always `snake_case`, never `camelCase` — e.g. `concept_id`, not `conceptId`. This matters because Python dicts and JSON keys need to match exactly between teams.

**IDs:** concepts are `c1`, `c2`, ...; quiz questions are `q1`, `q2`, ... Keep these consistent — Pair C's memory logic keys off `concept_id`, so if Pair A or B changes the ID format, tell the group immediately.

**Branches:** one per pair — `reader`, `builder`, `memory`, `frontend`. No personal branches; pairs share one branch.

**Commits:** short and descriptive, e.g. `git commit -m "reader: add source_text field to output"` — prefix with your pair name so it's easy to scan history.

## Setup (everyone runs this after cloning)

```bash
git clone https://github.com/OrikG-bit/TAPIA_2026_QWERTY.git
cd TAPIA_2026_QWERTY
git checkout <your-branch>          # e.g. git checkout reader

python3 -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

Set your API key (from the $100 gift card, if you're not using Claude Code directly):

```bash
export LLM_API_KEY="your-key-here"   # Windows: set LLM_API_KEY=your-key-here
```

Test the shared LLM connection works:

```bash
python llm_client.py
```

You should see a short response printed. If this fails, fix it before writing your own agent — everyone depends on this file.

`requirements.txt`

```text
openai
streamlit
```

(Add to this file, don't create a second requirements file. If your pair needs something else — e.g. `networkx` for the concept map, `textstat` for readability scoring — add it here and tell the group.)

## Data Contracts (the shapes that connect all 4 pairs)

Full schemas and field-by-field explanations are in `contracts/*.json` — these are the exact JSON shapes your function must produce or consume. **Do not change a field name or structure without telling everyone in the group chat first** — a silent change breaks whoever's downstream of you.

Quick reference:

| File | Produced by | Consumed by |
| --- | --- | --- |
| `concepts.json` | Pair A | Pair B |
| `materials.json` | Pair B | Pair C, Pair D |
| `student_memory.json` | Pair C | Pair D |
| `verification_report.json` | Pair D (verifier) | Pair D (frontend), demo |

## Workflow Rules

1. **Build against `contracts/` fake data first.** Don't wait for another pair's real output — swap it in later.
2. **Push early, push often**, even broken code, to your own branch. The integration owner needs visibility.
3. **Two checkpoints only** — roughly 1:30 and 2:45 into the hackathon. That's when branches merge into `main` and real data replaces fake data. Don't merge outside these unless something's blocking everyone.
4. **If you need to change a contract shape**, message the group first — don't just push it.
5. **Test your function standalone** (each agent file has a `if __name__ == "__main__":` block at the bottom) before assuming it works with anyone else's code.

## Demo Checklist

- [ ] Same passage shown in standard vs. ADHD vs. dyslexia mode, side by side
- [ ] Verifier's report confirming nothing was lost/invented between versions
- [ ] Live: take quiz → get some wrong → close app → reopen → only missed topics re-quizzed
- [ ] One specific agent mistake, caught by a human, shown on stage

`.gitignore`

```gitignore
venv/
__pycache__/
*.pyc
data/*.json
.env
```
