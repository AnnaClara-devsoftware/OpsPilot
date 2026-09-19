const STATUS_STYLES: Record<string, string> = {
  pending: "bg-slate-700 text-slate-200",
  processing: "bg-amber-500/20 text-amber-300",
  completed: "bg-emerald-500/20 text-emerald-300",
  failed: "bg-red-500/20 text-red-300",
  retry: "bg-orange-500/20 text-orange-300",
};

export function StatusBadge({ status }: { status: string }) {
  const style = STATUS_STYLES[status] ?? "bg-slate-700 text-slate-200";
  return <span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${style}`}>{status}</span>;
}
