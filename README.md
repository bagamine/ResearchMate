# **ResearchMate - Autonomous Research Assistant**


# ResearchMate 🧠📄

ResearchMate is an advanced autonomous multi-agent research assistant powered by LLMs.  
It automates the full process of researching, synthesizing, and generating academic reports on any topic.

This version provides the full backend research pipeline without any graphical user interface.

---

## Key Features

- Autonomous multi-agent architecture
- Supports multiple document sources: arXiv, PubMed, local documents
- Orchestrates fully automated research-to-report pipeline
- Saves all collected articles as PDFs
- Generates structured academic reports (markdown + PDF)
- Uses Gemini API for summarisation and editing
- Highly modular design for easy extension and production use



## ResearchMate Pipeline Overview

1️⃣ **Research Agent**
- Accepts a research topic
- Collects relevant articles from arXiv, PubMed, and document files
- Saves all articles as `{title, content}` objects

2️⃣ **Summariser Agent**
- Reads all collected articles
- Synthesizes into a single structured academic report:
    - Title
    - Introduction
    - Key Findings
    - Discussion
    - Conclusion
    - References (based on article titles)

3️⃣ **Editor Agent**
- Polishes and enhances report for clarity, grammar, and academic tone
- Enforces academic formatting standards

4️⃣ **Report Generation**
- Outputs structured markdown
- Converts to professional PDF using ReportLab Platypus engine
- Includes automatic references list matching articles

---

## 🛠️ Architecture

```

+--------------------+
\|    User Input      |
+--------------------+
        |
        v
+--------------------+
\|   Research Agent   |
+--------------------+
        |
        v
+--------------------+
\|  Summariser Agent  |
+--------------------+
        |
        v
+--------------------+
\|    Editor Agent    |
+--------------------+
        |
        v
+--------------------+
\|  PDF Report Output |
+--------------------+

```

---

## 🔧 Technologies

- Python 3.10+
- CrewAI framework (latest version)
- Gemini API (`gemini-flash-1.5` model)
- arXiv & PubMed API integrations
- ReportLab for PDF rendering

---

## 📂 Project Structure

```

/ResearchMate
├── agents/
│   ├── base\_agent.py
│   ├── research\_agent.py
│   ├── summariser\_agent.py
│   ├── editor\_agent.py
├── tools/
│   ├── base\_tool.py
│   ├── arxiv\_tool.py
│   ├── pubmed\_tool.py
│   ├── document\_search\_tool.py
├── workflows/
│   ├── orchestrator.py
├── configs/
│   ├── settings.py
├── outputs/
│   ├── final\_report.pdf
│   ├── articles/\*.pdf
├── main.py

````

---

## ✅ How to Run (Backend only)

1️⃣ Clone repository:
```bash
git clone https://github.com/yourusername/researchmate.git
cd researchmate
````

2️⃣ Create environment:

```bash
conda create -n crewai python=3.10
conda activate crewai
pip install -r requirements.txt
```

3️⃣ Add your Gemini API key inside `configs/settings.py`

4️⃣ Run main pipeline:

```bash
python main.py --topic "Your Research Topic Here"
```

5️⃣ Output files will be saved inside `/outputs/`:

```
final_report.pdf
articles/*.pdf
```

---

## 🔒 Disclaimer

This version of ResearchMate provides backend agent functionality only.
The optional Streamlit web interface is not included in this repository version.

---

## 💡 Authors

* Project lead: \[BAGUENNA Mohammed-Amine,[LinkedIn](https://www.linkedin.com/in/baguenna-mohammed-amine/)]
* Based on Gemini

