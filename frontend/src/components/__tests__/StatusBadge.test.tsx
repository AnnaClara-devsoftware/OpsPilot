import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { StatusBadge } from "../StatusBadge";

describe("StatusBadge", () => {
  it("renders the given status text", () => {
    render(<StatusBadge status="completed" />);
    expect(screen.getByText("completed")).toBeInTheDocument();
  });

  it("falls back gracefully for unknown statuses", () => {
    render(<StatusBadge status="weird-status" />);
    expect(screen.getByText("weird-status")).toBeInTheDocument();
  });
});
