import numpy as np
from openai import OpenAI, APIError


from app.config import settings

client = OpenAI(
    api_key=settings.openai_api_key,
    timeout=30.0,
    max_retries=2
)

class EmbeddingError(Exception): 
    """Raised when text embeddings cannot be generated"""


def generate_embedding(text: str) -> list[float]:
    if not text or not text.strip():
        raise ValueError("Text cannot be empty")

    if len(text) > 20_000:
        raise ValueError("Text exceeds 20,000 character limit")

    try:
        response = client.embeddings.create(
            model=settings.openai_embedding_model,
            input=text
        )

        return response.data[0].embedding

    except APIError as exc:
        raise EmbeddingError(
            "The embedding service is temporarily unavailable"
        ) from exc

def calculate_similarity(resume_text: str, job_description: str) -> float:
    resume_vector = np.array(generate_embedding(resume_text), dtype=np.float32) 
    job_vector = np.array(generate_embedding(job_description), dtype=np.float32)

    denominator = (np.linalg.norm(resume_vector) * np.linalg.norm(job_vector))

    if denominator == 0: 
        raise ValueError("Invalid Resume Text or Job Description provided")

    similarity = np.dot(resume_vector, job_vector) / denominator

    return round(float(similarity), 4)