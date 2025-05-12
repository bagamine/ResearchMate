# tools/pubmed_tool.py
import os
import requests
import logging
from tools.base_tool import BaseTool
from configs.settings import OUTPUT_PATH
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter

class PubMedTool(BaseTool):
    def sanitize_filename(self, title: str) -> str:
        return "".join(c if c.isalnum() or c in " _-" else "_" for c in title)[:80].replace(" ", "_")

    def run(self, input_data: str, topic: str) -> list:
        logging.info("[PubMedTool] Fetching articles from PubMed...")

        base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
        search_url = f"{base_url}esearch.fcgi"
        fetch_url = f"{base_url}efetch.fcgi"

        # ✅ Step 1: Search for multiple article IDs
        params = {"db": "pubmed", "term": input_data, "retmax": 5, "retmode": "json"}
        response = requests.get(search_url, params=params)
        ids = response.json().get("esearchresult", {}).get("idlist", [])

        if not ids:
            logging.info("[PubMedTool] No PubMed articles found.")
            return [{"title": "No PubMed Results", "content": "No articles found."}]

        articles = []

        # ✅ Step 2: Download and save each article separately
        for idx, pubmed_id in enumerate(ids, start=1):
            params = {"db": "pubmed", "id": pubmed_id, "retmode": "xml"}
            response = requests.get(fetch_url, params=params)
            raw_text = response.text

            safe_topic = self.sanitize_filename(topic)
            txt_path = f"{OUTPUT_PATH}articles/pubmed_{idx}_{safe_topic}.txt"
            os.makedirs(os.path.dirname(txt_path), exist_ok=True)
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(raw_text)
            logging.info(f"[PubMedTool] ✅ Saved raw PubMed txt: {txt_path}")

            # ✅ Add article to list for orchestrator tracking
            articles.append({
                "title": f"PubMed Article {idx} for '{topic}'",
                "content": raw_text
            })

        return articles
