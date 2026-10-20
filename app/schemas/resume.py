from pydantic import BaseModel, Field

class WorkExperience(BaseModel):
    job_title: str = Field(description="Job title stated in the resume, or empty string")
    company: str = Field(description="Employer stated in the resume or empty string")
    start_date: str = Field(description="Start date as stated, or empty string")
    end_date: str = Field(description="End date as stated, or empty string")
    responsibilities: list[str] = Field(description="Responsibilities and achievements explicity supported by the resume")


class Education(BaseModel):
    degree: str = Field(description="Degree or qualification, or empty string")
    institution: str = Field(description="School or institution, or empty string")
    graduation_date: str = Field(description="Graduation date as stated, or empty string")

class Project(BaseModel):
    name: str = Field(description="Name of the project stated in resume, or empty string")
    description: str = Field(description="Description supported by the resume")
    technologies: list[str] = Field(
        description="Technologies explicity associated with the project"
    )


class ResumeProfile(BaseModel):
    full_name: str = Field(
        description="Candidate's name as written in the resume or empty string"
    )
    email: str = Field(description="Email stated in the resume, or empty string")
    phone: str = Field(description="Phone stated in the resume, or empty string")
    professional_summary: str = Field(description="Total years only if explicity stated or relaibly derivable; otherwise null")
    skills: list[str] = Field(description="Distinct technical and professional skills supported by the resume")
    work_experience: list[WorkExperience]
    education: list[Education]
    certification: list[str]
    projects: list[Project]