# DevOps All Intern Work

> A comprehensive collection of DevOps projects, SAST tooling evaluations, and HashiCorp stack implementations completed during the internship.

**Author:** Soham Mukherjee  
**Date:** April 2026

---

## 📂 Projects Overview

| Project | Description |
|---------|-------------|
| [devops-intern-final-assessment](devops-intern-final-assessment/) | Complete DevOps pipeline with Docker, GitHub Actions, Nomad, and Grafana Loki |
| [infrastructure-sast-standardization](infrastructure-sast-standardization/) | Policy-driven SAST platform for backend services |
| [sast-ci-pipeline-implementation](sast-ci-pipeline-implementation/) | Reusable SAST CI/CD templates and security policies |
| [hashicorp/glynac-hashicorp-stack](hashicorp/glynac-hashicorp-stack/) | 11-node Consul, Nomad, Vault cluster with runbooks |
| [sast-tool-evaluation](sast-tool-evaluation/) | Evaluation of Semgrep, SonarQube, and Trivy |
| [devops-intern-final-assessment/sast-tools-evaluation](devops-intern-final-assessment/sast-tools-evaluation/) | Enterprise SAST tools comparison (SonarQube, Checkmarx, Veracode, etc.) |

---

## 🏗️ Project Summaries

### 1. DevOps Intern Final Assessment
**Tech Stack:** Python, Docker, GitHub Actions, Nomad, Grafana Loki

A complete DevOps pipeline demonstrating:
- Batch-style Python application with logging
- Docker containerization
- GitHub Actions CI/CD
- Nomad job scheduling
- Loki log aggregation with Grafana visualization

**Key Files:**
- `hello.py` — Application entry point
- `Dockerfile` — Container build
- `nomad/hello.nomad` — Nomad job specification
- `monitoring/` — Loki & Grafana configs

---

### 2. Infrastructure-Wide SAST Standardization
**Purpose:** Standardized SAST platform for backend services

Features:
- Reusable GitHub Actions workflows
- Policy-as-code (YAML-based rules)
- Exception handling and auditing
- Onboarding guides for new services

**Supported Backends:** Node.js (primary), Python (planned), Java (planned)

---

### 3. SAST CI Pipeline Implementation
**Purpose:** Framework for embedding security scanning into CI/CD

Contents:
- Reusable CI/CD templates
- Organization-wide security policies
- Onboarding and operational documentation

---

### 4. Glynac HashiCorp Stack
**Architecture:** 11-node cluster

| Component | Nodes | Purpose |
|-----------|-------|---------|
| Consul | 3 | Service mesh, DNS forwarding, mTLS |
| Nomad | 3 | Workload orchestration |
| Vault | 3 | Secrets management |
| Workers | 2 | Job execution |

**Runbooks (DEV tickets):**
- DEV-538: Consul service discovery
- DEV-539: Consul DNS Forwarding
- DEV-540: Consul mTLS best practices
- DEV-541: Nomad node pool
- DEV-542: Nomad security hardening
- DEV-543: Nomad namespace usage
- DEV-544: Troubleshooting guide

**Deployment Options:**
- Local: Vagrant + VirtualBox
- Cloud: Terraform on AWS

---

### 5. SAST Tool Evaluation
**Tools Evaluated:**
- **Semgrep** — Fast, open-source static analysis
- **SonarQube** — Code quality and security
- **Trivy** — Container and filesystem vulnerabilities

---

### 6. SAST Tools Evaluation (Enterprise)
**Enterprise Tools:**
- SonarQube, Checkmarx, Veracode, Fortify, Synopsys Coverity, Klocwork

**Open-Source Tools:**
- Semgrep, CodeQL, Bandit, Brakeman, ESLint Security Plugins

---

## 🚀 Quick Start

### Clone the Repository
```bash
git clone https://github.com/Asterioxer/DevOps-All_Intern_Work.git
cd DevOps-All_Intern_Work
```

### Explore Individual Projects
Each subdirectory is a self-contained project with its own README:
```bash
cd devops-intern-final-assessment
# Follow that project's README for specific instructions
```

### HashiCorp Stack (Local)
```bash
cd hashicorp/glynac-hashicorp-stack
vagrant up
```

---

## 📊 Key Achievements

- ✅ Complete DevOps pipeline from code to observability
- ✅ Policy-driven SAST standardization across infrastructure
- ✅ Enterprise and open-source SAST tool evaluation
- ✅ Production-simulated HashiCorp stack (11-node cluster)
- ✅ Comprehensive runbooks for operational procedures

---

## 🔗 Remote Repository

```
https://github.com/Asterioxer/DevOps-All_Intern_Work.git
```

---

*This summary was generated to provide a high-level overview of all projects contained in this repository.*