export interface User {
  id: string;
  email: string;
  full_name: string;
  is_active: boolean;
}

export interface TokenPair {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface Project {
  id: string;
  name: string;
  description: string | null;
  source_type: "zip" | "path";
  source_reference: string;
  created_at: string;
  updated_at: string;
}

export interface Analysis {
  id: string;
  project_id: string;
  status: "pending" | "processing" | "completed" | "failed";
  summary: Record<string, any> | null;
  created_at: string;
  updated_at: string;
}

export interface Job {
  id: string;
  analysis_id: string;
  job_type: string;
  status: "pending" | "processing" | "completed" | "failed" | "retry";
  progress: number;
  attempts: number;
  duration_seconds: number | null;
  logs: string | null;
  error_message: string | null;
  created_at: string;
  updated_at: string;
}

export interface ReportItem {
  id: string;
  analysis_id: string;
  format: "html" | "json" | "csv";
  file_path: string;
  created_at: string;
}

export interface DashboardStats {
  total_projects: number;
  total_analyses: number;
  jobs_pending: number;
  jobs_processing: number;
  jobs_completed: number;
  jobs_failed: number;
  total_loc_analyzed: number;
  recent_analyses: { id: string; status: string; created_at: string }[];
}
