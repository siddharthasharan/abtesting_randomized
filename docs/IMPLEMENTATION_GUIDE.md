# Building a CoderPad-Equivalent for Python + SQL with GPT-Based Senior/Principal DS Evaluation

## 1) Goal
Build an interview platform that:
- lets candidates solve **Python** and **SQL** tasks,
- executes code safely and reproducibly,
- compares solutions against a structured rubric aligned to a **Senior/Principal Data Scientist** bar,
- uses GPT models to score reasoning quality (not just final output), and
- gives interviewers transparent evidence behind each score.

---

## 2) Product Scope (MVP → V1)

### MVP (first 6–10 weeks)
- Candidate workspace with:
  - Python editor + execution
  - SQL editor + execution on sandbox DB
- Question library (Python + SQL)
- Auto-check baseline:
  - correctness/unit tests for Python
  - result-set checks for SQL
- GPT evaluation for open-ended quality dimensions
- Interviewer dashboard with:
  - final score
  - rubric breakdown
  - strengths/risks summary

### V1 expansion
- Live collaborative interview mode
- Anti-cheat signals (copy-paste bursts, tab switching heuristics)
- Model calibration dashboard by role/level/domain
- Versioned rubrics by company/team

---

## 3) High-Level Architecture

## Frontend
- Web app (React/Next.js recommended)
- Monaco editor (Python + SQL syntax)
- Split panes: prompt, code editor(s), output, schema docs

## Backend API
- Auth, session management, interview orchestration
- Submission pipeline to execution/evaluation services
- Event logging for replay + analytics

## Execution Layer
- **Python runner**: containerized execution with CPU/memory/time limits
- **SQL runner**: isolated ephemeral DB instance (e.g., Postgres per session)
- Deterministic seeds/data snapshots for reproducibility

## Evaluation Layer
- Deterministic checks first (tests/assertions)
- GPT rubric scoring second (reasoning, maintainability, trade-offs)
- Score fusion logic (weighted aggregate + confidence)

## Storage
- OLTP DB for users/interviews/submissions
- Object store for logs/artifacts
- Analytics warehouse for calibration and fairness audits

---

## 4) Data Model (minimum tables/entities)
- `users`
- `interview_sessions`
- `questions`
- `question_test_cases`
- `submissions`
- `execution_results`
- `rubrics`
- `gpt_evaluations`
- `final_scores`
- `audit_logs`

Key design principle: **every score must be reproducible** from stored prompt, rubric version, model version, and submission artifact.

---

## 5) Evaluation Philosophy (Senior/Principal DS)
For higher-level DS hiring, raw correctness is necessary but insufficient.

### Core rubric dimensions
1. **Correctness**
   - Python tests pass
   - SQL returns right results including edge cases
2. **Efficiency & scalability**
   - Algorithmic complexity
   - SQL query plan awareness/index use
3. **Statistical rigor**
   - Proper assumptions, bias awareness, experiment design quality
4. **Code quality**
   - Readability, modularity, naming, comments where needed
5. **Business translation**
   - Connects outputs to product/business impact
6. **Communication**
   - Can explain trade-offs and uncertainty clearly
7. **Principal-level signal**
   - Anticipates failure modes
   - Proposes validation and monitoring strategy

### Suggested scoring weights
- Deterministic correctness: 45%
- GPT qualitative rubric: 45%
- Explainability/communication artifact: 10%

Adjust by role family (e.g., experimentation-heavy teams can increase statistical rigor weight).

---

## 6) GPT-Based Evaluation Design

## Step A: Structured rubric prompt
Use a strict JSON schema for model output:
- per-dimension score (1–5)
- rationale with citation to candidate code/query lines
- confidence level
- red flags
- suggested follow-up questions

## Step B: Multi-pass evaluation for reliability
- Pass 1: independent scoring
- Pass 2: adversarial review ("find flaws in Pass 1")
- Optional Pass 3: reconciliation pass

## Step C: Guardrails
- Never allow GPT to execute candidate code directly
- Strip PII from candidate metadata before prompt construction
- Keep model temperature low for consistency
- Store full prompts/responses for auditability

## Step D: Calibration loop
- Periodically compare GPT scores with human interview panels
- Track drift by model version, question type, and candidate segment
- Re-weight or adjust rubric language when disagreement rises

---

## 7) SQL-Specific Considerations
- Use seeded datasets with hidden edge cases:
  - null handling
  - duplicate rows
  - skewed distributions
  - late-arriving events
- Evaluate both:
  - output correctness
  - query quality (joins, window functions, performance awareness)
- Capture `EXPLAIN` plans for advanced scoring context

---

## 8) Python-Specific Considerations
- Run hidden tests beyond sample tests
- Enforce sandbox controls:
  - no outbound network
  - restricted file system
  - package allow-list
- Capture runtime metrics:
  - wall-clock time
  - memory usage
  - exception traces

---

## 9) Safety, Fairness, and Compliance
- Bias controls:
  - blind metadata in evaluator prompts
  - evaluate consistency across demographic proxies where legal/available
- Security controls:
  - container isolation
  - resource quotas
  - dependency scanning
- Compliance:
  - retention policy for interview artifacts
  - candidate data deletion workflow
  - transparent AI-assistance disclosure

---

## 10) Step-by-Step Execution Plan

## Phase 0 — Discovery (Week 1)
1. Define role matrix (Senior DS vs Principal DS expectations).
2. Finalize rubric and weight ranges per role.
3. Pick initial 10–15 interview questions (balanced Python/SQL).

## Phase 1 — Core Platform (Weeks 2–4)
1. Implement authentication and interview session lifecycle.
2. Add Python + SQL editors in one workspace.
3. Build sandbox execution services (Python container + ephemeral Postgres).
4. Store submissions and execution artifacts.

## Phase 2 — Deterministic Scoring (Weeks 4–5)
1. Build Python test harness and SQL result validator.
2. Support hidden tests and edge-case datasets.
3. Return machine-verifiable pass/fail + partial credit.

## Phase 3 — GPT Rubric Scoring (Weeks 5–7)
1. Create rubric prompt templates with JSON output schema.
2. Add two-pass scoring + reconciliation.
3. Persist scoring evidence and confidence indicators.

## Phase 4 — Interviewer UX (Weeks 7–8)
1. Build dashboard with score breakdown by dimension.
2. Show evidence snippets and generated follow-up probes.
3. Add override/comments with audit trail.

## Phase 5 — Calibration & Pilot (Weeks 9–10)
1. Run pilot interviews with dual scoring (human + GPT).
2. Measure agreement and false signal rates.
3. Tune weights/rubrics before wider rollout.

---

## 11) Suggested Tech Stack
- Frontend: Next.js + TypeScript + Monaco
- Backend: FastAPI or Node/NestJS
- Queue: Celery/RQ (Python) or BullMQ (Node)
- Python execution: Docker/Kubernetes sandbox workers
- SQL execution: Postgres templates cloned per session
- Data store: Postgres + S3-compatible object storage
- Observability: OpenTelemetry + Prometheus + Grafana

---

## 12) KPI Dashboard (what success looks like)
- Interview completion rate
- Median candidate environment setup time (target: near-zero)
- Human↔GPT score agreement (target: >0.75 weighted kappa)
- Time-to-feedback for interviewer
- Offer-stage predictive validity (longer-term)

---

## 13) Risks and Mitigations
- **Risk:** GPT over-scores polished but shallow answers.
  - **Mitigation:** increase deterministic checks + require line-cited rationale.
- **Risk:** Inconsistent scoring across model upgrades.
  - **Mitigation:** version pinning and replay-based regression suite.
- **Risk:** Candidate trust concerns.
  - **Mitigation:** clear disclosure and human override policy.

---

## 14) Immediate Next Steps for You
1. Decide if you want a **take-home async** flow, **live interview** flow, or both first.
2. I can convert this into:
   - API contract draft,
   - DB schema SQL,
   - detailed backlog (epics/stories), and
   - first implementation skeleton (FastAPI + Postgres + worker).
3. After that, we can set up a pilot rubric for one Python and one SQL question and calibrate with sample candidate answers.

