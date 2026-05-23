# Shortlisted — ATS Resume Analyzer

A web app that analyzes how well your resume matches a job description — built to help job seekers understand why their resumes get filtered out before reaching a human recruiter.

**Live:** [shortlisted on Render](https://shortlisted-nnw7.onrender.com)

---

## What it does

Most resumes never reach a hiring manager. They get filtered out by ATS (Applicant Tracking Systems) that scan for specific skills and keywords before any human sees the application.

Shortlisted tells you:
- How well your resume matches a specific job description
- Which required skills are present and which are missing
- Skills you have that go beyond what the JD asks for
- Structural issues in your resume that ATS systems struggle to parse
- Specific, prioritized suggestions to improve your chances

---

## How it works

1. Upload your resume as a PDF
2. Paste the job description you're applying for
3. Get a detailed ATS report in under 60 seconds

The scoring is based on weighted keyword matching — skills mentioned multiple times in the job description are treated as high priority and weighted 2x in the score calculation. The final score reflects how well your skills align with what the role actually requires.

---

## Tech stack

| Layer | Technology |
|---|---|
| Backend | Python, Flask |
| PDF parsing | pdfplumber |
| Keyword matching | Regex-based variant matching |
| Frontend | HTML, CSS, JavaScript |
| Deployment | Render |

---

## Project structure

shortlisted/
├── app.py          # Flask server — handles routing and API endpoints
├── analyzer.py     # Core analysis engine — scoring, matching, suggestions
├── utils.py        # PDF extraction and skill detection utilities
├── index.html      # Frontend — landing page and tool UI
└── requirements.txt

---

## Key design decisions

**Why regex over NLP/TF-IDF**
Early versions used TF-IDF cosine similarity for scoring. It gave misleading results because it penalized resumes for containing content unrelated to the JD — like university names, city names, and project descriptions. Switched to direct keyword matching which is more honest and closer to how real ATS systems work.

**Why a curated skill list over free-text extraction**
Free-text keyword extraction from JDs pulls generic words like "application", "code", "team" which aren't meaningful skills. A curated list of 150+ canonical skills with variant mapping ensures only relevant technical terms are matched — "node.js", "nodejs", and "node js" all resolve to the same canonical skill.

**Why weighted scoring**
Skills mentioned multiple times in a JD signal what the employer actually cares about. A skill mentioned once might be a nice-to-have; mentioned three times it's probably essential. High-priority skills (2+ mentions) count 2x in the score.

---

## Known limitations

- Works best for technical roles — software engineering, data science, DevOps, mobile development
- Skills not in the curated list won't be detected (e.g. niche frameworks or domain-specific tools)
- Slash notation in JDs (e.g. "C/C++/Java") is treated as an OR requirement — all variants are detected independently
- Score is based on skill keyword match only, not semantic understanding of experience level or context

---

## Running locally

```bash
# Clone the repo
git clone https://github.com/gsaanvi/shortlisted.git
cd shortlisted

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Run
python app.py
```

Open `http://localhost:5000` in your browser.

---

## What I'd build next

- **Lightcast API integration** — replace the curated skill list with a 32,000+ skill taxonomy that works for any industry and role type
- **PDF report export** — let users download their analysis as a formatted PDF
- **Multi-JD comparison** — analyze one resume against multiple job descriptions and rank them by match score
- **Bulk candidate screening** — HR-facing feature to upload multiple resumes and rank candidates against one JD

---

Built by Saanvi Gupta