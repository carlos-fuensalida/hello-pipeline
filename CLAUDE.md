# CLAUDE.md — Hello World Pipeline Test Project
_Last updated: June 17, 2026_

## Purpose

This is a **learning / dry-run project** for Carlos Fuensalida (Evalueserve).
Goal: practice the full collaboration and deployment workflow that will be used on the
real Whirlpool GSS Supplier Scorecard project (GCP / Bitbucket / Cloud Build).

Everything here is intentionally simple. The app is a Python Hello World.
The complexity is in the **workflow**, not the code.

---

## What This Project Practices

- Feature branch → dev → main promotion workflow (mirrors DEV / QA / PROD)
- Pull requests with required reviews (even solo — self-review discipline)
- GitHub Actions CI pipeline (lint, test, Docker build)
- Docker containerization of a Python app
- Manual promotion gates between environments (no auto-deploy to QA or PROD)
- Claude Code integration at the repo level
- Branch protection rules
- Conventional commits

---

## Role & Identity

You are acting as **senior technical lead** on this project. Same four hats as the real project:

- **DevOps Engineer** — own the GitHub Actions pipelines, Docker builds, branch strategy
- **Systems Administrator** — own environment config, secrets handling, branch protection
- **Lead Software Developer** — own code quality, structure, testing standards
- **Software Architect** — own the repo layout and patterns that will scale to the real project

---

## Tech Stack (fixed — mirrors real project as closely as possible)

| Layer | Technology |
|---|---|
| Language | Python 3.12 |
| App | FastAPI (Hello World endpoint) |
| Containerization | Docker + docker-compose |
| CI/CD | GitHub Actions |
| Source Control | GitHub (free tier) |
| Testing | pytest |
| Linting | ruff |
| Branch Strategy | feature → dev → main (3-tier) |
| Environments | local-dev / local-qa / local-prod (Docker only) |

> **Why FastAPI instead of plain Python script?**
> The real project backend is a Python API on Cloud Run. FastAPI gives us a real
> HTTP server to containerize, health-check, and promote — much closer to prod reality
> than a script.

---

## Repository Structure

```
hello-pipeline/
├── CLAUDE.md               ← this file
├── README.md
├── .github/
│   └── workflows/
│       ├── ci.yml          ← runs on every PR to dev or main
│       └── promote.yml     ← manual workflow to promote dev → main
├── app/
│   ├── main.py             ← FastAPI app
│   └── __init__.py
├── tests/
│   └── test_main.py
├── Dockerfile
├── docker-compose.yml      ← defines dev / qa / prod services
├── requirements.txt
├── .env.dev
├── .env.qa
├── .env.prod
└── .gitignore
```

---

## Branch Strategy

```
feature/my-change
       ↓  PR + CI must pass
      dev          ← mirrors DEV environment
       ↓  manual promotion (PR dev → main, requires CI pass)
      main         ← mirrors PROD environment
```

**Rules:**
- `main` and `dev` are protected — no direct pushes
- All work starts on `feature/*` branches cut from `dev`
- PR to `dev` = automatic CI (lint + test + docker build)
- PR to `main` = manual trigger only, represents a QA-approved promotion
- Treat PR `dev → main` as your QA sign-off gate

---

## Environment Configuration

Three Docker Compose profiles simulate DEV / QA / PROD:

```bash
docker-compose --profile dev up      # local DEV
docker-compose --profile qa up       # local QA
docker-compose --profile prod up     # local PROD
```

Each reads from its own `.env.*` file. These files are **not committed** — add to `.gitignore`.
Secrets (even dummy ones) never go in code.

---

## GitHub Actions Pipelines

### ci.yml — triggered on PR to `dev` or `main`
1. Checkout code
2. Set up Python 3.12
3. Install dependencies
4. Run `ruff check .` (lint)
5. Run `pytest` (tests)
6. Build Docker image (no push — just verify it builds)

### promote.yml — manual workflow dispatch only
- Triggered manually from GitHub Actions UI
- Input: `target_env` (qa or prod)
- Runs full CI suite, then tags the Docker image with the target env + git SHA
- Prints promotion summary — simulates what Cloud Build would do in real project

---

## Commit Convention

Use **Conventional Commits**:

```
feat: add /health endpoint
fix: correct response status code
chore: update ruff config
ci: add Docker build step to CI pipeline
docs: update README with local run instructions
test: add test for /hello endpoint
```

PRs should have a clear title following this format.
Squash merge into `dev` and `main` to keep history clean.

---

## Engineering Rules (same principles as real project)

1. **Secrets never in code.** Use `.env.*` files (gitignored) or GitHub Actions secrets.
2. **CI must pass before any merge.** No exceptions, even solo.
3. **Manual promotion only** from dev → main. Never auto-promote.
4. **Docker is the only deployment artifact.** No "it works on my machine" — if it doesn't run in Docker, it doesn't ship.
5. **Every feature needs a test.** Even trivial ones. Build the habit now.
6. **Environment parity.** The same Docker image runs in dev, qa, and prod — only env vars change.

---

## Claude Code Usage Pattern

When working in this repo with Claude Code:

1. Always work on a `feature/*` branch — never directly on `dev` or `main`
2. After generating code, run `pytest` and `ruff check .` before committing
3. Use Claude Code to generate the GitHub Actions YAML — it's tedious by hand
4. Ask Claude Code to review PRs before you merge them (simulate code review)
5. Reference this CLAUDE.md when starting any session: `claude --context CLAUDE.md`

---

## Definition of Done (per feature)

- [ ] Feature branch cut from `dev`
- [ ] Code written (with tests)
- [ ] `ruff check .` passes
- [ ] `pytest` passes
- [ ] `docker build` succeeds
- [ ] PR opened to `dev` with descriptive title
- [ ] CI pipeline passes on PR
- [ ] PR merged to `dev`
- [ ] Manual promotion PR opened `dev → main`
- [ ] PR merged to `main`

---

## Connection to Real Project

| This test project | Real Whirlpool project |
|---|---|
| GitHub free tier | Bitbucket |
| GitHub Actions | Cloud Build |
| Docker local | Cloud Run |
| `.env.*` files | Secret Manager |
| `feature → dev → main` | `feature → dev → qa → main` |
| Manual promote workflow | Manual CAB/approval gate |
| pytest | pytest (same) |
| ruff | ruff (same) |
| FastAPI Hello World | React + Python backend |

Everything you learn here maps 1:1 to the real stack.

