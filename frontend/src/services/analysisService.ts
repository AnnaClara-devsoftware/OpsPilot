import { api } from "./api";
import { Analysis, DashboardStats, Job, ReportItem } from "../types";

export async function createAnalysis(projectId: string): Promise<Analysis> {
  const { data } = await api.post<Analysis>("/analyses", { project_id: projectId });
  return data;
}

export async function listAnalyses(): Promise<Analysis[]> {
  const { data } = await api.get<Analysis[]>("/analyses");
  return data;
}

export async function getAnalysis(id: string): Promise<Analysis> {
  const { data } = await api.get<Analysis>(`/analyses/${id}`);
  return data;
}

export async function listJobs(): Promise<Job[]> {
  const { data } = await api.get<Job[]>("/jobs");
  return data;
}

export async function getJob(id: string): Promise<Job> {
  const { data } = await api.get<Job>(`/jobs/${id}`);
  return data;
}

export async function listReports(): Promise<ReportItem[]> {
  const { data } = await api.get<ReportItem[]>("/reports");
  return data;
}

export function reportDownloadUrl(reportId: string): string {
  return `${api.defaults.baseURL}/reports/${reportId}/download`;
}

export async function getDashboardStats(): Promise<DashboardStats> {
  const { data } = await api.get<DashboardStats>("/dashboard/stats");
  return data;
}
