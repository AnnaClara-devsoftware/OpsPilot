import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { StatCard } from "../StatCard";

describe("StatCard", () => {
  it("renders label and value", () => {
    render(<StatCard label="Projetos" value={42} />);
    expect(screen.getByText("Projetos")).toBeInTheDocument();
    expect(screen.getByText("42")).toBeInTheDocument();
  });
});
