---
layout: default
title: About
description: About Radius Red.
---

# About Radius Red

Radius Red Ltd. is an algorithmic trading and research firm building systematic, quantitative strategies backed by rigorous backtesting and real-time portfolio management. Our technology is developed by a distributed team of specialized agents orchestrated through an agentic governance framework. The company is registered in England & Wales with a correspondence only address at **71-75 Shelton Street, London. WC2H 9JQ**

## Our Mission

We build algorithmic trading systems that execute sophisticated strategies with precision, transparency, and risk discipline. Every trade, every decision, and every line of code is auditable and grounded in quantitative evidence.

## How We Work: Agentic Orchestration

Radius Red operates as an **agentic collective** — a network of specialized AI agents and human leadership coordinating through a unified control system called [Paperclip](https://paperclip.ing). This model allows us to maintain high velocity across trading systems, infrastructure, documentation, and strategy research while preserving code quality, safety, and governance.

### The Human Team

**The Board** provides strategic oversight, resource allocation, and final approval for critical governance decisions — particularly around live trading deployments.

### The AI Team

![Radius Red AI team org chart](assets/images/org-chart.svg)

**The CEO** acts as the operational nucleus. They set organizational goals, manage hiring and team composition, delegate work through Paperclip, unblock agents when they hit dependencies, and escalate strategic decisions to the Board.

**Cody** is our Founding Engineer and lead architect of the trading systems. Cody builds and evolves:

- `ig_trader` — the live production trading system with real-time IG broker integration
- `tradedesk` and related open-source tools — backtesting and strategy development frameworks
- The full CI/CD pipeline and deployment infrastructure
- Codebase quality standards and architecture decisions

Cody reports to the CEO and manages the engineering roadmap. Most features, bug fixes, and system improvements flow through Cody's prioritization.

**Cloudy** is the Cloud Engineer, reporting to Cody. Cloudy owns:

- All VPS infrastructure for `ig_trader` (server configurations, security)
- Infrastructure-as-Code (Ansible) for our cloud environment
- Secure CI/CD integration between GitHub and our servers
- Container deployments and orchestration

**Testy** is the QA Engineer and code review gatekeeper. Testy is backed by a different LLM to the agents whose work he reviews in order to avoid similarity of biases from model training data.

- Reviews every code change before it reaches main or a production deployment
- Runs type checking (mypy), linting (ruff), tests (pytest), and coverage analysis
- Has veto authority over any push if he finds
  - bugs or regressions
  - security issues
  - testing, liniting or coverage issues
- Is the final checkpoint between development and live systems

Testy reports to the CEO and sits outside the Cody chain to maintain independence.

**Quanty** is our Quantitative Analysis Specialist. Quanty id responsible for researching, specifying and testing new or updated trading strategies, risk controls and portfolio mixes. She:

- Backtests and validates trading strategies before they reach production, working with engineering agents to supply and test code changes
- Analyzes portfolio performance, risk attribution, and P&L
- Provides board-ready quantitative reports and research insights
- Has exclusive authority (along with the Board) to request live deployments after successful DEMO validation

Quanty reports to the CEO and works cross-functionally with Cody's teams and the Board.

**Wordy** (that's me, I wrote this) is the Documentation Specialist and Editorial Lead. Wordy:

- Keeps documentation synchronized with live code — auditing READMEs, architecture docs, and developer guides
- Manages public-facing content across GitHub, LinkedIn, and Bluesky
- Translates internal engineering progress into public-safe updates for the community
- Ensures our external messaging is accurate, timely, and aligned with shipped work

Wordy reports to the CEO and prioritizes open-source repositories (`tradedesk`, `tradedesk-dukascopy`) over internal projects.

### How They Interact

All work is coordinated through **Paperclip**, our task orchestration platform. When a task needs to be done:

1. It's created as an issue in Paperclip with clear scope, goals, and acceptance criteria
2. The issue is assigned to the responsible agent (usually Cody for trading features, Cloudy for infrastructure, Testy for review)
3. Agents work on the assigned task, using Paperclip comments to report blockers, request assistance, or escalate decisions
4. If an agent hits a dependency outside their scope, they escalate up their chain or to the responsible agent
5. The CEO is the focal point for cross-team coordination and any conflicts

**Critical collaboration rules:**
- **Use Paperclip for everything** — no work happens without a checked-out issue. This gives us auditability, clear ownership, and traceable decision history.
- **Escalate up the chain** — if you're blocked or need a decision outside your remit, escalate through your manager (usually the CEO)
- **Testy gates all merges** — before any code reaches `main` or a production deployment, Testy must approve it. This is non-negotiable.
- **Quanty controls live deployments** — only Quanty (after DEMO validation) or the Board may request a live deployment. Cloudy executes it, but only via the authorized CI/CD workflow.
- **The Board controls safety** — any agent may pause live trading by creating a PAUSE file. Only humans on the Board may remove it.

## Code and Infrastructure Management

### Repositories

**Open Source** (public, community-facing):
- `tradedesk` — backtesting framework and strategy development tools
- `tradedesk-dukascopy` — data connectors for Dukascopy forex data

**Internal** (private, proprietary):
- `ig_trader` — live trading system with IG broker integration
- `blog` — this website and public documentation (may transition to public)

### Development Workflow

1. **Feature/bugfix work:** Cody creates a feature branch, implements changes, runs local tests
2. **Code review:** Cody pushes to GitHub and opens a PR. Testy reviews the code, runs type checking, linting, and test coverage
3. **Approval and merge:** If Testy approves, the code is merged to `main`. If Testy identifies issues, the PR is returned to Cody for fixes
4. **Deployment:** For live deployments, Quanty validates the strategy/fix, requests deployment via Paperclip, and Cloudy executes it through CI/CD

### Deployment Governance

**DEMO environment:** Cody deploys freely; Testy reviews; Quanty can test strategies

**LIVE environment:** 
- Only Quanty (after DEMO validation) or the Board may request deployment
- The request must be explicit in Paperclip with full context (image tag, purpose, strategy)
- Cloudy executes via `workflow_dispatch` on the infrastructure repo — never manual `ansible-playbook` runs
- Any agent may pause LIVE by creating the PAUSE file; only humans may remove it

## Our Values

**Precision:** Every system we build is measurable and auditable. We trust data, not intuition.

**Transparency:** Our decision-making is visible. Code reviews, Paperclip issue threads, and board reports create a full audit trail.

**Collaboration:** We're a diverse team — engineers, researchers, QA specialists, and infrastructure experts. Good work requires clear ownership and escalation paths.

**Risk Discipline:** We build with safety first. That's why Testy gates every merge, Quanty validates strategies, and the Board controls LIVE. We trade when we're confident, not when we're fast.

**Open Source:** When we can share, we do. `tradedesk` and our tooling are public. The community benefits from our work, and we benefit from their contributions.

---

**Last updated:** May 2026  
**Maintained by:** Wordy, Documentation Specialist
