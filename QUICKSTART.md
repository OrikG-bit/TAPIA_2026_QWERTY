# Quick Start Guide - For Judges & Demo

## 🚀 Run the App Locally

```bash
# 1. Navigate to project
cd TAPIA_2026_QWERTY

# 2. Make sure dependencies are installed
pip install -r requirements.txt

# 3. Run the app
streamlit run Streamlit.py
```

The app opens at: `http://localhost:8501`

## 📱 Live Demo URL

Once deployed: **[URL will be added after deployment]**

## 🎯 How to Use the App

### First Time: Generate Study Materials

1. **Click sidebar → "Study workspace"**

2. **Paste a chapter** in the text box (or upload a file)
   - Sample provided below, or use any OpenStax chapter
   - Click "Generate Study Materials"
   - Wait ~30 seconds for AI processing

3. **Explore the tabs:**
   - **Notes** - Review sheet with explanations
   - **Concept Map** - Visual relationships
   - **Quiz** - Test your knowledge

4. **Try learning modes** (sidebar):
   - Standard - Full explanations
   - ADHD - Reduced clutter
   - Dyslexia - Better spacing

### Take the Quiz

1. Go to **Quiz tab**
2. Answer the questions (get some wrong on purpose!)
3. Click **"Submit Quiz"**
4. See your score and feedback

### The Magic: Spaced Repetition

1. **Click "Missed Topics"** in sidebar
2. See ONLY the concepts you got wrong
3. Take the **re-quiz** with just those questions
4. Improve your score!

### Test Persistence

1. **Close the app** (close browser tab, stop the server)
2. **Relaunch:** `streamlit run Streamlit.py`
3. **Click "Missed Topics"** - your history is still there!

## 📝 Sample Chapter for Testing

Paste this into the app:

```
Introduction to Cell Biology

The Cell Theory is one of the fundamental principles of biology. It states that all living organisms are composed of one or more cells, the cell is the basic unit of life, and all cells arise from pre-existing cells. This theory was developed in the 19th century by scientists Matthias Schleiden, Theodor Schwann, and Rudolf Virchow.

Prokaryotic Cells are the simplest and oldest type of cells. They lack a membrane-bound nucleus and other membrane-bound organelles. Their DNA is located in a region called the nucleoid. Bacteria and archaea are examples of prokaryotic organisms. Despite their simplicity, prokaryotic cells are highly successful and exist in virtually every environment on Earth.

Eukaryotic Cells are more complex than prokaryotic cells. They contain a membrane-bound nucleus that houses their DNA, as well as various membrane-bound organelles such as mitochondria, endoplasmic reticulum, and Golgi apparatus. Animals, plants, fungi, and protists are all composed of eukaryotic cells.

The Cell Membrane, also called the plasma membrane, is a phospholipid bilayer that surrounds all cells. It is selectively permeable, meaning it controls what enters and exits the cell. Embedded proteins in the membrane facilitate transport and communication. The cell membrane is crucial for maintaining homeostasis within the cell.

Mitochondria are often called the powerhouses of the cell because they generate most of the cell's supply of ATP (adenosine triphosphate), which is used as a source of chemical energy. Mitochondria have their own DNA and can replicate independently, which supports the endosymbiotic theory that they were once free-living bacteria.

Chloroplasts are organelles found in plant cells and some protists that carry out photosynthesis. They contain chlorophyll, a green pigment that captures light energy from the sun and converts it into chemical energy stored in glucose. Like mitochondria, chloroplasts have their own DNA and are thought to have originated from endosymbiotic bacteria.

The Nucleus is the control center of eukaryotic cells. It contains the cell's genetic material (DNA) organized into chromosomes. The nuclear envelope, a double membrane with pores, separates the nucleus from the cytoplasm. Inside the nucleus is the nucleolus, where ribosomal RNA is synthesized.
```

## 🐛 Troubleshooting

**"Error: LLM_API_KEY not set"**
- Ask the developers to check the `.env` file

**"No materials generated"**
- Make sure you pasted chapter text
- Click the "Generate Study Materials" button
- Wait for completion message

**"Missed Topics is empty"**
- You need to take a quiz first
- Make sure you get at least one question wrong

## 🎬 5-Minute Demo Script

**Minute 1:** Show home page, explain the problem (students waste time reviewing what they already know)

**Minute 2:** Paste chapter → Generate → Show concept map and review sheet

**Minute 3:** Take quiz (get 2-3 wrong), submit, see results

**Minute 4:** Close app completely, relaunch, go to Missed Topics

**Minute 5:** Show re-quiz with ONLY missed concepts - this is the key feature!

**Bonus:** Show learning mode switches (Standard/ADHD/Dyslexia)
