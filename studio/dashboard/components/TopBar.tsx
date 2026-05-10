import Image from "next/image";
import Link from "next/link";
import { LiveIndicator } from "./LiveIndicator";
import type { DashboardMode } from "@/lib/projects-types";

interface Props {
  projectName: string;
  workspace: string;
  signedInUser?: string;
  agentOnline?: boolean;
  /** Loader mode (filesystem/http) for the LiveIndicator. */
  loaderMode: DashboardMode;
  /** API base when in http mode. */
  apiBase?: string | null;
  /** Workspace path for SSE subscription scope. */
  workspacePath?: string;
}

export function TopBar({
  projectName,
  workspace,
  signedInUser = "(not signed in)",
  agentOnline = true,
  loaderMode,
  apiBase,
  workspacePath,
}: Props) {
  return (
    <header className="flex h-14 shrink-0 items-center justify-between border-b border-ink-edge bg-ink-stage px-5">
      <div className="flex items-center gap-6">
        <Link href="/" className="flex items-center gap-2">
          <Image
            src="/brand/05-logo-horizontal.png"
            alt="BeQuite"
            width={110}
            height={28}
            className="h-6 w-auto"
            priority
          />
        </Link>
        <span className="text-sm text-silver-dim">/</span>
        <span className="text-sm text-silver-soft">{workspace}</span>
        <span className="text-sm text-silver-dim">/</span>
        <span className="text-sm font-medium text-silver">{projectName}</span>
      </div>

      <div className="flex items-center gap-4">
        <LiveIndicator
          mode={loaderMode}
          apiBase={apiBase ?? undefined}
          workspacePath={workspacePath}
          // Token is read from NEXT_PUBLIC_BEQUITE_API_TOKEN by default at build time
          // when running in HTTP/token mode. Operators set it in .env.local.
          apiToken={
            typeof process !== "undefined"
              ? process.env.NEXT_PUBLIC_BEQUITE_API_TOKEN
              : undefined
          }
        />
        <div className="flex items-center gap-2">
          <span
            aria-hidden
            className={`h-2 w-2 rounded-full ${agentOnline ? "animate-pulse bg-gold" : "bg-silver-dim"}`}
          />
          <span className="font-mono text-xs uppercase tracking-wider text-silver-soft">
            {agentOnline ? "AGENT ONLINE" : "AGENT OFFLINE"}
          </span>
        </div>
        <div className="text-xs text-silver-dim">
          <span className="text-silver-soft">{signedInUser}</span>
        </div>
      </div>
    </header>
  );
}
