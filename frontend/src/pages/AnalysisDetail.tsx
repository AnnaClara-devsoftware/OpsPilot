import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Sidebar } from "../components/Sidebar";
import { StatCard } from "../components/StatCard";
import { StatusBadge } from "../components/StatusBadge";
import { getAnalysis } from "../services/analysisService";
import { Analysis } from "../types";

export default function AnalysisDetail() {
  const { id } = useParams<{ id: string }>();
  const [analysis, setAnalysis] = useState<Analysis | null>(null);

  useEffect(() => {
    if (!id) return;
    const load = () => getAnalysis(id).then(setAnalysis);
    load();
    const interval = setInterval(load, 4000);
    return () => clearInterval(interval);
  }, [id]);

  const summary = analysis?.summary;

  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8">
        <div className="flex items-center gap-3">
          <h1 className="text-2xl font-bold text-white">Analise {id?.slice(0, 8)}</h1>
          {analysis && <StatusBadge status={analysis.status} />}
        </div>

        {!summary && (
          <p className="mt-6 text-slate-400">
            {analysis?.status === "failed" ? "A analise falhou." : "Processando... esta pagina atualiza automaticamente."}
          </p>
        )}

        {summary && (
          <>
            <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-5">
              <StatCard label="Arquivos" value={summary.total_files} />
              <StatCard label="Linhas de codigo" value={summary.total_loc} />
              <StatCard label="TODOs" value={summary.todo_count} />
              <StatCard label="Segredos" value={summary.secret_count} accent="text-red-300" />
              <StatCard label="Complexidade media" value={summary.average_complexity_score} />
            </div>

            <div className="mt-8 grid gap-6 lg:grid-cols-2">
              <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-6">
                <h2 className="font-semibold text-white">Linguagens</h2>
                <table className="mt-4 w-full text-sm">
                  <thead className="text-left text-slate-500">
                    <tr><th className="pb-2">Linguagem</th><th className="pb-2">LOC</th><th className="pb-2">Arquivos</th></tr>
                  </thead>
                  <tbody>
                    {Object.entries(summary.languages || {}).map(([lang, loc]) => (
                      <tr key={lang} className="border-t border-slate-800">
                        <td className="py-2 text-slate-200">{lang}</td>
                        <td className="py-2 text-slate-400">{loc as number}</td>
                        <td className="py-2 text-slate-400">{summary.language_file_counts?.[lang] ?? "-"}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>

              <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-6">
                <h2 className="font-semibold text-white">Dependencias detectadas</h2>
                <ul className="mt-4 space-y-2 text-sm">
                  {Object.entries(summary.dependencies || {}).map(([path, manager]) => (
                    <li key={path} className="flex justify-between rounded-lg bg-slate-800/60 px-3 py-2">
                      <span className="font-mono text-slate-300">{path}</span>
                      <span className="text-slate-500">{manager as string}</span>
                    </li>
                  ))}
                </ul>
              </div>
            </div>

            <div className="mt-6 rounded-xl border border-slate-800 bg-slate-900/60 p-6">
              <h2 className="font-semibold text-white">Arquivos mais complexos</h2>
              <table className="mt-4 w-full text-sm">
                <thead className="text-left text-slate-500">
                  <tr><th className="pb-2">Arquivo</th><th className="pb-2">Ramificacoes</th><th className="pb-2">LOC</th><th className="pb-2">Score</th></tr>
                </thead>
                <tbody>
                  {(summary.most_complex_files || []).map((c: any) => (
                    <tr key={c.file_path} className="border-t border-slate-800">
                      <td className="py-2 font-mono text-slate-300">{c.file_path}</td>
                      <td className="py-2 text-slate-400">{c.branch_points}</td>
                      <td className="py-2 text-slate-400">{c.lines_of_code}</td>
                      <td className="py-2 text-slate-400">{c.complexity_score}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </>
        )}
      </main>
    </div>
  );
}
