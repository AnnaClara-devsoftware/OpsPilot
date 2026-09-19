import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

const links = [
  { to: "/dashboard", label: "Dashboard", icon: "📊" },
  { to: "/jobs", label: "Jobs", icon: "⚙️" },
  { to: "/reports", label: "Relatorios", icon: "📄" },
  { to: "/settings", label: "Configuracoes", icon: "🔧" },
];

export function Sidebar() {
  const { user, logout } = useAuth();

  return (
    <aside className="flex h-screen w-64 flex-col justify-between border-r border-slate-800 bg-slate-900/50 p-4">
      <div>
        <div className="mb-8 flex items-center gap-2 px-2">
          <span className="text-2xl">🚀</span>
          <span className="text-lg font-bold text-white">OpsPilot</span>
        </div>
        <nav className="space-y-1">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-2 text-sm font-medium transition-colors ${
                  isActive ? "bg-brand-600 text-white" : "text-slate-400 hover:bg-slate-800 hover:text-white"
                }`
              }
            >
              <span>{link.icon}</span>
              {link.label}
            </NavLink>
          ))}
        </nav>
      </div>
      <div className="border-t border-slate-800 pt-4">
        <p className="truncate px-2 text-sm text-slate-300">{user?.full_name}</p>
        <p className="truncate px-2 text-xs text-slate-500">{user?.email}</p>
        <button
          onClick={logout}
          className="mt-3 w-full rounded-lg bg-slate-800 px-3 py-2 text-sm font-medium text-slate-200 hover:bg-slate-700"
        >
          Sair
        </button>
      </div>
    </aside>
  );
}
