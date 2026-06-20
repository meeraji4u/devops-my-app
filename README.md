# devops-my-app
# DevOps Sample App

A small Flask web application demonstrating a complete, working CI/CD pipeline — from commit to live deployment — built and run on a self-managed Jenkins server.

## What This Demonstrates

- **Containerization** — Multi-stage-ready Dockerfile with health checks
- **CI/CD Pipeline** — Jenkins declarative pipeline (build → test → deploy → verify)
- **Automated Testing** — Container is built, started, tested against live endpoints, then torn down before deployment
- **Zero-downtime-style Deploy** — Old container is stopped/removed safely before the new one starts
- **Post-deploy Verification** — Pipeline confirms the live endpoint is actually responding before marking the build successful
- **SSH-based Git Authentication** — Jenkins pulls source over SSH, not exposed tokens

## Pipeline Flow

```
Checkout → Build Image → Test → Deploy → Verify Deployment
```

| Stage | What Happens |
|---|---|
| **Checkout** | Jenkins pulls the latest commit via SSH |
| **Build Image** | Builds a tagged Docker image (`:BUILD_NUMBER` and `:latest`) |
| **Test** | Spins up a temporary container, hits `/health` and `/version`, tears it down |
| **Deploy** | Stops/removes the previous running container, starts the new image |
| **Verify Deployment** | Confirms the live deployed container is responding correctly |

If any stage fails, the pipeline stops — a broken build never reaches deployment.

## App Endpoints

| Route | Purpose |
|---|---|
| `GET /` | Returns app metadata (name, author, hostname) |
| `GET /health` | Health check endpoint used by Docker and the pipeline |
| `GET /version` | Returns current app version |

## Tech Stack

- **App**: Python 3.11, Flask
- **Containerization**: Docker
- **CI/CD**: Jenkins (declarative pipeline, Groovy)
- **Source Control**: Git / GitHub (SSH authentication)

## Running Locally

```bash
docker build -t devops-my-app .
docker run -d -p 5000:5000 devops-my-app
curl http://localhost:5000/health
```

## Why I Built This

I manage production infrastructure for a healthcare provider, including a Jenkins-based CI/CD pipeline for hospital systems. This repo is a clean, public demonstration of the same patterns — pipeline structure, automated testing, safe redeploys, and post-deploy verification — without any sensitive infrastructure details.

---
**Author:** Balaji K. — Systems Administrator (DevOps & Infrastructure)
[GitHub](https://github.com/meeraji4u)

## Build Status

This pipeline triggers automatically on every push via GitHub webhook.
