# BeQuite hook — PreToolUse — block destructive operations (PowerShell).
# OPT-IN. Review before enabling. See docs/architecture/CLAUDE_CODE_HOOKS_STRATEGY.md
# Protocol: stdin JSON; exit 2 = BLOCK (stderr -> Claude); exit 0 = allow. (exit 1 does NOT block.)
$raw = [Console]::In.ReadToEnd()
try { $j = $raw | ConvertFrom-Json -ErrorAction Stop } catch { exit 0 }
$hay = $null
try { if ($j.tool_input.command)   { $hay = $j.tool_input.command } }  catch {}
if (-not $hay) { try { if ($j.tool_input.file_path) { $hay = $j.tool_input.file_path } } catch {} }
if (-not $hay) { $hay = $raw }

function Block($what) {
  [Console]::Error.WriteLine("BeQuite hook blocked a destructive operation: $what")
  [Console]::Error.WriteLine("This is a hard human gate (per /bq-auto). Re-run only with explicit user confirmation, or choose a safer alternative.")
  exit 2
}

# PowerShell -match is case-insensitive by default.
if (($hay -match 'rm\s+-[a-z]*r[a-z]*f') -or ($hay -match 'rm\s+-[a-z]*f[a-z]*r') -or ($hay -match 'rm\s+-r[a-z]*\s+-f') -or ($hay -match 'rm\s+--recursive.*--force')) {
  if ($hay -notmatch '/tmp/|node_modules') { Block 'recursive force-delete (rm -rf) on tracked files' }
}
if ($hay -match 'rm\s+-[a-z]*[rf].*\.(bequite|claude)\b')                                  { Block 'deletion of .bequite/ or .claude/ (project memory)' }
if (($hay -match 'git\s+push\s+.*(--force|\s-f(\s|$))') -and ($hay -match '\b(main|master|prod|production|release)\b')) { Block 'git push --force to a protected branch' }
if ($hay -match 'git\s+reset\s+--hard')                                                     { Block 'git reset --hard (discards work)' }
if ($hay -match 'terraform\s+destroy')                                                      { Block 'terraform destroy' }
if ($hay -match 'DROP\s+(TABLE|DATABASE|SCHEMA)\b')                                          { Block 'SQL DROP TABLE/DATABASE/SCHEMA' }
exit 0
