from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class SampleFileItem(BaseModel):
    filename: str
    category: str
    relative_path: str

class GroundedEvidence(BaseModel):
    verbatim_quote: str
    page_number: int
    section_header: str

class VectorMatchItem(BaseModel):
    text: str
    metadata: Dict[str, Any]
    similarity_score: float

class ClauseAnalysisItem(BaseModel):
    is_risky: bool
    category: str
    defect_type: str
    severity: str  # HIGH, MEDIUM, LOW, NONE
    confidence_score: float
    explanation: str
    grounded_evidence: GroundedEvidence
    suggested_redline: Optional[str] = ""

class ClauseResultItem(BaseModel):
    clause_id: str
    header: str
    page_number: int
    text: str
    analysis: ClauseAnalysisItem
    vector_matches: List[VectorMatchItem] = Field(default_factory=list)

class ContractSummaryItem(BaseModel):
    overall_risk_score: float
    classification: str
    is_problematic: bool
    summary: str
    total_clauses: int
    flagged_count: int

class AnalysisResponse(BaseModel):
    filename: str
    character_count: int
    clause_count: int
    summary: ContractSummaryItem
    clauses: List[ClauseResultItem]
