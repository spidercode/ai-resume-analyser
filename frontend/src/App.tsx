
import { useState } from "react";
import {
  analyzeSkillGaps,
  extractResume,
  matchResume,
  parseResume,
  type ResumeProfile,
  type SkillGapAnalysis,
  type MatchResult,
} from "./api";
import "./App.css";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [resumeText, setResumeText] = useState("");
  const [jobDescription, setJobDescription] = useState("");
  const [profile, setProfile] = useState<ResumeProfile | null>(null);
  const [match, setMatch] = useState<MatchResult | null>(null);
  const [analysis, setAnalysis] = useState<SkillGapAnalysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleUpload() {
    if (!file) {
      setError("Choose a PDF or DOCX resume first.");
      return;
    }

    if (!/\.(pdf|docx)$/i.test(file.name)) {
      setError("Only PDF and DOCX files are supported.");
      return;
    }

    if (file.size > 5 * 1024 * 1024) {
      setError("The file must be 5 MB or smaller.");
      return;
    }

    setLoading(true);
    setError("");
    setProfile(null);
    setMatch(null);
    setAnalysis(null);

    try {
      const parsed = await parseResume(file);
      setResumeText(parsed.text);
      const extracted = await extractResume(parsed.text);
      setProfile(extracted);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Resume parsing failed.",
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleAnalyze() {
    if (!resumeText.trim()) {
      setError("Upload and parse a resume first.");
      return;
    }

    if (jobDescription.trim().length < 50) {
      setError("Enter a job description with at least 50 characters.");
      return;
    }

    setLoading(true);
    setError("");
    setMatch(null);
    setAnalysis(null);

    try {
      const [matchResult, gapResult] = await Promise.all([
        matchResume(resumeText, jobDescription),
        analyzeSkillGaps(resumeText, jobDescription),
      ]);

      setMatch(matchResult);
      setAnalysis(gapResult);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Analysis failed.",
      );
    } finally {
      setLoading(false);
    }
  }

  function reset() {
    setFile(null);
    setResumeText("");
    setJobDescription("");
    setProfile(null);
    setMatch(null);
    setAnalysis(null);
    setError("");
  }

  const similarityPercent =
    match === null ? null : Math.round(match.cosine_similarity * 100);

  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="/">
          <span className="brand-mark">R</span>
          <span>Resume<span className="brand-accent">IQ</span></span>
        </a>
        <span className="topbar-label">AI Resume Intelligence</span>
      </header>

      <section className="hero">
        <p className="eyebrow">CAREER INTELLIGENCE, POWERED BY AI</p>
        <h1>Make your next career move <span>with clarity.</span></h1>
        <p className="hero-copy">
          Understand your resume, compare it with a role, and discover
          where your experience aligns with the requirements.
        </p>
      </section>

      <section className="workspace">
        <div className="panel input-panel">
          <div className="section-heading">
            <span className="step-number">01</span>
            <div>
              <h2>Your resume</h2>
              <p>Upload a PDF or DOCX file, up to 5 MB.</p>
            </div>
          </div>

          <label className="upload-area">
            <span className="upload-icon">↑</span>
            <strong>{file ? file.name : "Choose your resume"}</strong>
            <span>PDF or DOCX · Maximum 5 MB</span>
            <input
              type="file"
              accept=".pdf,.docx"
              onChange={(event) => {
                setFile(event.target.files?.[0] ?? null);
                setResumeText("");
                setProfile(null);
                setMatch(null);
                setAnalysis(null);
                setError("");
              }}
            />
          </label>

          <button
            className="button button-secondary full-width"
            onClick={handleUpload}
            disabled={loading || !file}
          >
            {loading ? "Processing…" : "Parse resume"}
          </button>

          {resumeText && (
            <div className="success-note">
              ✓ Resume text extracted successfully
            </div>
          )}

          {profile && (
            <div className="profile-summary">
              <h3>{profile.full_name || "Resume profile"}</h3>
              <p>{profile.professional_summary || "No summary extracted."}</p>
              <div className="skill-list">
                {profile.skills.map((skill) => (
                  <span className="skill-chip" key={skill}>{skill}</span>
                ))}
              </div>
              <p className="muted">
                {profile.work_experience.length} roles ·{" "}
                {profile.education.length} education entries ·{" "}
                {profile.projects.length} projects
              </p>
            </div>
          )}
        </div>

        <div className="panel input-panel">
          <div className="section-heading">
            <span className="step-number">02</span>
            <div>
              <h2>Target role</h2>
              <p>Paste the job description you want to evaluate.</p>
            </div>
          </div>

          <label className="field-label" htmlFor="job-description">
            Job description
          </label>
          <textarea
            id="job-description"
            className="job-input"
            placeholder="Paste the role's responsibilities, required skills, and qualifications here…"
            value={jobDescription}
            onChange={(event) => setJobDescription(event.target.value)}
            rows={12}
          />

          <button
            className="button button-primary full-width"
            onClick={handleAnalyze}
            disabled={loading || !resumeText || jobDescription.trim().length < 50}
          >
            {loading ? "Analyzing…" : "Analyze job match →"}
          </button>

          <button className="reset-button" onClick={reset} disabled={loading}>
            Start a new analysis
          </button>
        </div>
      </section>

      {error && (
        <div className="error-banner" role="alert">
          <strong>Something went wrong</strong>
          <p>{error}</p>
        </div>
      )}

      {loading && (
        <div className="loading-panel" role="status">
          <div className="spinner" />
          <strong>Analyzing your experience</strong>
          <p>AI analysis can take a little time. Please keep this page open.</p>
        </div>
      )}

      {match && analysis && (
        <section className="results">
          <div className="results-heading">
            <div>
              <p className="eyebrow">YOUR RESULTS</p>
              <h2>Here's where you stand.</h2>
            </div>
            <span className="result-label">Analysis complete</span>
          </div>

          <div className="result-grid">
            <article className="panel score-panel">
              <p className="card-label">Semantic similarity</p>
              <div className="score">
                {similarityPercent}<span>%</span>
              </div>
              <p className="muted">
                Text similarity signal, not a hiring probability.
              </p>
            </article>

            <article className="panel summary-panel">
              <p className="card-label">AI summary</p>
              <p>{analysis.overall_summary}</p>
              <h3>Resume strengths</h3>
              <ul>
                {analysis.strengths.map((item, index) => (
                  <li key={`${item}-${index}`}>{item}</li>
                ))}
              </ul>
            </article>
          </div>

          <article className="panel requirements-panel">
            <h2>Requirement-by-requirement analysis</h2>
            <p className="muted">
              “Not demonstrated” means the resume did not provide enough
              evidence; it does not prove the candidate lacks that skill.
            </p>

            {analysis.requirements.map((item, index) => (
              <div className="requirement" key={`${item.requirement}-${index}`}>
                <div className="requirement-heading">
                  <div>
                    <h3>{item.requirement}</h3>
                    <span className="importance">
                      {item.importance}
                    </span>
                  </div>
                  <span className={`status status-${item.status}`}>
                    {item.status.replaceAll("_", " ")}
                  </span>
                </div>

                <p>{item.explanation}</p>

                {item.evidence.length > 0 && (
                  <div className="evidence">
                    <strong>Evidence from your resume</strong>
                    {item.evidence.map((quote, quoteIndex) => (
                      <blockquote key={`${quote}-${quoteIndex}`}>
                        “{quote}”
                      </blockquote>
                    ))}
                  </div>
                )}
              </div>
            ))}
          </article>

          <article className="panel next-steps">
            <h2>Recommended next steps</h2>
            <ul>
              {analysis.recommended_next_steps.map((step, index) => (
                <li key={`${step}-${index}`}>{step}</li>
              ))}
            </ul>
          </article>
        </section>
      )}

      <footer>
        <span>ResumeIQ · AI Resume Analyzer</span>
        <span>Your results are guidance, not a hiring decision.</span>
      </footer>
    </main>
  );
}

export default App;
