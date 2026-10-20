import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import App from "./App";

describe("Resume Analyzer dashboard", () => {
  it("renders the resume upload and job description areas", () => {
    render(<App />);

    expect(
      screen.getByRole("heading", { name: /your resume/i }),
    ).toBeInTheDocument();

    expect(
      screen.getByRole("heading", { name: /target role/i }),
    ).toBeInTheDocument();

    expect(
      screen.getByLabelText(/job description/i),
    ).toBeInTheDocument();
  });
});