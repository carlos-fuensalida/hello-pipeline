# STATUS.md — Hello Pipeline Project
_Last updated: 2026-06-17_

> **For Claude Code:** Read this file at the start of every session.
> Do not proceed with any task until you have confirmed the current
> milestone statuses and open blockers below.

---

## Current Branch State

| Branch | SHA | Status |
|---|---|---|
| `main` | `6f19a9b` | Protected. Source of truth for prod. |
| `dev` | `bcc2624` | Protected. In sync with main (PR #13). Ready for new features. |
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
| M2: Branch hygiene | DONE | dev/main synced; merge strategy rules established |
| M3: Code quality fixes | NOT STARTED | Fix list from repo review below — do before M4 |
| M4: First real feature | NOT STARTED | After M3 is clean |

---

## Merge Strategy Rules (CRITICAL)

Wrong merge method = branch divergence on every promotion cycle.

| PR direction | Method | Why |
|---|---|---|
| `feature/* → dev` | **Squash merge** | Collapses feature commits into one clean commit on dev |
| `dev → main` | **Regular merge (merge commit)** | Preserves shared commit SHAs — dev and main stay in sync after promotion |

**Never squash `dev → main`.** Squash creates a brand-new SHA on main that dev doesn't have, causing 1-ahead/2-behind divergence immediately after every promotion.

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

Fix all items in a single `feature/code-quality-fixes` branch before starting new features.

### Fix (must do)

| File | Issue | Fix |
|---|---|---|
| `Dockerfile` | `pyproject.toml` not copied into image — breaks pytest inside container | Add `COPY pyproject.toml .` |
| `Dockerfile` | App runs as root — security finding for Cloud Run | Add non-root `appuser` before CMD |
| `.gitignore` | Plain `.env` (no suffix) not covered | Add `.env` line |

### Improve (do in same PR)

| File | Issue | Fix |
|---|---|---|
| `tests/test_main.py` | `env` key present but value not asserted | `assert data["env"] == "dev"` |
| `ci.yml` | No pip caching — slow CI | Add `actions/cache@v4` for `~/.cache/pip` |
| `promote.yml` | No `permissions:` block | Add `permissions: contents: read` |

### Future (note for real project)

- Split `requirements.txt` into runtime vs dev deps before real project
- Add `healthcheck` in `docker-compose.yml` targeting `GET /health`

---

## What Went Wrong (lessons learned)

### Incident 1 — feature branch merged directly to main, bypassing dev

**Root cause:** `feature/initial-scaffold` merged into both `dev` and `main` separately instead of following `feature → dev → main`. Left `main` 2 commits ahead of `dev`.

**Fix:** PR #6 back-synced `main → dev`.

**Rule:** Feature PRs target `dev` only. `main` receives changes only via promotion PR from `dev`.

### Incident 2 — squash merge on `dev → main` caused repeated divergence

**Root cause:** Using squash merge for `dev → main` creates a new SHA on `main` that `dev` never has. After every promotion cycle, `dev` is immediately 1 ahead / 2 behind `main`.

**Fix:** PR #13 back-synced `main → dev`. Merge strategy rules added to CLAUDE.md and this file.

**Rule:** `dev → main` must always use **regular merge (merge commit)**. See merge strategy table above.

---

## Open Blockers

None.

---

## Next Session Action Items

1. Delete stale branches from GitHub UI: `feature/initial-scaffold`, `claude/compassionate-allen-jksecj`.
2. Cut `feature/code-quality-fixes` from `dev`.
3. Apply all **Fix** and **Improve** items from the M3 review table above.
4. Open PR to `dev` — squash merge — confirm CI passes.
5. Promote `dev → main` via PR — **regular merge (merge commit)**.
6. Verify `dev` and `main` show same SHA after promotion (no divergence).
7. Then cut next feature branch and practice full Definition of Done from CLAUDE.md.
