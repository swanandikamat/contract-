from typing import Dict, List, Any, Union
from pathlib import Path
from backend.app.services.document_parser import DocumentParser
from backend.app.services.clause_segmenter import ClauseSegmenter
from backend.app.services.vector_store import VectorStore
from backend.app.services.llm_analyzer import LLMAnalyzer

class RAGPipeline:
    """
    Unified Retrieval-Augmented Generation (RAG) Legal Risk Analysis Pipeline.
    """

    def __init__(self, api_key: str = None):
        self.vector_store = VectorStore()
        self.llm_analyzer = LLMAnalyzer(api_key=api_key)

    def analyze_document(
        self,
        file_source: Union[str, Path, bytes],
        filename: str
    ) -> Dict[str, Any]:
        """
        Executes end-to-end document parsing, vector retrieval, LLM reasoning, and evidence aggregation.
        """
        # 1. Extraction & Parsing
        doc_data = DocumentParser.parse_file(file_source, filename)
        raw_text = doc_data.get("raw_text", "")

        # 2. Structural Clause Segmentation
        clauses = ClauseSegmenter.segment_contract(doc_data)

        # 3. Process Each Clause via Vector Search + LLM Reasoning
        evaluated_clauses: List[Dict[str, Any]] = []
        flagged_risky_clauses: List[Dict[str, Any]] = []

        for clause in clauses:
            # Semantic search in ChromaDB for reference matches
            vector_matches = self.vector_store.search_similar(clause["text"], top_k=3)
            
            # Contextual LLM evaluation
            analysis = self.llm_analyzer.analyze_clause(
                target_clause=clause,
                vector_matches=vector_matches,
                contract_context_snippet=raw_text[:2000]
            )

            clause_result = {
                "clause_id": clause["clause_id"],
                "header": clause["header"],
                "page_number": clause["page_number"],
                "text": clause["text"],
                "analysis": analysis,
                "vector_matches": vector_matches
            }
            evaluated_clauses.append(clause_result)

            if analysis.get("is_risky"):
                flagged_risky_clauses.append(analysis)

        # 4. Aggregate Contract-Level Risk Summary
        summary_info = self.llm_analyzer.summarize_contract(
            filename=filename,
            total_clauses=len(clauses),
            risky_clauses=flagged_risky_clauses
        )

        return {
            "filename": filename,
            "character_count": len(raw_text),
            "clause_count": len(clauses),
            "summary": summary_info,
            "clauses": evaluated_clauses
        }
