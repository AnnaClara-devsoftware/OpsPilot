import { Link } from "react-router-dom";

const features = [
  { title: "Analise automatica", desc: "Estrutura, linguagens, LOC, dependencias e complexidade em segundos.", icon: "🔍" },
  { title: "Workers assincronos", desc: "Fila com Celery + Redis: pending, processing, completed, failed, retry.", icon: "⚙️" },
  { title: "Seguranca em primeiro lugar", desc: "Deteccao heuristica de segredos expostos e uploads sanitizados.", icon: "🛡️" },
  { title: "Relatorios completos", desc: "Exporte em HTML, JSON ou CSV para compartilhar com o time.", icon: "📄" },
];

export default function Landing() {
  return (
    <div className="min-h-screen overflow-hidden bg-slate-950 text-slate-100">
      <header className="mx-auto flex max-w-6xl items-center justify-between px-6 py-6">
        <div className="flex items-center gap-2 text-xl font-bold">
          <span className="animate-float text-2xl">🚀</span> OpsPilot
        </div>
        <div className="flex gap-3">
          <Link to="/login" className="rounded-lg px-4 py-2 text-sm font-medium text-slate-300 hover:text-white">
            Entrar
          </Link>
          <Link to="/register" className="rounded-lg bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700">
            Criar conta
          </Link>
        </div>
      </header>

      <section className="mx-auto grid max-w-6xl gap-12 px-6 py-16 md:grid-cols-2 md:py-24">
        <div className="animate-fade-in-up">
          <span className="rounded-full bg-brand-500/10 px-3 py-1 text-xs font-semibold text-brand-300">
            Automacao para engenharia de software
          </span>
          <h1 className="mt-5 text-4xl font-extrabold leading-tight md:text-5xl">
            Analise projetos inteiros em <span className="text-brand-400">minutos</span>, nao em dias.
          </h1>
          <p className="mt-5 text-lg text-slate-400">
            Faca upload de um .zip, dispare a analise e receba metricas de linhas de codigo, linguagens,
            dependencias, TODOs e possiveis segredos expostos — tudo processado por workers assincronos.
          </p>
          <div className="mt-8 flex gap-4">
            <Link to="/register" className="rounded-lg bg-brand-600 px-6 py-3 font-semibold text-white shadow-lg shadow-brand-600/30 hover:bg-brand-700">
              Comecar gratis
            </Link>
            <a href="#arquitetura" className="rounded-lg border border-slate-700 px-6 py-3 font-semibold text-slate-200 hover:bg-slate-900">
              Ver arquitetura
            </a>
          </div>
        </div>

        <div className="animate-fade-in-up rounded-2xl border border-slate-800 bg-slate-900/60 p-6 shadow-2xl" style={{ animationDelay: "0.15s" }}>
          <div className="mb-4 flex gap-2">
            <span className="h-3 w-3 rounded-full bg-red-500" />
            <span className="h-3 w-3 rounded-full bg-amber-500" />
            <span className="h-3 w-3 rounded-full bg-emerald-500" />
          </div>
          <div className="space-y-3 text-sm">
            <div className="flex justify-between rounded-lg bg-slate-800/60 px-4 py-3">
              <span className="text-slate-400">Analises executadas</span>
              <span className="font-bold text-brand-300">128</span>
            </div>
            <div className="flex justify-between rounded-lg bg-slate-800/60 px-4 py-3">
              <span className="text-slate-400">Jobs em andamento</span>
              <span className="font-bold text-amber-300">4</span>
            </div>
            <div className="flex justify-between rounded-lg bg-slate-800/60 px-4 py-3">
              <span className="text-slate-400">Linhas de codigo analisadas</span>
              <span className="font-bold text-emerald-300">482.930</span>
            </div>
            <div className="flex justify-between rounded-lg bg-slate-800/60 px-4 py-3">
              <span className="text-slate-400">Segredos detectados</span>
              <span className="font-bold text-red-300">3</span>
            </div>
          </div>
        </div>
      </section>

      <section className="mx-auto max-w-6xl px-6 py-16">
        <h2 className="text-center text-2xl font-bold">O que o OpsPilot faz por voce</h2>
        <div className="mt-10 grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          {features.map((f) => (
            <div key={f.title} className="rounded-xl border border-slate-800 bg-slate-900/50 p-6">
              <div className="text-3xl">{f.icon}</div>
              <h3 className="mt-3 font-semibold text-white">{f.title}</h3>
              <p className="mt-2 text-sm text-slate-400">{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      <section id="arquitetura" className="mx-auto max-w-6xl px-6 py-16">
        <h2 className="text-center text-2xl font-bold">Arquitetura</h2>
        <p className="mx-auto mt-3 max-w-2xl text-center text-slate-400">
          FastAPI + PostgreSQL para a API, Celery + Redis para processamento assincrono, e um frontend em
          React, TypeScript e Tailwind consumindo tudo via REST.
        </p>
        <pre className="mx-auto mt-8 max-w-3xl overflow-x-auto rounded-xl border border-slate-800 bg-slate-900/70 p-6 text-xs text-slate-300">
{`Browser (React/Vite) --> API (FastAPI) --> PostgreSQL (Neon)
                                |
                                v
                        Fila (Redis/Upstash)
                                |
                                v
                      Workers (Celery) --> Relatorios HTML/JSON/CSV`}
        </pre>
      </section>

      <footer className="border-t border-slate-800 py-8 text-center text-sm text-slate-500">
        OpsPilot &copy; {new Date().getFullYear()} — projeto de portfolio em engenharia de software.
      </footer>
    </div>
  );
}
