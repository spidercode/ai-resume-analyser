from multiprocessing import Value
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.config import settings
from app.schemas.matching import ResumeMatchRequest, ResumeMatchResponse
from app.schemas.skill_gap_request import SkillGapRequest
from app.schemas.skill_gap import SkillGapAnalysis
from app.services.skill_gap_analyzer import (SkillGapAnalyzerError, analyze_skill_gaps)


from app.services.document_parser import (DocumentParsingError, extract_text)
from app.services.embedding_service import EmbeddingError, calculate_similarity
from app.services.resume_extractor import (ResumeExtractionError, extract_resume_profile)



app = FastAPI(
    title="AI Resume Analyzer",
    description="Analyse resumes against Job decription",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.allow_origins],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class JobDescriptionRequest(BaseModel):
    text: str = Field(min_length=20, max_length=30_000)

class ResumeExtractionRequest(BaseModel):
    text: str = Field(min_length=1, max_length=30_000)

@app.get("/health")
def health_check():
    return {"status": "ok"}



@app.post("/api/v1/resumes/parse")
async def parse_resume(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read(5 * 1024 * 1024 + 1)

        text = extract_text(file.filename or "", file_bytes)

        return {
            "filename": file.filename,
            "character_count": len(text),
            "text": text
        }

    except DocumentParsingError as exc: 
        raise HTTPException(status_code=400, detail=str(exc))
    finally:
        await file.close()

@app.post("/api/v1/job-description/parse")
def parse_job_description(request: JobDescriptionRequest):
    text = request.text.strip()

    if len(text) < 20:
        raise HTTPException(status_code=400, detail="Job description must contain atleast 20 characters")

    return {
        "characters_count": len(text),
        "text": text
    }

@app.post("/api/v1/resumes/extract")
def extract_resume(request: ResumeExtractionRequest): 
    try:
        profile = extract_resume_profile(request.text)

        return {
            "profile": profile.model_dump()
        }

    except ValueError as exc: 
        raise HTTPException(status_code=400, details=str(exc)) from exc

    except ResumeExtractionError as exc: 
        raise HTTPException(status_code=502, details=str(exc)) from exc


@app.post("/api/v1/resumes/match", response_model=ResumeMatchResponse)
def match_resume(request: ResumeMatchRequest):
    try:
        similarity = calculate_similarity(request.resume_text, request.job_description)
        return ResumeMatchResponse(cosine_similarity=similarity)

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    except EmbeddingError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@app.post("/api/v1/resumes/skill-gap-analysis", response_model=SkillGapAnalysis)
def skil_gap_analysis(request: SkillGapRequest): 
    try: 
        return analyze_skill_gaps(resume_text=request.resume_text, job_description=request.job_description)
    except Value as exc: 
        raise HTTPException(status_code=400, details=str(exc)) from exc
    except SkillGapAnalyzerError as exc: 
        raise HTTPException(status_code=502, detail=str(exc)) from exc