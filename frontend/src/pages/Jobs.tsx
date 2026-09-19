import { useEffect, useState } from "react";
import { Sidebar } from "../components/Sidebar";
import { StatusBadge } from "../components/StatusBadge";
import { listJobs } from "../services/analysisService";
import { Job } from "../types";

export default function Jobs() {
  const [jobs, setJobs] = useState<Job[]>([]);

  useEffect(() => {
    const load = () => listJobs().then(setJobs);
    load();
    const interval = setInterval(load, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8">
        <h1 className="text-2xl font-bold text-white">Jobs</h1>
        <p className="text-slate-400">Fila de processamento: pending, processing, completed, failed, retry.</p>

        <div className="mt-6 space-y-3">
          {jobs.length === 0 && <p className="text-slate-500">Nenhum job encontrado.</p>}
          {jobs.map((job) => (
            <div key={job.id} className="rounded-xl border border-slate-800 bg-slate-900/60 p-5">
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-mono text-sm text-slate-300">{job.job_type}</p>
                  <p className="text-xs text-slate-500">ID: {job.id}</p>
                </div>
                <StatusBadge status={job.status} />
              </div>
              <div className="mt-3 h-2 w-full overflow-hidden rounded-full bg-slate-800">
                <div className="h-full bg-brand-500 transition-all" style={{ width: `${job.progress}%` }} />
              </div>
              <div className="mt-2 flex justify-between text-xs text-slate-500">
                <span>Progresso: {job.progress}%</span>
                <span>Tentativas: {job.attempts}</span>
                {job.duration_seconds != null && <span>Duracao: {job.duration_seconds}s</span>}
              </div>
              {job.error_message && <p className="mt-2 text-xs text-red-400">Erro: {job.error_message}</p>}
              {job.logs && (
                <pre className="mt-3 max-h-32 overflow-y-auto rounded-lg bg-black/40 p-3 text-xs text-slate-400">
                  {job.logs}
                </pre>
              )}
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
