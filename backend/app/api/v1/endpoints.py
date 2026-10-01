from typing import List, Optional
from fastapi import APIRouter, UploadFile, File, HTTPException, Query
from backend.app.core.config import settings
from backend.app.services.pipeline import RAGPipeline
from backend.app.services.vector_store import VectorStore
from backend.app.api.v1.schemas import AnalysisResponse, SampleFileItem

router = APIRouter()

@router.get("/health", tags=["Health"])
def health_check():
    vector_store = VectorStore()
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
        "vector_store_count": vector_store.count()
    }

@router.get("/samples", response_model=List[SampleFileItem], tags=["Benchmark Data"])
def get_sample_contracts():
    """
    Returns the list of 20 benchmark contracts (10 CLEAN, 10 PROB) available for testing.
    """
    samples: List[SampleFileItem] = []
    
    if settings.RAW_CLEAN_DIR.exists():
        for file_path in settings.RAW_CLEAN_DIR.glob("*.docx"):
            if not file_path.name.endswith(".gitkeep"):
                samples.append(SampleFileItem(
                    filename=file_path.name,
                    category="CLEAN",
                    relative_path=str(file_path.relative_to(settings.DATA_DIR))
                ))
                
    if settings.RAW_PROB_DIR.exists():
        for file_path in settings.RAW_PROB_DIR.glob("*.docx"):
            if not file_path.name.endswith(".gitkeep"):
                samples.append(SampleFileItem(
                    filename=file_path.name,
                    category="PROB",
                    relative_path=str(file_path.relative_to(settings.DATA_DIR))
                ))
                
    return sorted(samples, key=lambda x: (x.category, x.filename))

@router.post("/analyze", response_model=AnalysisResponse, tags=["Analysis"])
async def analyze_contract(
    file: Optional[UploadFile] = File(None),
    sample_filename: Optional[str] = Query(None, description="Filename from benchmark dataset to analyze")
):
    """
    Executes RAG + LLM analysis on an uploaded contract file or a benchmark sample contract.
    """
    filename = ""
    file_bytes = None
    file_path = None
    
    if file is not None:
        filename = file.filename
        file_bytes = await file.read()
    elif sample_filename:
        target_clean = settings.RAW_CLEAN_DIR / sample_filename
        target_prob = settings.RAW_PROB_DIR / sample_filename
        
        if target_clean.exists():
            file_path = target_clean
        elif target_prob.exists():
            file_path = target_prob
        else:
            raise HTTPException(status_code=404, detail=f"Sample file '{sample_filename}' not found in dataset.")
        filename = sample_filename
    else:
        raise HTTPException(status_code=400, detail="Must provide either an uploaded file or sample_filename parameter.")

    try:
        pipeline = RAGPipeline()
        source = file_bytes if file_bytes else file_path
        result = pipeline.analyze_document(source, filename)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"RAG Analysis failed for '{filename}': {str(e)}")
