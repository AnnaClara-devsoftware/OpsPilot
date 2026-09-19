import { api } from "./api";
import { Project } from "../types";

export async function listProjects(): Promise<Project[]> {
  const { data } = await api.get<Project[]>("/projects");
  return data;
}

export async function createProject(payload: {
  name: string;
  description?: string;
  source_type: "zip" | "path";
  source_reference: string;
}): Promise<Project> {
  const { data } = await api.post<Project>("/projects", payload);
  return data;
}

export async function getProject(id: string): Promise<Project> {
  const { data } = await api.get<Project>(`/projects/${id}`);
  return data;
}

export async function deleteProject(id: string): Promise<void> {
  await api.delete(`/projects/${id}`);
}

export async function uploadProjectZip(projectId: string, file: File): Promise<void> {
  const formData = new FormData();
  formData.append("file", file);
  await api.post(`/uploads/${projectId}/zip`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
}
