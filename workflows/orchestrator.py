# workflows/orchestrator.py
import os
import logging
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.pagesizes import letter
from agents.research_agent import ResearchAgent
from agents.summariser_agent import SummariserAgent
from agents.editor_agent import EditorAgent
from configs.settings import OUTPUT_PATH, load_pipeline_config

class Orchestrator:
    def __init__(self):
        config = load_pipeline_config()
        self.config = config
        self.research_enabled = config["pipeline"]["agents"].get("research", True)
        self.summariser_enabled = config["pipeline"]["agents"].get("summariser", True)
        self.editor_enabled = config["pipeline"]["agents"].get("editor", True)

        self.research_agent = ResearchAgent() if self.research_enabled else None
        self.summariser_agent = SummariserAgent() if self.summariser_enabled else None
        self.editor_agent = EditorAgent() if self.editor_enabled else None

        self.article_sources = []  # NEW: Track articles

    def sanitize_topic(self, topic: str) -> str:
        return "".join(c if c.isalnum() or c in " _-" else "_" for c in topic)[:80].replace(" ", "_")

    def get_source_files(self, topic: str) -> list:
        folder = os.path.join(OUTPUT_PATH, "articles")
        if not os.path.exists(folder):
            return []
        topic_name = self.sanitize_topic(topic)
        return [f for f in os.listdir(folder) if f.endswith(".pdf") and topic_name in f]

    def write_pdf_using_platypus(self, text: str, topic: str, filename: str):
        logging.info(f"Writing final structured PDF: {filename}")
        os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)

        doc = SimpleDocTemplate(filename, pagesize=letter,
                                rightMargin=50, leftMargin=50,
                                topMargin=50, bottomMargin=50)

        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='Heading1Centered',
                                  parent=styles['Heading1'],
                                  alignment=1,
                                  spaceAfter=20))

        elements = []

        # Title + metadata
        elements.append(Paragraph(f"<b>ResearchMate Final Report</b>", styles['Heading1Centered']))
        
        elements.append(Paragraph(f"<b>Topic:</b> {topic}", styles['Normal']))
        elements.append(Paragraph(f"<b>Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        elements.append(Spacer(1, 20))

        # Research Summary
        for para in text.split("\n\n"):
            if para.strip():
                elements.append(Paragraph(para.strip().replace("\n", " "), styles['Normal']))
                elements.append(Spacer(1, 12))

        # NEW: Add References
        if self.article_sources:
            elements.append(Spacer(1, 20))
            elements.append(Paragraph("References:", styles['Heading2']))
            for idx, article in enumerate(self.article_sources, 1):
                elements.append(Paragraph(f"[{idx}] {article['title']}", styles['Normal']))

        doc.build(elements)
        logging.info(f"✅ PDF successfully generated: {filename}")

    def run_pipeline(self, topic: str) -> str:
        logging.info(f"Running AI Research Pipeline for topic: {topic}")

        # NEW: clear sources for each run
        self.article_sources = []

        # --- Step 1: Gather data ---
        data = topic
        if self.research_agent:
            # NEW: pull articles from ResearchAgent tools
            # Add this logic inside your ResearchAgent → self.article_sources.append({"title": ..., "content": ...})
            data = self.research_agent.execute(topic, topic)
            logging.info("Research complete.")

        # --- Step 2: Pre-process article dataset for summarisation ---
        if self.article_sources:
            combined_text = ""
            for idx, article in enumerate(self.article_sources, 1):
                combined_text += f"[{idx}] {article['title']}\n{article['content']}\n\n"
            data = combined_text

        # --- Step 3: Summarise + edit ---
        if self.summariser_agent:
            data = self.summariser_agent.execute(data, topic)
            logging.info("Summarisation complete.")

        if self.editor_agent:
            data = self.editor_agent.execute(data, topic)
            logging.info("Editing complete.")

        # --- Step 4: Save final report ---
        final_pdf_path = self.config["settings"]["final_report_pdf"]
        self.write_pdf_using_platypus(data, topic, final_pdf_path)

        return data
