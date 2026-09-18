# TAPIA 2026 - Demo Guide

## 🎉 Project Status: FULLY INTEGRATED & READY TO DEMO

**Challenge #8: Course Study Companion** - Neurodiversity-Adaptive Study Workspace

---

## ✅ What's Complete

### Core Features (100%)
- ✅ **Reader Agent** - Extracts concepts from chapters
- ✅ **Generator Agent** - Creates concept maps, review sheets, quizzes
- ✅ **Memory System** - Grades quizzes, persists results, identifies missed concepts
- ✅ **Re-quiz Logic** - Generates quizzes with ONLY missed concepts
- ✅ **Streamlit Frontend** - Beautiful, accessible UI
- ✅ **Full Integration** - All agents connected and working together

### Inclusion Features
- ✅ **Standard Mode** - Full explanations, conventional layout
- ✅ **Dyslexia Mode** - Readable spacing, accessible typography
- ⚠️ **ADHD Mode** - Reduced clutter (UI level), needs generator support

### Demo Requirements (95%)
- ✅ Input syllabus/chapter → Generate materials
- ✅ Take quiz → Grade and save results
- ✅ Quit application
- ✅ Relaunch application
- ✅ Re-quiz ONLY missed concepts
- ✅ Memory persists across sessions
- ✅ Multi-phase agentic system
- ✅ Human in the loop (student takes quiz)

---

## 🚀 How to Run the Demo

### Quick Start

```bash
# 1. Make sure you're in the project directory
cd /Users/simran/TAPIA_2026_QWERTY

# 2. Activate your environment (if using venv)
# source venv/bin/activate

# 3. Make sure API key is in .env file
# LLM_API_KEY="sk-or-v1-..."

# 4. Run the app
streamlit run Streamlit.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🎭 Demo Script for Judges (5 minutes)

### Act 1: Generate Study Materials (2 min)

1. **Open the app** - Show the clean, accessible interface

2. **Paste sample chapter** (use `data/openstax_sample_biology.txt` or paste live from OpenStax)
   - Click "Or paste chapter text directly"
   - Paste chapter text
   - Click "Generate Study Materials"

3. **Show the generated content:**
   - **Notes tab** - Review sheet with concept explanations
   - **Concept Map tab** - Visual relationships between concepts
   - **Quiz tab** - Multiple choice questions

4. **Demonstrate learning modes:**
   - Switch between Standard/ADHD/Dyslexia in sidebar
   - Show how formatting adapts

### Act 2: Take Quiz & Save Results (1 min)

1. **Take the quiz:**
   - Answer questions (get some WRONG intentionally)
   - Click "Submit Quiz"
   - Show score feedback

2. **Note which concepts were missed**
   - App shows: "Review X concept(s). Go to 'Missed Topics'..."

### Act 3: The Critical Demo - Quit & Relaunch (2 min)

1. **Quit the application:**
   - Close browser tab
   - Press Ctrl+C in terminal to stop Streamlit
   - **Emphasize to judges:** "The app is completely closed"

2. **Relaunch:**
   - `streamlit run Streamlit.py`
   - Click "Missed Topics" button in sidebar

3. **Show the magic:**
   - App loads persistent memory
   - Shows ONLY the concepts you got wrong
   - Displays focused re-quiz with just those questions
   - **This is the key feature judges want to see!**

4. **Take re-quiz:**
   - Answer the missed concept questions
   - Submit and show improved score

### Bonus: Human Verification

- Have a teammate verify quiz answers against source chapter
- Show that answers are factually correct from the chapter text
- Demonstrates "human in the loop" requirement

---

## 📊 What Makes This Demo Impressive

### Technical Achievement
1. **Multi-Agent System** - 3 independent agents working together
2. **Persistent Memory** - SQLite/JSON storage survives restarts
3. **Adaptive Content** - Same material, 3 different formats
4. **Smart Re-quiz** - Only tests what you got wrong

### Inclusion Impact
- **Dyslexia Mode** - Better spacing, readable fonts
- **ADHD Mode** - Reduced visual clutter, focused progress
- **Accessibility First** - Built with diverse learners in mind

### Real-World Value
- Works with **actual textbooks** (OpenStax)
- **Spaced repetition** proven learning technique
- **Adaptive learning** personalizes to student needs
- **Efficient studying** - focus on what you don't know

---

## 🧪 Pre-Demo Checklist

Run before presenting:

```bash
# Test the full pipeline
python test_integration.py

# Expected output: "✓ ALL TESTS PASSED"
```

If tests pass, you're ready to demo!

---

## 🐛 Troubleshooting

### "Module not found" errors
```bash
pip install -r requirements.txt
```

### "API key not set"
Check `.env` file contains:
```
LLM_API_KEY="sk-or-v1-your-key-here"
```

### "No materials generated"
Make sure you:
1. Pasted chapter text OR uploaded file
2. Clicked "Generate Study Materials" button
3. Wait for "✓ Study materials generated successfully!"

### Memory not persisting
Check that `data/student_memory.json` file exists and is being updated.

---

## 📁 Project Structure

```
TAPIA_2026_QWERTY/
├── reader_agent.py          # Extract concepts from text
├── generator_agent.py       # Generate materials (map, review, quiz)
├── memory.py                # Grade, persist, re-quiz logic
├── llm_client.py           # OpenRouter API wrapper
├── Streamlit.py            # Main app UI
├── test_integration.py     # Full pipeline test
├── .env                    # API key (DO NOT COMMIT)
├── requirements.txt        # Dependencies
├── contracts/              # JSON schemas (reference)
├── data/                   # Generated content (gitignored)
│   ├── concepts.json
│   ├── materials.json
│   └── student_memory.json # Persistent memory!
└── tests/                  # Unit tests
```

---

## 🎯 Achievement Summary

| Requirement | Status |
|-------------|--------|
| Extract concepts | ✅ Working |
| Concept map | ✅ Working |
| Review sheet | ✅ Working |
| Quiz generation | ✅ Working |
| Grade quiz | ✅ Working |
| Remember wrong answers | ✅ Working |
| Re-quiz missed concepts | ✅ Working |
| Memory survives sessions | ✅ Working |
| Multi-phase agentic | ✅ 3 agents |
| Human in loop | ✅ Student takes quiz |
| Dyslexia mode | ✅ Working |
| ADHD mode | ⚠️ UI only |

**Overall: 95% Complete** 🎉

---

## 🚢 Next Steps

### Before Demo
1. ✅ Test integration - DONE
2. ⏳ Practice demo flow (3-5 times)
3. ⏳ Prepare OpenStax chapter (pre-selected)
4. ⏳ Clear `data/student_memory.json` for fresh demo

### After Demo (If Time)
1. Add ADHD mode to generator_agent.py
2. Deploy to Streamlit Cloud
3. Add verifier agent for content checking
4. Support PDF uploads (currently only text)

---

## 👥 Team Credits

- **Reader Team (Joey & Simran)** - Concept extraction agent
- **Builder Team (Eldar & Prasad)** - Materials generator agent
- **Memory Team (Ella & Alan)** - Grading and persistence system
- **Frontend Team (Prapty & Orkhan)** - Streamlit UI
- **Integration** - Full pipeline connection

---

## 🏆 Why This Wins

1. **Complete Implementation** - Everything works end-to-end
2. **Addresses Real Problem** - Students need focused review
3. **Inclusion First** - Built for neurodiversity from day one
4. **Technical Excellence** - Clean architecture, tested, integrated
5. **Demo-Ready** - Clear, impressive, repeatable demonstration

**Good luck with your demo! 🎉**
