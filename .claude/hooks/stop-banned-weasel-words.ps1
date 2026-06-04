# BeQuite hook — Stop — block a completion claim that uses banned weasel words (PowerShell).
# OPT-IN and the MOST EXPERIMENTAL of the three (reads the transcript; fails soft on uncertainty).
# Review before enabling. See docs/architecture/CLAUDE_CODE_HOOKS_STRATEGY.md
# Protocol: exit 2 = block turn-end (forces Claude to keep working). MUST exit 0 when
# stop_hook_active is true (avoid infinite loop). Claude Code force-overrides after 8 blocks.
$raw = [Console]::In.ReadToEnd()
try { $j = $raw | ConvertFrom-Json -ErrorAction Stop } catch { exit 0 }
if ($j.stop_hook_active -eq $true) { exit 0 }
$t = $null; try { $t = $j.transcript_path } catch {}
if (-not $t -or -not (Test-Path -LiteralPath $t)) { exit 0 }

$last = ''
try {
  $lines = Get-Content -LiteralPath $t -ErrorAction Stop
  for ($i = $lines.Count - 1; $i -ge 0; $i--) {
    try { $o = $lines[$i] | ConvertFrom-Json -ErrorAction Stop } catch { continue }
    if ($o.type -eq 'assistant' -and $o.message -and $o.message.content) {
      foreach ($c in $o.message.content) { if ($c.type -eq 'text') { $last += "`n" + $c.text } }
      if ($last) { break }
    }
  }
} catch { exit 0 }
if (-not $last) { exit 0 }

if ($last -match '(?i)\b(should (work|be fixed|pass|be fine)|probably (works|correct|fixed|fine)|seems to (work|be fixed)|appears to (work|be fixed)|i think it works|i believe it works|might (work|fix)|hopefully (fixed|works|that)|in (theory|principle))\b') {
  [Console]::Error.WriteLine("BeQuite Stop hook: this response makes a completion claim with a banned weasel word.")
  [Console]::Error.WriteLine("Replace it with concrete evidence (the command run + exit code + output), or state an explicit 'UNVERIFIED:' / 'I don't know' - then finish.")
  exit 2
}
exit 0
