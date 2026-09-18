# OpenStax Content Guide for Demo

## What is OpenStax?

OpenStax is a **nonprofit educational initiative** providing **free, peer-reviewed textbooks**. Perfect for your hackathon demo because:
- ✅ **Legally free to use** (CC BY license)
- ✅ **High-quality content** used by real universities
- ✅ **Wide range of subjects**
- ✅ **Easy to access** (web + PDF)

Website: https://openstax.org/

## How to Get Content for Your Demo

### Method 1: Copy from Website (EASIEST)
1. Go to https://openstax.org/subjects
2. Pick a book (e.g., "Biology 2e", "Introduction to Computer Science")
3. Click "View online"
4. Navigate to a chapter
5. Select and copy the text
6. Paste into your app or save as `.txt` file

### Method 2: Download PDF
1. Go to https://openstax.org/
2. Find a book
3. Click "Download" → PDF
4. Open PDF, copy chapter text
5. Clean up formatting if needed

## Recommended Books for Demo

### Best for Clear Concepts (Recommended):

**1. Biology 2e**
- URL: https://openstax.org/books/biology-2e/pages/1-introduction
- Why: Clear distinct concepts (cells, organelles, photosynthesis)
- Good for concept maps with relationships
- Example chapter: "Cell Structure and Function" (see `data/openstax_sample_biology.txt`)

**2. Introduction to Computer Science**
- URL: https://openstax.org/books/introduction-computer-science/pages/1-introduction
- Why: Algorithms, data structures - technical and precise
- Good for students/judges who understand tech

**3. Psychology 2e**
- URL: https://openstax.org/books/psychology-2e/pages/1-introduction
- Why: Interesting, accessible concepts
- Good for general audience demo

**4. Calculus Volume 1**
- URL: https://openstax.org/books/calculus-volume-1/pages/1-introduction
- Why: Mathematical concepts are distinct
- Shows your system works with equations

### What Makes Good Demo Content:

✅ **5-8 clear concepts** in a chapter  
✅ **Distinct topics** (not all overlapping)  
✅ **Relationships between concepts** (for concept map)  
✅ **Quiz-able facts** (dates, definitions, cause-effect)  
✅ **Not too technical** (judges need to understand it)

## Sample Content Included

I've created: `data/openstax_sample_biology.txt`
- Biology chapter on Cell Structure
- Has 8 clear concepts
- Ready to test with your reader agent
- Try it: `python reader_agent.py`

## For Your Demo

### Before the Demo:
1. **Pick 2-3 chapters** (in case one doesn't work well)
2. **Test each one** with your pipeline
3. **Choose the one** with the best concept map and quiz
4. **Save it** as your demo input

### During the Demo:
**Option A: Pre-loaded**
- Have the chapter already loaded
- Shows cleaner, faster demo
- Less can go wrong

**Option B: Live paste**
- Copy from OpenStax website live
- Shows it works on real content
- More impressive but riskier

I recommend **Option A** - save time, less risk.

## Testing Your System

Try the sample I created:
```bash
cd /Users/simran/TAPIA_2026_QWERTY
python reader_agent.py  # Will use data/source_chapter.txt
```

Or test with biology sample:
```bash
# Temporarily replace the source
cp data/openstax_sample_biology.txt data/source_chapter.txt
python reader_agent.py
```

## License Info (For Judges)

OpenStax content is **CC BY 4.0 licensed**:
- ✅ Free to use
- ✅ Can modify
- ✅ Can redistribute
- Must attribute: "Source: OpenStax, Biology 2e"

This makes your demo **legally clean** - important for judges!

## Other Resources Mentioned

The challenge also mentioned:
- **"Attention Is All You Need"** paper (arXiv) - famous transformer paper
- **ArXiv papers** - https://arxiv.org/
- More technical, for advanced demo

**Recommendation**: Start with OpenStax (easier), add arXiv paper support later if time permits.
