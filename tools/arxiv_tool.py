# tools/arxiv_tool.py
import requests
import arxiv
import os
import logging
from tools.base_tool import BaseTool
from configs.settings import OUTPUT_PATH

class ArxivTool(BaseTool):
    def sanitize_filename(self, title: str) -> str:
        return "".join(c if c.isalnum() or c in " _-" else "_" for c in title)[:80].replace(" ", "_")

    def run(self, input_data: str, topic: str) -> str:
        logging.info("[ArxivTool] Fetching papers from arXiv...")
        search = arxiv.Search(
            query=input_data, 
            max_results=10, 
            sort_by=arxiv.SortCriterion.Relevance
            )
        results = []
        os.makedirs(f"{OUTPUT_PATH}articles/", exist_ok=True)

        for result in search.results():
            results.append(f"Title: {result.title}\nSummary: {result.summary}\n")

            # NEW: Download full PDF from arXiv
            
            pdf_url = result.pdf_url
            pdf_response = requests.get(pdf_url)
            clean_title = self.sanitize_filename(result.title)
            pdf_path = f"{OUTPUT_PATH}articles/arxiv_{clean_title}.pdf"
            with open(pdf_path, "wb") as f:
                f.write(pdf_response.content)
            logging.info(f"[ArxivTool] Downloaded PDF: {pdf_path}")

        output = "\n".join(results) if results else "No arXiv papers found."
        return output

