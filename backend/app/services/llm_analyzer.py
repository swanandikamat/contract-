import os
import json
from typing import Dict, List, Any
from backend.app.core.config import settings

class LLMAnalyzer:
    """
    Leverages Google Gemini API (`google-genai` SDK) to perform contextual risk analysis,
    structured classification, confidence estimation, and redlining grounded in vector retrieval matches.
    """

    def __init__(self, api_key: str = None, model_name: str = None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY", settings.GEMINI_API_KEY)
        self.model_name = model_name or settings.GEMINI_MODEL_NAME
        self.client = None
        self._init_client()

    def _init_client(self):
        # Ignore placeholder keys
        is_placeholder = not self.api_key or "your_" in self.api_key.lower() or "here" in self.api_key.lower()
        if not is_placeholder and self.api_key.strip():
            try:
                from google import genai
                self.client = genai.Client(api_key=self.api_key.strip())
                print(f"[LLMAnalyzer] Initialized Gemini API client with model {self.model_name}")
            except Exception as e:
                print(f"[LLMAnalyzer] Warning: Could not initialize Gemini API client: {e}")
        else:
            print("[LLMAnalyzer] Info: GEMINI_API_KEY not set. Running in Vector Semantic RAG mode.")

    def analyze_clause(
        self,
        target_clause: Dict[str, Any],
        vector_matches: List[Dict[str, Any]],
        contract_context_snippet: str = ""
    ) -> Dict[str, Any]:
        """
        Analyzes a single target clause along with its top-K retrieved reference matches.
        Returns a structured dictionary with risk assessment, severity, confidence, grounding, and redlines.
        """
        if self.client:
            try:
                prompt = self._build_prompt(target_clause, vector_matches, contract_context_snippet)
                response = self.client.models.generate_content(
                    model=self.model_name,
                    contents=prompt
                )
                
                resp_text = response.text.strip()
                if resp_text.startswith("```json"):
                    resp_text = resp_text[7:]
                if resp_text.endswith("```"):
                    resp_text = resp_text[:-3]
                    
                data = json.loads(resp_text.strip())
                return data
            except Exception as e:
                print(f"[LLMAnalyzer] Gemini API call error: {e}. Switching to RAG semantic fallback.")

        return self._semantic_rag_fallback(target_clause, vector_matches)

    def _build_prompt(
        self,
        target_clause: Dict[str, Any],
        vector_matches: List[Dict[str, Any]],
        contract_context_snippet: str
    ) -> str:
        ref_summary = []
        for idx, match in enumerate(vector_matches, 1):
            meta = match.get("metadata", {})
            ref_summary.append(
                f"Reference Match #{idx} (Similarity: {match.get('similarity_score', 0):.2f}, "
                f"Label: {meta.get('ground_truth_label', 'UNKNOWN')}, File: {meta.get('source_filename', '')}):\n"
                f"\"{match.get('text', '')[:300]}\""
            )
        ref_text = "\n\n".join(ref_summary)

        return f"""You are a senior legal counsel auditing a commercial contract clause for risk exposure.

Target Clause ID: {target_clause.get('clause_id')}
Header: {target_clause.get('header')}
Page Number: {target_clause.get('page_number')}
Verbatim Text:
"{target_clause.get('text')}"

Contract Snippet Context:
"{contract_context_snippet[:1500]}"

Semantically Similar Reference Clauses (from Benchmark Dataset):
{ref_text if ref_text else "No reference vector matches found."}

Analyze this clause for legal risks (e.g. uncapped liability, one-sided indemnity, auto-renewal traps, missing safeguards, vague specs, foreign jurisdiction, overbroad non-compete, currency penalty).

Return your evaluation as a strictly valid JSON object with key structures:
{{
  "is_risky": <true or false>,
  "category": "<Standard Clause Category Name>",
  "defect_type": "<Short Defect Identifier or CLEAN>",
  "severity": "<HIGH, MEDIUM, LOW, or NONE>",
  "confidence_score": <float between 0.0 and 1.0>,
  "explanation": "<Clear plain-English explanation of risk exposure>",
  "grounded_evidence": {{
    "verbatim_quote": "<Exact verbatim snippet from clause text>",
    "page_number": {target_clause.get('page_number', 1)},
    "section_header": "{target_clause.get('header', '')}"
  }},
  "suggested_redline": "<Balanced redline or negotiation edit if risky, or empty string if clean>"
}}
Respond ONLY with raw JSON. Do not include markdown formatting or codeblocks.
"""

    def _semantic_rag_fallback(
        self,
        target_clause: Dict[str, Any],
        vector_matches: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Semantic fallback grounded in comparative vector retrieval scores (PROB vs CLEAN similarity).
        """
        prob_matches = [m for m in vector_matches if m.get("metadata", {}).get("ground_truth_label") == "PROB"]
        clean_matches = [m for m in vector_matches if m.get("metadata", {}).get("ground_truth_label") == "CLEAN"]

        top_prob_sim = prob_matches[0].get("similarity_score", 0.0) if prob_matches else 0.0
        top_clean_sim = clean_matches[0].get("similarity_score", 0.0) if clean_matches else 0.0

        is_risky = False
        severity = "NONE"
        confidence = 0.85
        explanation = "Clause aligns with standard, balanced commercial terms."
        defect_type = "CLEAN"
        category = "General / Miscellaneous"
        redline = ""

        # Flag only when similarity to a PROB risk clause is high AND significantly stronger than to clean clauses
        if top_prob_sim >= 0.72 and (top_prob_sim > top_clean_sim + 0.05):
            is_risky = True
            severity = "HIGH" if top_prob_sim >= 0.82 else "MEDIUM"
            confidence = round(top_prob_sim, 2)
            meta = prob_matches[0].get("metadata", {})
            defect_type = "SEMANTIC_RISK_MATCH"
            category = meta.get("header", "Legal Risk Exposure")
            explanation = (
                f"High semantic similarity ({int(top_prob_sim*100)}%) to known benchmark risk pattern "
                f"in reference document '{meta.get('source_filename')}'."
            )
            redline = "Revise clause to ensure mutual obligations and standard risk caps."

        return {
            "is_risky": is_risky,
            "category": category,
            "defect_type": defect_type,
            "severity": severity,
            "confidence_score": confidence,
            "explanation": explanation,
            "grounded_evidence": {
                "verbatim_quote": target_clause.get("text", "")[:250],
                "page_number": target_clause.get("page_number", 1),
                "section_header": target_clause.get("header", "")
            },
            "suggested_redline": redline
        }

    def summarize_contract(
        self,
        filename: str,
        total_clauses: int,
        risky_clauses: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        high_severity_count = sum(1 for c in risky_clauses if c.get("severity") == "HIGH")
        medium_severity_count = sum(1 for c in risky_clauses if c.get("severity") == "MEDIUM")
        
        score = min(100.0, round((high_severity_count * 25.0) + (medium_severity_count * 15.0), 1))
        is_prob = score >= 35.0 or high_severity_count > 0
        classification = "PROBABLE ISSUES / HIGH RISK" if is_prob else "CLEAN / LOW RISK"

        summary_text = (
            f"Analyzed '{filename}' across {total_clauses} clauses using RAG + LLM engine. "
            f"Identified {len(risky_clauses)} flagged risk clauses ({high_severity_count} High, {medium_severity_count} Medium). "
            f"Overall contract risk score: {score}/100."
        )

        return {
            "overall_risk_score": score,
            "classification": classification,
            "is_problematic": is_prob,
            "summary": summary_text,
            "total_clauses": total_clauses,
            "flagged_count": len(risky_clauses)
        }
