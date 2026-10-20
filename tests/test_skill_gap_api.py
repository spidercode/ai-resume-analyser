from starlette.middleware import P
from app.services.skill_gap_analyzer import analyze_skill_gaps

def test_skill_gap_endpoint_returns_structured_result(client, monkeypatch):
    def fake_analysis(resume_text, job_description):
        return {
            "overall_summary": "Relevant backend experience.",
            "strengths": ["REST API development"],
            "requirements": [
                {
                    "requirement": "REST API experience",
                    "importance": "required",
                    "status": "supported",
                    "evidence": ["Built REST APIs using C# and .NET."],
                    "explanation": "The resume mentions REST APIs.",
                }
            ],
            "recommended_next_steps": [],
        }

    monkeypatch.setattr("app.main.analyze_skill_gaps", fake_analysis)

    response = client.post("/api/v1/resumes/skill-gap-analysis", 
                json={
                    "resume_text": (
                        "Built REST APIs using C# and .NET. "
                        "Developed backend services for enterprise applications."
                    ),
                    "job_description": (
                        "Required experience building REST APIs and scalable "
                        "backend services using modern programming languages."
                    ),
                },
            )

    assert response.status_code == 200

    body = response.json()

    assert body["requirements"][0]["status"] == "supported"
    assert body["requirements"][0]["evidence"] == ["Built REST APIs using C# and .NET."]

def test_skill_gap_endpoint_rejects_short_resume(client):
    response = client.post(
        "/api/v1/resumes/skill-gap-analysis",
        json={
            "resume_text": "Too short",
            "job_description": ("This is a sufficiently long job description for validation."
            ),
        },
    )

    assert response.status_code == 422


def test_quote_matching_ignores_case_and_whitespace():
    from app.services.skill_gap_analyzer import (
        normalize_for_comparison,
    )

    resume = "Built REST APIs using C# and .NET."

    quote = "  BUILT   REST APIs using C# and .NET. "

    assert (normalize_for_comparison(quote) in normalize_for_comparison(resume))