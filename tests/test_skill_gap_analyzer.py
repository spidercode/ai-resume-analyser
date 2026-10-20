
from app.schemas.skill_gap import (
    RequirementAnalysis,
    SkillGapAnalysis,
)
from app.services.skill_gap_analyzer import validate_evidence


def test_valid_resume_quote_is_preserved():
    resume = (
        "Built REST APIs using C# and .NET. "
        "Designed SQL data pipelines."
    )

    analysis = SkillGapAnalysis(
        overall_summary="Relevant backend experience.",
        strengths=["API development"],
        requirements=[
            RequirementAnalysis(
                requirement="Experience building REST APIs",
                importance="required",
                status="supported",
                evidence=["Built REST APIs using C# and .NET."],
                explanation="The resume explicitly mentions REST APIs.",
            )
        ],
        recommended_next_steps=[],
    )

    result = validate_evidence(analysis, resume)

    assert result.requirements[0].status == "supported"
    assert result.requirements[0].evidence == [
        "Built REST APIs using C# and .NET."
    ]


def test_fabricated_quote_is_rejected():
    resume = "Built REST APIs using C# and .NET."

    analysis = SkillGapAnalysis(
        overall_summary="Some backend experience.",
        strengths=[],
        requirements=[
            RequirementAnalysis(
                requirement="Kubernetes experience",
                importance="preferred",
                status="supported",
                evidence=["Managed Kubernetes clusters for five years."],
                explanation="The candidate has Kubernetes experience.",
            )
        ],
        recommended_next_steps=[],
    )

    result = validate_evidence(analysis, resume)
    item = result.requirements[0]

    assert item.status == "not_demonstrated"
    assert item.evidence == []
    assert "No verifiable" in item.explanation


def test_no_evidence_does_not_claim_candidate_lacks_skill():
    resume = "Built backend APIs using C#."

    analysis = SkillGapAnalysis(
        overall_summary="Backend development experience.",
        strengths=[],
        requirements=[
            RequirementAnalysis(
                requirement="Experience with React",
                importance="unspecified",
                status="not_demonstrated",
                evidence=[],
                explanation="React was not mentioned.",
            )
        ],
        recommended_next_steps=[],
    )

    result = validate_evidence(analysis, resume)

    assert result.requirements[0].status == "not_demonstrated"
    assert result.requirements[0].evidence == []
