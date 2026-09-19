import { createContext, ReactNode, useContext, useEffect, useState } from "react";
import { fetchCurrentUser, login as loginRequest } from "../services/authService";
import { User } from "../types";

interface AuthContextValue {
  user: User | null;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem("opspilot_access_token");
    if (!token) {
      setIsLoading(false);
      return;
    }
    fetchCurrentUser()
      .then(setUser)
      .catch(() => {
        localStorage.removeItem("opspilot_access_token");
        localStorage.removeItem("opspilot_refresh_token");
      })
      .finally(() => setIsLoading(false));
  }, []);

  async function login(email: string, password: string) {
    const tokens = await loginRequest(email, password);
    localStorage.setItem("opspilot_access_token", tokens.access_token);
    localStorage.setItem("opspilot_refresh_token", tokens.refresh_token);
    const currentUser = await fetchCurrentUser();
    setUser(currentUser);
  }

  function logout() {
    localStorage.removeItem("opspilot_access_token");
    localStorage.removeItem("opspilot_refresh_token");
    setUser(null);
  }

  return <AuthContext.Provider value={{ user, isLoading, login, logout }}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth deve ser usado dentro de um AuthProvider");
  return ctx;
}
