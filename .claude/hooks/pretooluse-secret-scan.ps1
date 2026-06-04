# BeQuite hook — PreToolUse (matcher: Write|Edit) — block secret-shaped strings (PowerShell).
# OPT-IN. Review before enabling. See docs/architecture/CLAUDE_CODE_HOOKS_STRATEGY.md
# Only HIGH-CONFIDENCE patterns block (near-zero false positives).
$raw = [Console]::In.ReadToEnd()
try { $j = $raw | ConvertFrom-Json -ErrorAction Stop } catch { exit 0 }
$hay = $null; $file = 'the edit'
try { if ($j.tool_input.content)    { $hay = $j.tool_input.content } }    catch {}
if (-not $hay) { try { if ($j.tool_input.new_string) { $hay = $j.tool_input.new_string } } catch {} }
if (-not $hay) { $hay = $raw }
try { if ($j.tool_input.file_path)  { $file = $j.tool_input.file_path } } catch {}

function Block($what) {
  [Console]::Error.WriteLine("BeQuite hook blocked a secret-shaped string in $($file): $what")
  [Console]::Error.WriteLine("Move it to .env / an OS keychain / a secret manager, gitignore the file, and use a placeholder in code.")
  exit 2
}

if ($hay -cmatch 'AKIA[0-9A-Z]{16}')                       { Block 'AWS access key id' }
if ($hay -match  'gh[pousr]_[A-Za-z0-9_]{36,}')            { Block 'GitHub token' }
if ($hay -match  'sk-ant-[A-Za-z0-9_-]{20,}')              { Block 'Anthropic API key' }
if ($hay -cmatch 'sk-[A-Za-z0-9]{32,}')                    { Block 'OpenAI-style API key' }
if ($hay -match  '-----BEGIN [A-Z ]*PRIVATE KEY-----')     { Block 'private key block' }
if ($hay -match  'xox[baprs]-[A-Za-z0-9-]{10,}')           { Block 'Slack token' }

# OPTIONAL (false-positive prone — enable per project):
# if ($hay -match '(?i)(api|secret|password|token)[a-z_]*\s*[:=]\s*.{0,2}[A-Za-z0-9+/_-]{20,}') { Block 'hardcoded credential assignment' }
exit 0
