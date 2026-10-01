import sys
from pathlib import Path

# Add project root to python path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from backend.app.core.config import settings
from backend.app.services.document_parser import DocumentParser
from backend.app.services.clause_segmenter import ClauseSegmenter
from backend.app.services.vector_store import VectorStore

def index_reference_contracts():
    print("=" * 70)
    print("LEGAL PREDICTOR - INGESTING & INDEXING REFERENCE CONTRACT DATASET")
    print("=" * 70)

    vector_store = VectorStore()
    
    clean_files = sorted([f for f in settings.RAW_CLEAN_DIR.glob("*.docx") if not f.name.endswith(".gitkeep")])
    prob_files = sorted([f for f in settings.RAW_PROB_DIR.glob("*.docx") if not f.name.endswith(".gitkeep")])
    
    reference_clauses = []

    print(f"\nProcessing {len(clean_files)} CLEAN reference contracts...")
    for f in clean_files:
        doc_data = DocumentParser.parse_file(f, f.name)
        clauses = ClauseSegmenter.segment_contract(doc_data)
        for c in clauses:
            item_id = f"CLEAN_{f.stem}_{c['clause_id']}"
            reference_clauses.append({
                "id": item_id,
                "text": c["text"],
                "metadata": {
                    "source_filename": f.name,
                    "ground_truth_label": "CLEAN",
                    "clause_id": c["clause_id"],
                    "header": c["header"],
                    "page_number": c["page_number"]
                }
            })

    print(f"Processing {len(prob_files)} PROB reference contracts...")
    for f in prob_files:
        doc_data = DocumentParser.parse_file(f, f.name)
        clauses = ClauseSegmenter.segment_contract(doc_data)
        for c in clauses:
            item_id = f"PROB_{f.stem}_{c['clause_id']}"
            reference_clauses.append({
                "id": item_id,
                "text": c["text"],
                "metadata": {
                    "source_filename": f.name,
                    "ground_truth_label": "PROB",
                    "clause_id": c["clause_id"],
                    "header": c["header"],
                    "page_number": c["page_number"]
                }
            })

    print(f"\nTotal reference clauses extracted: {len(reference_clauses)}")
    vector_store.add_reference_clauses(reference_clauses)
    
    print("\n" + "=" * 70)
    print(f"INDEXING COMPLETE. Total items in ChromaDB collection: {vector_store.count()}")
    print("=" * 70)

if __name__ == "__main__":
    index_reference_contracts()
