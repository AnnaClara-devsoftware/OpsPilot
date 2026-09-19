import { api } from "./api";
import { TokenPair, User } from "../types";

export async function register(email: string, fullName: string, password: string): Promise<User> {
  const { data } = await api.post<User>("/auth/register", { email, full_name: fullName, password });
  return data;
}

export async function login(email: string, password: string): Promise<TokenPair> {
  const { data } = await api.post<TokenPair>("/auth/login", { email, password });
  return data;
}

export async function fetchCurrentUser(): Promise<User> {
  const { data } = await api.get<User>("/auth/me");
  return data;
}
