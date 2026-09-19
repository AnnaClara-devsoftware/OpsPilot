import { Sidebar } from "../components/Sidebar";
import { useAuth } from "../context/AuthContext";

export default function Settings() {
  const { user } = useAuth();

  return (
    <div className="flex min-h-screen bg-slate-950">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8">
        <h1 className="text-2xl font-bold text-white">Configuracoes</h1>
        <p className="text-slate-400">Informacoes da sua conta.</p>

        <div className="mt-6 max-w-lg rounded-xl border border-slate-800 bg-slate-900/60 p-6">
          <div className="space-y-4">
            <div>
              <p className="text-xs uppercase text-slate-500">Nome</p>
              <p className="text-white">{user?.full_name}</p>
            </div>
            <div>
              <p className="text-xs uppercase text-slate-500">E-mail</p>
              <p className="text-white">{user?.email}</p>
            </div>
            <div>
              <p className="text-xs uppercase text-slate-500">Status</p>
              <p className="text-white">{user?.is_active ? "Ativo" : "Inativo"}</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}
