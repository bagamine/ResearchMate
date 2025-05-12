# tools/document_search_tool.py
import glob
import os
import logging
from tools.base_tool import BaseTool
from configs.settings import DATA_PATH, OUTPUT_PATH

class DocumentSearchTool(BaseTool):
    def run(self, input_data: str, topic: str) -> str:
        logging.info("[DocumentSearchTool] Searching local documents...")
        results = []
        files = glob.glob(os.path.join(DATA_PATH, "*.txt"))
        for file in files:
            with open(file, "r", encoding="utf-8") as f:
                content = f.read()
                if input_data.lower() in content.lower():
                    results.append(f"File: {file}\n{content[:1000]}...\n")
        output = "\n".join(results) if results else "No local documents matched."

        # Save output
        filename = f"{OUTPUT_PATH}articles/document_search_{topic.replace(' ', '_')}.txt"
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(output)

        return output
