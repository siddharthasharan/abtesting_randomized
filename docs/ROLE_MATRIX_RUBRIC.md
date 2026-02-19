# Role Matrix and Rubric Weights (Issue 1)

This document operationalizes Issue 1 from the implementation plan:
- define Senior DS vs Principal DS expectations,
- finalize rubric dimensions,
- assign scoring weights by role profile,
- establish versioning and sign-off workflow.

## 1) Scope

Applies to Python + SQL interview evaluations in the MVP stage.

## 2) Role Matrix

| Dimension | Senior Data Scientist (SDS) | Principal Data Scientist (PDS) |
|---|---|---|
| Correctness | Produces mostly correct solutions with small guidance | Produces correct solutions consistently under ambiguity |
| Efficiency & Scalability | Understands complexity and practical optimization | Drives architecture-level performance trade-offs |
| Statistical Rigor | Uses valid assumptions and test design | Anticipates bias, validity threats, and organizational impact |
| Code Quality | Writes clear and maintainable code | Sets coding and review standards for teams |
| Business Translation | Connects outputs to product metrics | Shapes strategy with measurable decision frameworks |
| Communication | Explains approach and uncertainty clearly | Influences cross-functional decisions with technical clarity |
| Principal-level Signal | Not required for strong pass | Required: anticipates failure modes and monitoring plan |

## 3) Rubric Dimensions (Locked for MVP)

1. Correctness
2. Efficiency & scalability
3. Statistical rigor
4. Code quality
5. Business translation
6. Communication
7. Principal-level signal

Scoring scale per dimension: **1 (insufficient) to 5 (excellent)**.

## 4) Weight Profiles

### 4.1 Base profile (default)
- Deterministic correctness: **45%**
- GPT qualitative rubric: **45%**
- Explainability/communication artifact: **10%**

### 4.2 Senior DS profile (SDS-v1)
- Correctness: 30%
- Efficiency & scalability: 15%
- Statistical rigor: 15%
- Code quality: 15%
- Business translation: 10%
- Communication: 10%
- Principal-level signal: 5%

### 4.3 Principal DS profile (PDS-v1)
- Correctness: 20%
- Efficiency & scalability: 15%
- Statistical rigor: 20%
- Code quality: 10%
- Business translation: 15%
- Communication: 10%
- Principal-level signal: 10%

## 5) Scoring Policy

- Deterministic checks are mandatory gates for both roles.
- GPT qualitative scoring must include line-cited rationale and confidence values.
- Final score = weighted aggregate of deterministic + rubric + explainability components.
- Human override is allowed with mandatory comment and audit log entry.

## 6) Versioning

- Rubric versions use semantic style: `rubric-<role>-v<major>.<minor>`
  - Example: `rubric-sds-v1.0`, `rubric-pds-v1.0`
- Update rules:
  - Major: dimension or scale changes
  - Minor: wording/weight adjustments
- Every interview result stores: rubric version, model version, prompt version.

## 7) Sign-off Checklist

- [ ] Hiring manager sign-off
- [ ] DS panel sign-off (at least 2 reviewers)
- [ ] DEI/fairness reviewer sign-off
- [ ] Engineering owner sign-off
- [ ] Version tags added to evaluator config

## 8) Open Questions for Next Iteration

1. Should experimentation-focused roles get a dedicated profile with higher statistical rigor weighting?
2. Should SQL-heavy roles include a separate data-modeling dimension in V1?
3. What threshold should trigger mandatory human secondary review?
