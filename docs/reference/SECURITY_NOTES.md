# 🔒 Security Notes

**Known tradeoffs in this application, and what a real deployment would do differently**

---

This is not a vulnerability disclosure. Everything here is a deliberate, documented choice made so this app is easy to run locally as a teaching tool, not an oversight someone forgot to fix. If you're using Testbook to practice security testing (see [Stage 4](../../learn/stage_4_performance_security/README.md) and [tests/security/](../../tests/security/README.md)), understanding *why* these choices were made, and what a production system would do instead, is itself part of the lesson.

**The one rule that matters more than any of the specifics below: never expose a running instance of this app to the internet.** Every tradeoff here assumes the app only ever runs on `localhost`, reachable by the person who started it.

---

## JWT authentication has no revocation

**The tradeoff:** [`backend/auth.py`](../../backend/auth.py) issues a bearer token on login that's valid for 24 hours (`ACCESS_TOKEN_EXPIRE_MINUTES`, default `60 * 24`) with no way to invalidate it early. A token issued before a password change or a logout stays valid until it simply expires on its own.

**Why it's acceptable here:** Building real revocation means either a server-side check on every request (a database or cache lookup for every single authenticated call, which defeats the actual point of using a stateless JWT in the first place) or a short-lived-access-token-plus-revocable-refresh-token flow. Either is real, non-trivial infrastructure that would add complexity to nearly every lab in this curriculum without teaching a new testing concept - the tradeoff is documented directly in a comment on `get_current_user()` rather than hidden.

**What production would do differently:** Short-lived access tokens (minutes, not hours) paired with a refresh token that's checked against a server-side store on each use, so it can actually be revoked. Some systems instead maintain a denylist of revoked token IDs, checked on every request - more effort, but avoids a refresh flow.

## Seed accounts are public credentials

**The tradeoff:** `sarah.johnson@testbook.com` / `Sarah2024!` and the other accounts in [`backend/seed.py`](../../backend/seed.py) are committed in this public repository. They are not secrets - anyone who has ever cloned this repo, or looked at it on GitHub, knows them.

**Why it's acceptable here:** A learning app needs accounts a student can log into on their very first run without registering one. Committing them in source is the only way that works without a separate onboarding step.

**What production would do differently:** Never ship default credentials in source at all. If seed/demo accounts are needed for a staging environment, generate random passwords at deploy time and store them outside the repository (a secrets manager, an environment variable injected by the deployment pipeline).

## CORS allows any origin

**The tradeoff:** [`backend/main.py`](../../backend/main.py) sets `allow_origins=["*"]` - any website can call this API from a browser, not just the real Testbook frontend.

**Why it's acceptable here:** In development, "the frontend" could be running on any port a student happens to have free, and there's no sensitive data behind this API worth protecting from a random third-party site in a local learning environment.

**What production would do differently:** Replace the wildcard with the specific origin(s) the real frontend is served from. Note this app does *not* set `allow_credentials=True` alongside the wildcard - that combination would have been worse than either setting alone (see the comment in `main.py`): this app authenticates with a bearer token in the `Authorization` header, never a cookie, so CORS credentials mode was never actually needed, and leaving it enabled would only have added risk with zero benefit.

## File uploads: real but partial validation

**The tradeoff:** [`backend/routers/posts.py`](../../backend/routers/posts.py) and [`backend/routers/users.py`](../../backend/routers/users.py) accept image and video uploads. Both check the file extension server-side (not just in the frontend) and, for image formats, check the actual file bytes against the format's known signature (see [`backend/upload_validation.py`](../../backend/upload_validation.py)) - a file renamed to claim it's a `.png` but containing something else is rejected. Video formats (`.mp4`, `.mov`, `.avi`) are extension-checked only, not signature-checked - their container formats are more complex and less uniformly signatured across variants, and this app never does anything with an uploaded video beyond storing and serving it back unmodified.

Uploads are saved under a server-generated UUID filename (the original filename's path is never used to build the destination path, so a filename like `../../etc/passwd.png` cannot escape the uploads directory - verified directly against a running instance, not just read in the code) and served from `backend/static/uploads/`, which is inside the same web root the rest of the app is served from. A global request-size middleware (`backend/main.py`) caps any POST/PUT/PATCH body at 10MB, uploads included - though it only checks the `Content-Length` header, so a request that omits it (chunked transfer encoding) would not be caught by this specific check.

**Why it's acceptable here:** There's no execution path for an uploaded file - it's served as static bytes via FastAPI's `StaticFiles`, never interpreted or run. The realistic risk this app actually has is a mislabeled file being served back with a misleading content type, which the format-signature check now catches for images.

**What production would do differently:** Store uploads outside the web root (or in a dedicated object store like S3) with access control and expiring signed URLs, rather than a public, permanently-accessible path. Scan uploads for malware. Validate video formats' actual content, not just their extension. Enforce the size limit on the actual request body as it streams in, not only via a spoofable header.

---

## Where these are tested

[`tests/security/`](../../tests/security/README.md) covers authentication, authorization, input validation (SQL injection, XSS), rate limiting, and data exposure. It does not have dedicated tests for the CORS configuration or upload-validation logic described here - `tests/security/README.md`'s own OWASP coverage table already flags A05 (Security Misconfiguration) as only partially covered for exactly this reason (no test verifies HTTP security headers or CORS policy). If you're looking for a real gap to practice writing a test against, that's one.
