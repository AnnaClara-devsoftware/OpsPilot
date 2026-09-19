import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { BrowserRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";
import Login from "../Login";
import { AuthProvider } from "../../context/AuthContext";

vi.mock("../../services/authService", () => ({
  login: vi.fn().mockResolvedValue({ access_token: "a", refresh_token: "b", token_type: "bearer" }),
  fetchCurrentUser: vi.fn().mockResolvedValue({ id: "1", email: "a@a.com", full_name: "A", is_active: true }),
  register: vi.fn(),
}));

function renderLogin() {
  return render(
    <BrowserRouter>
      <AuthProvider>
        <Login />
      </AuthProvider>
    </BrowserRouter>
  );
}

describe("Login page", () => {
  it("renders email and password fields", () => {
    renderLogin();
    expect(screen.getByText("E-mail")).toBeInTheDocument();
    expect(screen.getByText("Senha")).toBeInTheDocument();
  });

  it("allows typing into the email field", async () => {
    renderLogin();
    const user = userEvent.setup();
    const emailInputs = screen.getAllByRole("textbox");
    await user.type(emailInputs[0], "test@example.com");
    expect((emailInputs[0] as HTMLInputElement).value).toBe("test@example.com");
  });
});
