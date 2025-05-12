# main.py
import argparse
import logging
from workflows.orchestrator import Orchestrator

def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

    parser = argparse.ArgumentParser(description="AI Research Assistant")
    parser.add_argument("--topic", required=True, help="Research topic")
    args = parser.parse_args()

    orchestrator = Orchestrator()
    final_report = orchestrator.run_pipeline(args.topic)

    print("\n========== FINAL PDF REPORT GENERATED ==========\n")
    print(f"Check outputs/final_report.pdf")

if __name__ == "__main__":
    main()
