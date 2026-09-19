import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from "recharts";
import { Sidebar } from "../components/Sidebar";
import { StatCard } from "../components/StatCard";
import { StatusBadge } from "../components/StatusBadge";
import { createProject, listProjects, uploadProjectZip } from "../services/projectService";
import { createAnalysis, getDashboardStats } from "../services/analysisService";
import { DashboardStats, Project } from "../types";

export default function Dashboard() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);
  const [name, setName] = useState("");
  const [file, setFile] = useState<File | null>(null);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  async function refresh() {
    const [s, p] = await Promise.all([getDashboardStats(), listProjects()]);
    setStats(s);
    setProjects(p);
  }

  useEffect(() => {
    refresh();
  }, []);

  async function handleCreateAndAnalyze(e: React.FormEvent) {
    e.preventDefault();
    if (!file) {
      setMessage("Selecione um arquivo .zip do seu projeto.");
      return;
    }
    setBusy(true);
    setMessage(null);
    try {
      const project = await createProject({
        name,
        source_type: "zip",
        source_reference: "pending-upload",
      });
      await uploadProjectZip(project.id, file);
      await createAnalysis(project.id);
      setMessage("Analise disparada! Acompanhe o progresso na aba Jobs.");
      setName("");
      setFile(null);
      await refresh();
    } catch (err: any) {
      setMessage(err?.response?.data?.detail ?? "Falha ao iniciar a analise.");
    } finally {
      setBusy(false);
    }
  }

  const chartData = stats
    ? [
        { name: "Pendentes", value: stats.jobs_pending },
        { name: "Processando", value: stats.jobs_processing },
        { name: "Concluidos", value: stats.jobs_completed },
        { name: "Falharam", value: stats.jobs_failed },
      ]
    : [];

  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8">
        <h1 className="text-2xl font-bold text-white">Dashboard</h1>
        <p className="text-slate-400">Visao geral das suas analises e jobs.</p>

        {stats && (
          <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            <StatCard label="Projetos" value={stats.total_projects} />
            <StatCard label="Analises" value={stats.total_analyses} />
            <StatCard label="LOC analisadas" value={stats.total_loc_analyzed.toLocaleString("pt-BR")} accent="text-emerald-300" />
            <StatCard label="Jobs falhos" value={stats.jobs_failed} accent="text-red-300" />
          </div>
        )}

        <div className="mt-8 grid gap-6 lg:grid-cols-2">
          <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-6">
            <h2 className="font-semibold text-white">Nova analise</h2>
            <p className="mt-1 text-sm text-slate-400">Envie um .zip do seu projeto para analisar.</p>
            <form onSubmit={handleCreateAndAnalyze} className="mt-4 space-y-3">
              <input
                placeholder="Nome do projeto"
                required
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-white outline-none focus:border-brand-500"
              />
              <input
                type="file"
                accept=".zip"
                onChange={(e) => setFile(e.target.files?.[0] ?? null)}
                className="w-full rounded-lg border border-slate-700 bg-slate-800 px-3 py-2 text-sm text-slate-300"
              />
              <button
                type="submit"
                disabled={busy}
                className="w-full rounded-lg bg-brand-600 py-2.5 font-semibold text-white hover:bg-brand-700 disabled:opacity-60"
              >
                {busy ? "Enviando..." : "Enviar e analisar"}
              </button>
              {message && <p className="text-sm text-slate-300">{message}</p>}
            </form>
          </div>

          <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-6">
            <h2 className="font-semibold text-white">Status dos jobs</h2>
            <div className="mt-4 h-56">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart data={chartData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="name" stroke="#94a3b8" fontSize={12} />
                  <YAxis stroke="#94a3b8" fontSize={12} allowDecimals={false} />
                  <Tooltip contentStyle={{ background: "#0f172a", border: "1px solid #1e293b" }} />
                  <Bar dataKey="value" fill="#3b6bff" radius={[6, 6, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        <div className="mt-8 rounded-xl border border-slate-800 bg-slate-900/60 p-6">
          <h2 className="font-semibold text-white">Analises recentes</h2>
          <div className="mt-4 space-y-2">
            {stats?.recent_analyses.length ? (
              stats.recent_analyses.map((a) => (
                <Link
                  key={a.id}
                  to={`/analysis/${a.id}`}
                  className="flex items-center justify-between rounded-lg bg-slate-800/60 px-4 py-3 hover:bg-slate-800"
                >
                  <span className="font-mono text-sm text-slate-300">{a.id.slice(0, 8)}...</span>
                  <StatusBadge status={a.status} />
                </Link>
              ))
            ) : (
              <p className="text-sm text-slate-500">Nenhuma analise ainda. Envie um projeto para comecar.</p>
            )}
          </div>
        </div>

        <div className="mt-8 rounded-xl border border-slate-800 bg-slate-900/60 p-6">
          <h2 className="font-semibold text-white">Seus projetos</h2>
          <div className="mt-4 space-y-2">
            {projects.length ? (
              projects.map((p) => (
                <div key={p.id} className="flex items-center justify-between rounded-lg bg-slate-800/60 px-4 py-3">
                  <div>
                    <p className="font-medium text-white">{p.name}</p>
                    <p className="text-xs text-slate-500">{p.description || "Sem descricao"}</p>
                  </div>
                  <button
                    onClick={async () => {
                      await createAnalysis(p.id);
                      await refresh();
                    }}
                    className="rounded-lg bg-brand-600/20 px-3 py-1.5 text-sm font-medium text-brand-300 hover:bg-brand-600/30"
                  >
                    Analisar novamente
                  </button>
                </div>
              ))
            ) : (
              <p className="text-sm text-slate-500">Nenhum projeto cadastrado.</p>
            )}
          </div>
        </div>
      </main>
    </div>
  );
}
