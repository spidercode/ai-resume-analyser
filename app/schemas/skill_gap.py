from typing import Literal
from pydantic import BaseModel, Field


class RequirementAnalysis(BaseModel): 
    requirement: str = Field(description="A specific requirement from the job description")
    importance: Literal["required", "preferred", "unspecified"]
    status: Literal["supported", "partially_supported", "not_demonstrated"]
    evidence: list[str] = Field(description="Verbatim excerpts from the resume that support this assessment. Empty if no suporting evidence exists.")
    explanation: str = Field(description="Brief explanation grounded in the resume evidence")

class SkillGapAnalysis(BaseModel): 
    overall_summary: str
    strengths: list[str]
    requirements: list[RequirementAnalysis]
    recommended_next_steps: list[str]

