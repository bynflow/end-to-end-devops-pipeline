# End-to-End DevOps Pipeline

Production-style DevOps portfolio project demonstrating:

* test-driven development with **pytest**
* CI on **GitHub Actions**
* container build and publish to **GitHub Container Registry (GHCR)**
* cluster-centric CD on **Kubernetes** using **Tekton**
* deterministic **promotion** across `dev -> staging -> prod`
* deterministic **rollback** by redeploying a previous immutable image tag
* cloud validation on **Hetzner** with **K3s**

---

## Why this project exists

This project was built to prove end-to-end operational understanding, not just isolated tool familiarity.

The core idea is simple:

1. application changes are tested in CI
2. CI builds and publishes immutable container images
3. CD promotes a chosen image tag across environments
4. production deploys are explicitly gated
5. rollback is performed by redeploying a known previous artifact

That means the same delivery logic is reproducible, auditable, and interview-defendable.

---

## Stack

**Application**

* Python
* Flask
* pytest

**CI**

* GitHub Actions

**Container**

* Docker
* GHCR

**CD / Orchestration**

* Kubernetes
* Tekton Pipelines
* Kustomize

**Validation environments**

* local `kind`
* cloud `Hetzner` + `K3s`

---

## Architecture

```text
Developer -> GitHub -> GitHub Actions -> GHCR (immutable sha-* images)
                                      
Tekton Pipeline -> clone repo -> apply Kustomize overlay -> pin image tag -> verify rollout
                                      
Kubernetes namespaces:
  - proj2-dev
  - proj2-staging
  - proj2-prod
```

### Key design decisions

* **Git stores structure, not image versions**

  * overlays define environment structure only
  * image tag is injected at deploy time by Tekton

* **Immutable artifact promotion**

  * promotion is done by changing the Tekton `tag` parameter
  * not by rebuilding images
  * not by mutating manifests in Git

* **Rollback via artifact redeploy**

  * rollback is performed by redeploying a previous `sha-*` image tag
  * not by relying on `kubectl rollout undo`

* **Production safety**

  * production deploys require explicit approval (`approve_prod=true`)
  * production uses a dedicated ServiceAccount

---

## Repository structure

```text
app/
  app.py

tests/
  test_health.py

k8s/
  base/
    deployment.yaml
    service.yaml
    kustomization.yaml
  overlays/
    dev/
      kustomization.yaml
    staging/
      kustomization.yaml
    prod/
      kustomization.yaml

tekton/
  tasks/
    git-clone.yaml
    deploy.yaml
    guard-prod.yaml
  pipelines/
    deploy.yaml
  pipelineruns/
    deploy-run.yaml
    deploy-prod-run.yaml
  rbac/
  workspaces/
    pvc.yaml

.github/workflows/
  pipeline.yml
```

---

## Delivery model

### 1. CI

On GitHub Actions:

* run test suite
* build Docker image
* push image to GHCR on `main`

Images are published with immutable tags such as:

```text
ghcr.io/bynflow/end-to-end-devops-pipeline:sha-ec5cb7c
```

### 2. CD

Tekton pipeline performs:

1. clone repo
2. select overlay via `environment`
3. apply environment manifests
4. pin the chosen image tag at runtime
5. wait for rollout completion

### 3. Promotion

The same image tag can be promoted across:

* `dev`
* `staging`
* `prod`

without rebuilding the image.

### 4. Rollback

Rollback is executed by rerunning the same pipeline with a previous immutable tag.

---

## Environments

| Environment | Namespace       | Deploy mechanism                     |
| ----------- | --------------- | ------------------------------------ |
| Dev         | `proj2-dev`     | Tekton `deploy-run.yaml`             |
| Staging     | `proj2-staging` | Tekton `deploy-run.yaml`             |
| Prod        | `proj2-prod`    | Tekton `deploy-prod-run.yaml` + gate |

---

## Production gate

Production is protected by two controls:

1. **logical gate**

   * Tekton task `guard-prod`
   * fails unless `approve_prod=true`

2. **RBAC separation**

   * `tekton-deployer` for dev/staging
   * `tekton-deployer-prod` for prod

This keeps production deploys explicit and reduces blast radius.

---

## Validation completed

### Local validation (`kind`)

Validated successfully:

* dev deploy
* promotion to staging
* promotion to prod with gate
* rollback to previous immutable image tag

### Cloud validation (`Hetzner` + `K3s`)

Validated successfully:

* single-node K3s cluster bootstrapped on Hetzner
* Tekton installed on cloud cluster
* same deploy pipeline reused successfully
* `/health` verified in dev, staging, and prod
* environment separation confirmed by image pinning

Example result during cloud validation:

* `dev` pinned to a newer tag
* `staging` and `prod` intentionally held on previous tag

This proved promotion is controlled per environment rather than globally.

---

## Example commands

### Run a dev deploy

```bash
kubectl create -f tekton/pipelineruns/deploy-run.yaml
```

### Promote to staging

Edit `tekton/pipelineruns/deploy-run.yaml`:

* `environment: staging`
* `tag: sha-<target>`

Then:

```bash
kubectl create -f tekton/pipelineruns/deploy-run.yaml
```

### Deploy to prod

Edit `tekton/pipelineruns/deploy-prod-run.yaml`:

* `environment: prod`
* `approve_prod: "true"`
* `tag: sha-<target>`

Then:

```bash
kubectl create -f tekton/pipelineruns/deploy-prod-run.yaml
```

### Rollback

Redeploy a previous immutable tag through the same PipelineRun mechanism.

---

## What this project demonstrates

This repository demonstrates practical understanding of:

* CI vs CD responsibilities
* immutable artifacts
* environment promotion
* cluster-centric deployment design
* RBAC separation
* rollout verification
* rollback strategy
* cloud portability beyond local Kubernetes

---

## Limits / conscious simplifications

This is a portfolio project, not a full production platform. Some simplifications were intentional:

* no secrets manager integration yet
* no ingress/TLS exposure for the application
* no full IaC provisioning for Hetzner resources in this repo
* no observability stack yet (Prometheus/Grafana/Loki)
* Hetzner validation used K3s single-node for controlled cost and simplicity

These are known next-step improvements, not blind spots.

---

## Short project summary

A complete DevOps pipeline project showing how to test, build, publish, deploy, promote, gate, and roll back a containerized application across Kubernetes environments using GitHub Actions, GHCR, Tekton, Kustomize, and real cloud validation on Hetzner.

---

## Author

Carlo Capobianchi (bynflow)
Year: 2026

This project is part of a structured DevOps learning path and professional portfolio.
