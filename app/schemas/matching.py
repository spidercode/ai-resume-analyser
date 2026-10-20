from pydantic import BaseModel, Field

class ResumeMatchRequest(BaseModel): 
    resume_text: str = Field(min_length=50, max_length=20_000)
    job_description: str = Field(min_length=50, max_length=20_000)


class ResumeMatchResponse(BaseModel): 
    cosine_similarity: float