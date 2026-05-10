import { ShieldCheck } from "lucide-react";
import type { ReceiptSummary } from "@/lib/projects";

interface Props {
  receipts: ReceiptSummary[];
}

export function ReceiptsList({ receipts }: Props) {
  if (receipts.length === 0) {
    return (
      <div className="rounded-xl border border-ink-edge bg-ink-stage p-5">
        <p className="font-mono text-[11px] uppercase tracking-[0.25em] text-gold">
          Receipts
        </p>
        <p className="mt-2 text-sm text-silver-dim">
          (no receipts yet — they'll appear here as auto-mode runs)
        </p>
      </div>
    );
  }

  return (
    <div className="overflow-hidden rounded-xl border border-ink-edge bg-ink-stage">
      <header className="border-b border-ink-edge bg-ink-velvet/40 px-4 py-2.5">
        <div className="flex items-center justify-between">
          <p className="font-mono text-[11px] uppercase tracking-[0.25em] text-gold">
            Recent receipts ({receipts.length})
          </p>
          <span className="text-[10px] text-silver-dim">chain-hashed · ed25519 signed</span>
        </div>
      </header>
      <ul className="divide-y divide-ink-edge">
        {receipts.map((r) => (
          <li
            key={r.filename}
            className="flex items-center justify-between px-4 py-2.5 transition-colors duration-200 hover:bg-ink-velvet/40"
          >
            <div className="flex min-w-0 items-center gap-3">
              <span
                className={`flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-md border ${
                  r.signed
                    ? "border-gold-deep/50 bg-gold/10 text-gold"
                    : "border-silver-dim/30 bg-ink-velvet text-silver-dim"
                }`}
                title={r.signed ? "ed25519 signed" : "unsigned"}
              >
                <ShieldCheck className="h-3.5 w-3.5" strokeWidth={2.5} />
              </span>
              <div className="min-w-0">
                <p className="font-mono text-xs text-silver">
                  {r.phase} · {r.model}
                </p>
                <p className="font-mono text-[10px] text-silver-dim truncate">
                  {r.filename}
                </p>
              </div>
            </div>
            <div className="text-right">
              <p className="font-mono text-xs text-gold">${r.cost_usd.toFixed(4)}</p>
              <p className="text-[10px] text-silver-dim">{r.timestamp_utc.slice(0, 16).replace("T", " ")}</p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}
