import { useEffect, useState } from "react";
import { Sidebar } from "../components/Sidebar";
import { downloadReport, listReports } from "../services/analysisService";
import { ReportItem } from "../types";

const FORMAT_ICON: Record<string, string> = { html: "🌐", json: "🧾", csv: "📊" };

export default function Reports() {
  const [reports, setReports] = useState<ReportItem[]>([]);

  useEffect(() => {
    listReports().then(setReports);
  }, []);

  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8">
        <h1 className="text-2xl font-bold text-white">Relatorios</h1>
        <p className="text-slate-400">Baixe os relatorios gerados pelas suas analises.</p>

        <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {reports.length === 0 && <p className="text-slate-500">Nenhum relatorio gerado ainda.</p>}
          {reports.map((r) => (
            <button
              key={r.id}
              onClick={() => downloadReport(r.id, r.format)}
              className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-900/60 p-5 hover:bg-slate-900 text-left"
            >
              <div>
                <p className="font-semibold uppercase text-white">{r.format}</p>
                <p className="text-xs text-slate-500">{new Date(r.created_at).toLocaleString("pt-BR")}</p>
              </div>
              <span className="text-2xl">{FORMAT_ICON[r.format] ?? "📄"}</span>
            </button>
          ))}
        </div>
      </main>
    </div>
  );
}