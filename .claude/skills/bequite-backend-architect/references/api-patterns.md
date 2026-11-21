# API patterns (verified 2026-11-21)

## Choosing a style (ten questions first; these are starting points)

| Style | Fits when | Costs |
|---|---|---|
| HTTP + JSON with schemas | Public or third-party consumers, CRUD, curl-able debugging | Hand-written client types unless generated from OpenAPI |
| Typed RPC (one language end to end) | One team owns client and server, no public consumers | Harder to open up later |
| GraphQL | Several clients need different shapes of the same graph | Caching, auth per field, query cost limits |
| gRPC | Service-to-service, streaming, polyglot | Browser support needs a proxy |

## Errors: RFC 9457 problem details

```http
HTTP/1.1 422 Unprocessable Content
Content-Type: application/problem+json

{ "type": "https://api.example.com/probs/validation",
  "title": "Request body failed validation",
  "status": 422,
  "detail": "startsAt must be in the future",
  "instance": "/bookings",
  "request_id": "req_01JD7Q8",
  "errors": [{ "field": "startsAt", "code": "past_date" }] }
```

- `status` matches the HTTP status. Clients ignore unknown members, so extensions (`request_id`, `errors`) are safe.
- 401 and 403 bodies never say whether the user exists.
- 5xx bodies hold only the `request_id`; the full context goes to the server log.

## Validation

- Schema per route for body, query, path and the headers you read. Reject unknown fields on writes.
- Path IDs: parse and bound (no unbounded integers, no raw strings into SQL).
- Pagination: cursor (opaque, encodes the sort key) over offset for large or changing lists; cap `limit`.

## Webhooks (receiving)

- Verify the provider's signature on the raw body before parsing; reject stale timestamps.
- Store the event ID with a unique constraint; a repeat returns 200 without re-running (providers retry).
- Acknowledge fast (2xx), do the work in a job.

## Webhooks (sending)

- Sign each payload; include an event ID and a timestamp; retry with backoff; let receivers replay.

## Versioning and change

- Additive changes only within a version: new optional fields, new endpoints.
- Removing or renaming a field is a breaking change: a new version or a deprecation window announced in the changelog (`bequite-release-gate`).
- Contract tests keep client and server on one schema (`bequite-testing-gate`).

## Method semantics (RFC 9110 section 9.2)

Safe: GET, HEAD, OPTIONS, TRACE. Idempotent: the safe methods plus PUT and DELETE. POST and PATCH are neither: retry them only with an idempotency key.

## Idempotency-Key (draft-ietf-httpapi-idempotency-key-header-09, 2026-11-21)

| Case | Response |
|---|---|
| Key missing on an operation that requires it | 400 |
| Key reused with a different payload | 422 |
| Retry while the first request is still processing | 409 |
| True retry after completion | the stored response |

Store: key (unique), payload fingerprint, state, response, created time. Expiry is your published policy (a payment API prunes after at least 24 h). Never put personal data in the key.
