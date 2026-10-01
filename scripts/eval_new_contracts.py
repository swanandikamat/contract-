import sys
import json
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.services.pipeline import RAGPipeline

def evaluate_test_suite():
    clean_dir = ROOT_DIR / "data" / "test_contracts" / "clean"
    prob_dir = ROOT_DIR / "data" / "test_contracts" / "prob"
    
    clean_files = list(clean_dir.glob("*.docx"))
    prob_files = list(prob_dir.glob("*.docx"))
    
    pipeline = RAGPipeline()
    results = []
    
    print("\n=======================================================")
    print("      EVALUATING MODEL ON NEW OUT-OF-SAMPLE TEST SUITE ")
    print("=======================================================\n")
    
    # Evaluate Clean Contracts
    print("--- 1. TESTING NEW CLEAN CONTRACTS ---")
    for fpath in clean_files:
        print(f"\nAnalyzing Clean Contract: {fpath.name}")
        res = pipeline.analyze_document(fpath, fpath.name)
        summary = res["summary"]
        print(f"  * Total Clauses: {res['clause_count']}")
        print(f"  * Risk Score: {summary['overall_risk_score']}/100")
        print(f"  * Classification: {summary['classification']}")
        print(f"  * Flagged Risk Clauses: {summary['flagged_count']}")
        
        results.append({
            "expected_type": "CLEAN",
            "filename": fpath.name,
            "risk_score": summary['overall_risk_score'],
            "classification": summary['classification'],
            "is_problematic": summary['is_problematic'],
            "flagged_count": summary['flagged_count'],
            "flagged_clauses": [
                {
                    "clause_id": c.get("clause_id"),
                    "header": c.get("header"),
                    "severity": c.get("severity"),
                    "explanation": c.get("explanation")
                } for c in res.get("clauses", []) if c.get("is_risky")
            ]
        })

    # Evaluate Problematic Contracts
    print("\n--- 2. TESTING NEW PROBLEMATIC CONTRACTS ---")
    for fpath in prob_files:
        print(f"\nAnalyzing Problematic Contract: {fpath.name}")
        res = pipeline.analyze_document(fpath, fpath.name)
        summary = res["summary"]
        print(f"  * Total Clauses: {res['clause_count']}")
        print(f"  * Risk Score: {summary['overall_risk_score']}/100")
        print(f"  * Classification: {summary['classification']}")
        print(f"  * Flagged Risk Clauses: {summary['flagged_count']}")
        for c in res.get("clauses", []):
            if c.get("is_risky"):
                print(f"    - [{c.get('severity')}] Header: '{c.get('header')}' | Defect: {c.get('defect_type')} | Redline: {c.get('suggested_redline')[:80]}...")

        results.append({
            "expected_type": "PROB",
            "filename": fpath.name,
            "risk_score": summary['overall_risk_score'],
            "classification": summary['classification'],
            "is_problematic": summary['is_problematic'],
            "flagged_count": summary['flagged_count'],
            "flagged_clauses": [
                {
                    "clause_id": c.get("clause_id"),
                    "header": c.get("header"),
                    "severity": c.get("severity"),
                    "defect_type": c.get("defect_type"),
                    "explanation": c.get("explanation"),
                    "suggested_redline": c.get("suggested_redline")
                } for c in res.get("clauses", []) if c.get("is_risky")
            ]
        })

    # Calculate Evaluation Summary Metrics
    clean_correct = sum(1 for r in results if r["expected_type"] == "CLEAN" and not r["is_problematic"])
    prob_correct = sum(1 for r in results if r["expected_type"] == "PROB" and r["is_problematic"])
    total_docs = len(results)
    accuracy = ((clean_correct + prob_correct) / total_docs) * 100 if total_docs > 0 else 0.0

    print("\n=======================================================")
    print(f" EVALUATION SUMMARY: Accuracy = {accuracy:.1f}% ({clean_correct + prob_correct}/{total_docs} docs)")
    print("=======================================================")
    
    out_path = ROOT_DIR / "data" / "test_contracts" / "eval_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print(f"Full evaluation results saved to: {out_path}")

if __name__ == "__main__":
    evaluate_test_suite()
