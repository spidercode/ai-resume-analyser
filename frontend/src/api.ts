
const API_BASE =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000";

export interface ResumeProfile {
  full_name: string;
  email: string;
  phone: string;
  professional_summary: string;
  total_years_experience: number | null;
  skills: string[];
  certifications: string[];
  work_experience: {
    job_title: string;
    company: string;
    start_date: string;
    end_date: string;
    responsibilities: string[];
  }[];
  education: {
    degree: string;
    institution: string;
    graduation_date: string;
  }[];
  projects: {
    name: string;
    description: string;
    technologies: string[];
  }[];
}

export interface Requirement {
  requirement: string;
  importance: "required" | "preferred" | "unspecified";
  status:
    | "supported"
    | "partially_supported"
    | "not_demonstrated";
  evidence: string[];
  explanation: string;
}

export interface SkillGapAnalysis {
  overall_summary: string;
  strengths: string[];
  requirements: Requirement[];
  recommended_next_steps: string[];
}

export interface ParseResult {
  text: string;
  filename?: string;
}

export interface MatchResult {
  cosine_similarity: number;
}

async function request<T>(
  path: string,
  init: RequestInit,
): Promise<T> {
  let response: Response;

  try {
    response = await fetch(`${API_BASE}${path}`, init);
  } catch {
    throw new Error(
      "Cannot connect to the API. Check that FastAPI is running.",
    );
  }

  if (!response.ok) {
    const body = await response.json().catch(() => null);
    const detail =
      typeof body?.detail === "string"
        ? body.detail
        : `Request failed (${response.status}).`;

    throw new Error(detail);
  }

  return response.json() as Promise<T>;
}

export async function parseResume(
  file: File,
): Promise<ParseResult> {
  const formData = new FormData();
  formData.append("file", file);

  const result = await request<ParseResult>(
    "/api/v1/resumes/parse",
    { method: "POST", body: formData },
  );

  if (!result.text?.trim()) {
    throw new Error(
      "The parser did not return readable resume text. Check its response format.",
    );
  }

  return result;
}

export async function extractResume(
  text: string,
): Promise<ResumeProfile> {
  const result = await request<{ profile: ResumeProfile }>(
    "/api/v1/resumes/extract",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    },
  );

  return result.profile;
}

export async function matchResume(
  resumeText: string,
  jobDescription: string,
): Promise<MatchResult> {
  return request<MatchResult>("/api/v1/resumes/match", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      resume_text: resumeText,
      job_description: jobDescription,
    }),
  });
}

export async function analyzeSkillGaps(
  resumeText: string,
  jobDescription: string,
): Promise<SkillGapAnalysis> {
  return request<SkillGapAnalysis>(
    "/api/v1/resumes/skill-gap-analysis",
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        resume_text: resumeText,
        job_description: jobDescription,
      }),
    },
  );
}
