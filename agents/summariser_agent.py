# agents/summariser_agent.py
import google.generativeai as genai
from agents.base_agent import BaseAgent
from configs.settings import GEMINI_API_KEY

class SummariserAgent(BaseAgent):
    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-flash")

    def execute(self, input_data: str, topic: str) -> str:
        prompt = (
            "You are the Summariser Agent in a CrewAI multi-agent research assistant system called ResearchMate.\n"
            "The Research Agent has collected a set of research articles for the following topic.\n\n"
            "Your task is to read the documents and synthesize them into a single, highly structured, academic research report.\n\n"
            "The report MUST include the following sections:\n"
            "1. Title (short and descriptive)\n"
            "2. Introduction (brief overview of the topic)\n"
            "3. Key Findings (detailed research synthesis)\n"
            "4. Discussion (interpretation and analysis of findings)\n"
            "5. Conclusion (wrap-up + future directions)\n"
            "6. At the end, add a 'References' section where you list ONLY the original article titles provided in the input as a numbered list.\n\n"
            "Important guidelines:\n"
            "- Maintain formal academic writing style.\n"
            "- Add numbered references inline in the report as [1], [2], etc.\n"
            "- Do NOT invent or add external sources.\n"
            "- Do NOT format references as a table. Only use numbered list format: [1] Article Title.\n"
            "- Keep each reference on a single line.\n\n"
            f"Research Topic: {topic}\n\n"
            "Research Articles:\n\n"
            f"{input_data}"
        )
        response = self.model.generate_content(prompt)
        return response.text
