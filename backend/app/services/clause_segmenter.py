import re
from typing import Dict, List, Any

class ClauseSegmenter:
    """
    Segments full contract text or page streams into structured, location-aware clauses/sections.
    """

    @staticmethod
    def segment_contract(parsed_doc: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Splits contract text into logical sections/clauses based on structural headers or double linebreaks,
        attaching page numbers and structural metadata for evidence grounding.
        """
        raw_text = parsed_doc.get("raw_text", "")
        pages = parsed_doc.get("pages", [])
        
        if not raw_text:
            return []

        # Pattern for numbered headers: e.g. "SECTION 1", "1. Supply", "ARTICLE II", "Clause 4."
        header_pattern = re.compile(
            r'\n(?=(?:\b(?:SECTION|ARTICLE|CLAUSE)\s+\d+|\b\d+\.\s+[A-Z]))',
            re.IGNORECASE
        )
        
        raw_chunks = header_pattern.split(raw_text)
        clauses: List[Dict[str, Any]] = []
        chunk_id = 1
        
        for chunk in raw_chunks:
            chunk = chunk.strip()
            if not chunk or len(chunk) < 15:
                continue
                
            lines = [l.strip() for l in chunk.split('\n') if l.strip()]
            header = lines[0] if lines else f"Section {chunk_id}"
            
            # Map clause to page number if PDF pages available
            page_num = 1
            if len(pages) > 1:
                for p in pages:
                    if chunk[:50] in p["text"]:
                        page_num = p["page_num"]
                        break
            
            clauses.append({
                "clause_id": f"C{chunk_id:02d}",
                "header": header[:100],
                "text": chunk,
                "page_number": page_num,
                "line_count": len(lines),
                "char_length": len(chunk)
            })
            chunk_id += 1
            
        return clauses
