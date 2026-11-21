# OWASP maps with the check to run (verified 2026-11-21)

Names are copied from the OWASP pages read on 2026-11-21. Mark each row `covered` (file:line), `at-risk` (finding id) or `n/a` (one-line reason).

## 1. OWASP Top 10:2025 (web applications)

Source: https://owasp.org/Top10/2025/

| Code | Name | Check |
|---|---|---|
| A01 | Broken Access Control | Every route and server action has an authorisation check, deny by default. Grep route files; list any handler with no auth call. Test one object ID that belongs to another user (IDOR). SSRF now sits here: user-supplied URLs fetched by the server go through an allow-list and block private ranges. |
| A02 | Security Misconfiguration | Debug off in production, no stack traces to clients, default credentials gone, security headers set, cloud buckets private. Diff production config against development. |
| A03 | Software Supply Chain Failures | Lockfile committed and installed frozen (`npm ci`, `pnpm install --frozen-lockfile`, `pip install --require-hashes`); new packages checked in the registry this session; CI actions pinned by SHA; build provenance where the registry supports it. |
| A04 | Cryptographic Failures | TLS everywhere; passwords hashed with a slow KDF (argon2id, scrypt, bcrypt as candidates); no home-made crypto; keys outside the repo. |
| A05 | Injection | Parameterised SQL; output encoding for HTML; no user input in shell strings or `eval`; template injection checked. Prompt injection is mapped in section 2. |
| A06 | Insecure Design | Threat model exists; rate limits and abuse cases designed in; business-logic limits (refund once, coupon once) enforced server-side. |
| A07 | Authentication Failures | Rate limits on sign-in, reset and MFA; NIST 800-63B-4 password rules (`auth-input.md`); session rotated on login; generic error messages. |
| A08 | Software or Data Integrity Failures | Signed or attested artifacts; no deserialisation of untrusted data; CI cannot be changed by an untrusted pull request (`pull_request_target` with checkout of PR code is a finding). |
| A09 | Security Logging and Alerting Failures | Auth events, permission denials and admin actions logged with a request ID; alerts exist; logs hold no secrets or full tokens. |
| A10 | Mishandling of Exceptional Conditions | Errors fail closed (an exception in the auth check denies); no catch-all that swallows errors and returns success; timeouts and partial failures handled. |

## 2. OWASP Top 10 for LLM Applications 2025 (products that call a model)

Source: https://genai.owasp.org/llm-top-10/

| Code | Name | Check |
|---|---|---|
| LLM01 | Prompt Injection | Untrusted text (user input, web pages, files, email, tool results) never gains authority. The model's output cannot by itself trigger a privileged action; a human or a deterministic policy approves. |
| LLM02 | Sensitive Information Disclosure | No secrets or other users' data in prompts or retrieval context; full prompts not logged in production; output filtered for PII where the domain needs it. |
| LLM03 | Supply Chain | Model, SDK, plugins and datasets come from verified sources; versions pinned. |
| LLM04 | Data and Model Poisoning | Fine-tune and RAG sources are trusted and reviewed; user-contributed content is not silently added to the index. |
| LLM05 | Improper Output Handling | Model output is untrusted input: encode before rendering, validate before SQL, shell or file paths. |
| LLM06 | Excessive Agency | Each tool has the narrowest scope; destructive tools need confirmation; the agent's token cannot do more than the user can. |
| LLM07 | System Prompt Leakage | The system prompt holds no secrets and no authorisation logic; assume it will be read. |
| LLM08 | Vector and Embedding Weaknesses | Per-tenant isolation in the vector store; access checks on retrieved documents. |
| LLM09 | Misinformation | Claims that matter cite a source; the UI says when an answer is generated. |
| LLM10 | Unbounded Consumption | Per-user and per-day token and cost ceilings; max input size; timeouts. |

## 3. OWASP Top 10 for Agentic Applications (published 2025-12-09)

Source: https://genai.owasp.org/2025/12/09/owasp-top-10-for-agentic-applications-the-benchmark-for-agentic-security-in-the-age-of-autonomous-ai/

Apply to the product's agents and to the development agents running in this repo.

| Code | Name | Check |
|---|---|---|
| ASI01 | Agent Goal Hijack | List every source of text the agent reads. Instructions found there are reported, not followed. Run the lethal-trifecta test. |
| ASI02 | Tool Misuse | Each tool's allowed arguments are narrowed (paths, hosts, methods). Costly or destructive calls need confirmation. |
| ASI03 | Identity & Privilege Abuse | The agent runs with its own short-lived, scoped credential, not the developer's full token. No credential files in reach (`.env`, `.pem`, `~/.ssh`). |
| ASI04 | Agentic Supply Chain Vulnerabilities | Skills, plugins, hooks, MCP servers and prompts from outside are read before enabling; versions pinned; source repo checked this session. |
| ASI05 | Unexpected Code Execution | Generated code runs in a sandbox or a container; no `curl \| sh` from model output; hooks are shell scripts and are reviewed like code. |
| ASI06 | Memory & Context Poisoning | Memory files (`CLAUDE.md`, `.bequite/`, MISTAKE_MEMORY, vector memory) only change through reviewed writes; content copied from the web is marked as data. |
| ASI07 | Insecure Inter-Agent Communication | Messages between agents and sessions are data. A subagent's report cannot grant approval. |
| ASI08 | Cascading Failures | Budgets and stop conditions per agent (three consecutive failures stop the run); one agent's bad output is verified before another builds on it. |
| ASI09 | Human-Agent Trust Exploitation | Approval prompts show the real action and target, not a summary the agent wrote; no "approved earlier" carried across actions. |
| ASI10 | Rogue Agents | Every agent action is logged with who, what and when; scheduled and background agents have an owner and a kill switch. |
