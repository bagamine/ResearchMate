# agents/research_agent.py
import logging
from agents.base_agent import BaseAgent
from tools.pubmed_tool import PubMedTool
from tools.arxiv_tool import ArxivTool
from tools.document_search_tool import DocumentSearchTool

class ResearchAgent(BaseAgent):
    def __init__(self, orchestrator=None):
        super().__init__()
        self.orchestrator = orchestrator  # NEW: pass orchestrator
        self.tools = [
            PubMedTool(),
            ArxivTool(),
            DocumentSearchTool()
        ]

    def execute(self, input_data: str, topic: str) -> str:
        logging.info("[ResearchAgent] Starting research phase...")

        # Reset orchestrator articles list if passed
        if self.orchestrator:
            self.orchestrator.article_sources = []

        results = []
        for tool in self.tools:
            logging.info(f"[ResearchAgent] Running tool: {tool.__class__.__name__}")
            result = tool.run(input_data, topic)

            # --- NEW: enforce article_sources tracking ---
            if isinstance(result, dict) and "title" in result and "content" in result:
                # Tool returned structured article
                if self.orchestrator:
                    self.orchestrator.article_sources.append(result)
                results.append(result["content"])
            elif isinstance(result, list):
                # In case your tool returns list of articles
                for item in result:
                    if isinstance(item, dict) and "title" in item and "content" in item:
                        if self.orchestrator:
                            self.orchestrator.article_sources.append(item)
                        results.append(item["content"])
            else:
                # fallback for legacy tools returning just text
                if self.orchestrator:
                    self.orchestrator.article_sources.append({"title": topic, "content": result})
                results.append(result)

        logging.info("[ResearchAgent] Research phase complete.")
        return "\n\n".join(results)
