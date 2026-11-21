# Auth, input, headers and the one-page threat model (verified 2026-11-21)

## Passwords (NIST SP 800-63B-4, https://pages.nist.gov/800-63-4/sp800-63b.html)

- Minimum 15 characters when the password is the only factor; minimum 8 when it is part of MFA. Allow at least 64.
- No composition rules (no "one capital, one symbol").
- No forced periodic change; force a change on evidence of compromise.
- Check new passwords against a blocklist of breached, dictionary and context words.
- Allow paste and password managers.

## Sessions and flows

- Rotate the session ID at login and privilege change; invalidate server-side on logout.
- Cookies: `HttpOnly`, `Secure`, `SameSite=Lax` (or `Strict` for sensitive apps). Refresh tokens server-side, never in `localStorage`.
- Sign-in, sign-up and reset: rate-limited per account and per IP; one generic message ("if an account exists, we sent an email").
- Reset tokens: single use, short-lived, sent only to the address on file.
- MFA: TOTP or passkeys as candidates; SMS only as a fallback.
- Prefer a maintained auth library or service over custom code. Compare candidates with the ten questions.

## Input and output

- Validate body, query, path and headers on the server against a schema; bound numbers and string lengths.
- Uploads: size limit, type allow-list, content checked against the extension, stored outside the web root, served with `Content-Disposition`.
- Encode output for its context (HTML, attribute, URL, JS). Sanitise user HTML on output.
- No user input in shell strings, `eval`, file paths without normalisation, or SQL built by concatenation.

## Headers

Strict starting CSP; loosen only with a written reason:

```
default-src 'self'; script-src 'self'; style-src 'self'; img-src 'self' data: https:;
connect-src 'self'; frame-ancestors 'none'; form-action 'self'; base-uri 'self'; object-src 'none'
```

CORS: name exact origins for credentialed requests; `*` only for public, credential-free APIs.

## One-page threat model (goes in the plan's security section)

```markdown
### Assets
- (user data, credentials, payments, files, agent tokens)
### Trust boundaries
- browser -> app (untrusted) · app -> DB · app -> third parties · agent -> tools · agent -> web pages
### STRIDE
- Spoofing: ... control: ...
- Tampering: ...
- Repudiation: ...
- Information disclosure: ...
- Denial of service: ...
- Elevation of privilege: ...
### Agent risks (if any agent runs)
- Lethal trifecta legs present: private data [y/n] · untrusted content [y/n] · outbound channel [y/n]
- Leg removed or approval placed at: ...
### Out of scope
- ...
```
