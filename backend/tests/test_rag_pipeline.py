import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.core.config import settings
from backend.app.services.pipeline import RAGPipeline

def test_rag_pipeline_clean():
    clean_files = list(settings.RAW_CLEAN_DIR.glob("*.docx"))
    assert len(clean_files) > 0, "No clean files found"
    
    pipeline = RAGPipeline()
    res = pipeline.analyze_document(clean_files[0], clean_files[0].name)
    
    assert res["filename"] == clean_files[0].name
    assert res["clause_count"] > 0
    assert "summary" in res
    assert "clauses" in res
    print(f"\n[Test RAG Pipeline CLEAN] Document: {res['filename']}")
    print(f"  * Clause count: {res['clause_count']}")
    print(f"  * Risk Score: {res['summary']['overall_risk_score']}")
    print(f"  * Classification: {res['summary']['classification']}")

def test_rag_pipeline_prob():
    prob_files = list(settings.RAW_PROB_DIR.glob("*.docx"))
    assert len(prob_files) > 0, "No prob files found"
    
    pipeline = RAGPipeline()
    res = pipeline.analyze_document(prob_files[0], prob_files[0].name)
    
    assert res["filename"] == prob_files[0].name
    assert res["clause_count"] > 0
    assert "summary" in res
    print(f"\n[Test RAG Pipeline PROB] Document: {res['filename']}")
    print(f"  * Clause count: {res['clause_count']}")
    print(f"  * Risk Score: {res['summary']['overall_risk_score']}")
    print(f"  * Classification: {res['summary']['classification']}")

if __name__ == "__main__":
    test_rag_pipeline_clean()
    test_rag_pipeline_prob()
