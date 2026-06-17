# STATUS.md — Hello Pipeline Project
_Last updated: 2026-06-17_

> **For Claude Code:** Read this file at the start of every session.
> Do not proceed with any task until you have confirmed the current
> milestone statuses and open blockers below.

---

## Current Branch State

| Branch | SHA | Status |
|---|---|---|
| `main` | `23fa427` | Protected. Source of truth for prod. |
| `dev` | `23fa427` | Protected. In sync with main. Ready for new features. |
| `feature/initial-scaffold` | `bd08f5b` | **STALE — delete from GitHub UI** |
| `claude/compassionate-allen-jksecj` | `3023fd3` | **STALE — delete from GitHub UI** |
| `claude/admiring-volta-rbrx3i` | — | Current Claude session branch. Delete after session. |

### Pending manual cleanup (GitHub UI → Branches)
- [ ] Delete `feature/initial-scaffold`
- [ ] Delete `claude/compassionate-allen-jksecj`

---

## Milestone Status

| Milestone | Status | Notes |
|---|---|---|
| M1: Repo scaffold | DONE | FastAPI app, Dockerfile, CI workflow, pytest, ruff all in place |
| M2: Branch hygiene | DONE | dev/main synced via PR #6 after history divergence incident |
| M3: Code quality fixes | NOT STARTED | Fix list from repo review below — do before M4 |
| M4: First real feature | NOT STARTED | After M3 is clean |

---

## What Is In The Repo (as of M2 completion)

```
app/main.py              FastAPI app — GET /hello and GET /health
app/__init__.py
tests/test_main.py       pytest tests for both endpoints
Dockerfile               Python 3.12-slim, uvicorn on port 8080
docker-compose.yml       dev / qa / prod profiles (ports 8080/8081/8082)
requirements.txt         fastapi, uvicorn, pytest, httpx, ruff (all pinned)
pyproject.toml           pytest rootdir config so `app` module resolves
.github/workflows/ci.yml      lint + test + docker build on PR to dev or main
.github/workflows/promote.yml manual dispatch: tag image for qa or prod
.env.dev / .env.qa / .env.prod  gitignored env files (must be created locally)
```

---

## Repo Review Findings (2026-06-17) — Fix in M3

These came out of a full repo review. Fix all of them in a single `feature/code-quality-fixes` branch before starting new features.

### Fix (must do)

| File | Issue | Fix |
|---|---|---|
| `Dockerfile` | `pyproject.toml` not copied into image — breaks pytest inside container | Add `COPY pyproject.toml .` |
| `Dockerfile` | App runs as root — security finding for Cloud Run | Add `RUN adduser --disabled-password --gecos "" appuser` + `USER appuser` before CMD |
| `.gitignore` | Plain `.env` (no suffix) not covered — would be committed accidentally | Add `.env` line |

### Improve (do in same PR)

| File | Issue | Fix |
|---|---|---|
| `tests/test_main.py` | `env` key presence checked but value not asserted | `assert data["env"] == "dev"` |
| `ci.yml` | No pip dependency caching — slow CI | Add `actions/cache@v4` step for `~/.cache/pip` keyed on `requirements.txt` hash |
| `promote.yml` | No `permissions:` block — broad default GitHub Actions permissions | Add `permissions: contents: read` |

### Future (note for real project, not urgent here)

- `requirements.txt`: split into `requirements.txt` (runtime) and `requirements-dev.txt` (ruff, pytest, httpx) before real project
- `docker-compose.yml`: add `healthcheck` targeting `GET /health` endpoint

---

## What Went Wrong (lessons learned)

### Incident: feature branch merged directly to main, bypassing dev

**Root cause:** `feature/initial-scaffold` was merged into **both** `dev` and `main` separately, violating the `feature → dev → main` promotion chain. Left `main` 2 commits ahead of `dev` with divergent history.

**Fix applied:** PR #6 (`main → dev`) back-synced `dev` forward. Both branches now share identical content.

**Rules to enforce going forward:**
1. Feature PRs target **`dev` only** — never `main` directly.
2. `main` receives changes **only** via a promotion PR from `dev`.
3. Before opening any PR, verify the base branch is correct.

---

## Open Blockers

None.

---

## Next Session Action Items

1. Delete stale branches from GitHub UI: `feature/initial-scaffold`, `claude/compassionate-allen-jksecj`.
2. Cut `feature/code-quality-fixes` from `dev`.
3. Apply all **Fix** and **Improve** items from the review table above.
4. Open PR to `dev`, confirm CI passes, merge.
5. Promote `dev → main` via PR.
6. Then cut `feature/health-endpoint` (or next real feature) and practice the full Definition of Done flow from CLAUDE.md.
