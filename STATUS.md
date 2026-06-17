# STATUS.md — Hello Pipeline Project
_Last updated: 2026-06-17_

> **For Claude Code:** Read this file at the start of every session.
> Do not proceed with any task until you have confirmed the current
> milestone statuses and open blockers below.

---

## Current Branch State

| Branch | SHA | Status |
|---|---|---|
| `main` | `b6ddb1c` | Protected. Source of truth for prod. |
| `dev` | `bba52a8` | Protected. Synced with main via back-sync PR #6. Ready for new features. |
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
| M3: First real feature | NOT STARTED | Next session should start here |

---

## What Is In The Repo (as of M1 completion)

```
app/main.py              FastAPI app — GET / returns {"message":"Hello, World!"}
app/__init__.py
tests/test_main.py       pytest tests for / endpoint
Dockerfile               Python 3.12-slim, uvicorn on port 8000
docker-compose.yml       dev / qa / prod profiles
requirements.txt         fastapi, uvicorn, pytest, httpx, ruff
pyproject.toml           pytest rootdir config so `app` module resolves
.github/workflows/ci.yml      lint + test + docker build on PR to dev or main
.github/workflows/promote.yml manual dispatch: tag image for qa or prod
.env.dev / .env.qa / .env.prod  gitignored env files (must be created locally)
```

---

## What Went Wrong This Session (lessons learned)

### Incident: feature branch merged directly to main, bypassing dev

**Root cause:** `feature/initial-scaffold` was opened as a PR and merged into **both** `dev` and `main` separately, instead of following the `feature → dev → main` promotion chain. This left `main` 2 commits ahead of `dev` with divergent history.

**Fix applied:**
- PR #6 (`main → dev`) created and merged to back-sync `dev` forward.
- `dev` and `main` now share identical file content.

**Rule to enforce going forward:**
1. Feature PRs target **`dev` only** — never `main` directly.
2. `main` receives changes **only** via a promotion PR opened from `dev`.
3. Before opening any PR, verify the base branch is correct.

---

## Open Blockers

None.

---

## Next Session Action Items

1. Delete stale branches from GitHub UI (see list above).
2. Cut a new `feature/` branch from `dev` for the next piece of work.
3. Suggested next feature: add a `GET /health` endpoint with test, following the full Definition of Done in CLAUDE.md.
4. Verify CI pipeline runs clean on the new feature PR to `dev`.
5. Practice the full promotion: feature → dev PR, then dev → main PR.
