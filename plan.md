# GitHub Repository SEO Plan (Agent-Ready)

Updated: 2026-03-08  
Scope: Improve discoverability and conversion for this repository across GitHub search and Google indexing of repository surfaces.  
Phase: Planning only (no implementation in this document).

## 1. Objectives

- Increase qualified discovery in GitHub repository search.
- Improve repository conversion (visitors -> stars/forks/uses/contributors).
- Strengthen trust/completeness signals (community profile + governance files).
- Preserve traffic history beyond GitHub's 14-day window.
- Build a repeatable agent-driven optimization loop using this repo's existing architecture.

## 2. KPI Model

- Discovery KPIs:
  - target query visibility on GitHub search (position bands: 1-10, 11-25, 26-50).
  - topical coverage score (share of planned topics currently configured).
- Conversion KPIs:
  - visitor -> star rate.
  - visitor -> fork rate.
  - visitor -> docs click-through rate (if docs links exist).
- Trust KPIs:
  - community profile completion score.
  - release cadence adherence.
- Trend KPIs:
  - weekly deltas for views, unique visitors, clones, unique cloners, referrers.

## 3. Technical Prerequisites (Auth + API + Limits)

### Authentication Strategy

- Preferred: Fine-grained personal access token (PAT) for repo-scoped automation.
- Minimum scopes required:
  - repository metadata read/write (for metadata checks and planned updates).
  - traffic read access (`read:traffic`) for views/clones/referrers.
- Alternative path: GitHub App for org-scale multi-repo rollout.

### API Strategy

- Use GraphQL for consolidated repository state (topics, description, community health related fields where available).
- Use REST endpoints for traffic and community/profile endpoints not exposed via GraphQL.
- Implement unified client wrapper with:
  - rate-limit introspection,
  - exponential backoff with jitter,
  - 429/403 retry policy,
  - deterministic timeout and partial-result handling.

### Rate-Limit Guardrails

- Hard limit per run (max requests budget by script).
- Cache stable responses during one run to avoid duplicate calls.
- Emit "incomplete due to rate limit" as environment limitation, not SEO failure.

## 4. Data Persistence Strategy (14-Day Traffic Constraint)

- Introduce local archive directory:
  - `.github-seo-data/`
- Proposed files:
  - `.github-seo-data/traffic_history.jsonl` (append-only daily snapshots).
  - `.github-seo-data/search_benchmark.csv` (query + rank snapshots over time).
  - `.github-seo-data/community_health_history.json` (weekly status snapshots).
- Archive policy:
  - snapshot traffic at least daily (or every 48h max).
  - keep immutable timestamped records for trend reconstruction.
- Output policy:
  - every report must indicate snapshot freshness and any data gaps.

## 5. Core Workstreams

### A. Metadata and GitHub Search Discoverability

- Optimize repository:
  - name and description for intent-match keywords.
  - topics (<=20, high-signal, non-spam).
  - homepage URL.
  - social preview image.
- Validate with deterministic query set and competitor benchmarking.

### B. README SEO + Conversion IA

- Rebuild README sections for both ranking and conversion:
  - high-intent opening value proposition.
  - installation matrix by IDE/environment.
  - capability matrix and routing examples.
  - proof/evidence section (artifacts/screenshots/output examples).
  - troubleshooting and limitations.
  - contribution and support CTAs.
- Enforce markdown SEO linting:
  - single H1, logical headings, descriptive link text.
  - image alt text coverage.
  - keyword-intent presence in title/opening sections.

### C. Trust and Community Signals

- Ensure complete governance and contribution assets:
  - `CONTRIBUTING.md`
  - `CODE_OF_CONDUCT.md`
  - `SECURITY.md`
  - issue templates and PR template
  - support/contact guidance
  - `CITATION.cff`
- Track community profile completeness weekly.

### D. Release and Distribution

- Define searchable release-note structure (feature intent + impact + migration notes).
- Standardize tags/changelog taxonomy.
- Add lightweight post-release distribution checklist.

### E. Google-to-GitHub Repository SEO

- Optimize repository page content for external snippets:
  - clear About/description phrasing,
  - strong README opening paragraphs,
  - alt text on README images,
  - meaningful section headings and internal anchors.
- If enabled, align GitHub Pages/docs with repo:
  - canonical linking strategy,
  - custom domain + HTTPS,
  - sitemap/indexing readiness.

### F. Measurement and Experiment Loop

- Weekly scorecard:
  - rank movement by query,
  - traffic and conversion deltas,
  - community completeness deltas.
- One controlled experiment per cycle (topic set, README block, release wording, social preview).
- Maintain decision log with hypothesis -> change -> measured outcome.

## 6. Repo-Native Architecture Mapping

Add GitHub SEO capability using existing project layout:

- Skills:
  - `resources/skills/seo-github.md` (main GitHub SEO orchestration instructions).
- Agents:
  - `resources/agents/seo-github-analyst.md` (strategy/orchestration role).
  - `resources/agents/seo-github-benchmark.md` (competitor/query benchmark role).
  - `resources/agents/seo-github-data.md` (API collection + persistence role).
- References:
  - `resources/references/github-ranking-factors.md`
  - `resources/references/readme-audit-rubric.md`
  - `resources/references/github-api-ops.md` (auth, scopes, limits, retries).
- Templates:
  - `resources/templates/github-seo-report.md`
  - `resources/templates/github-weekly-scorecard.md`

## 7. Script Plan (Execution Phase)

- `scripts/github_repo_audit.py`
  - audit metadata, topics, community health files, release freshness.
  - produce JSON summary + severity labels.
- `scripts/github_traffic_archiver.py` (critical)
  - fetch traffic endpoints and append timestamped snapshots to `.github-seo-data/`.
- `scripts/github_search_benchmark.py`
  - run deterministic query set, capture rank snapshots and competitor set.
- `scripts/github_readme_lint.py`
  - SEO-aware markdown linting (headings, alt text, intent-keyword coverage, CTA presence).
- `scripts/github_community_health.py`
  - evaluate community profile and missing governance artifacts.
- `scripts/github_seo_report.py`
  - merge script outputs into one consolidated markdown/html summary.

## 8. Agent Workflow (Programmatic Hand-offs)

- Agent 1: Data Collector
  - runs `github_traffic_archiver.py` + `github_repo_audit.py`.
  - owns raw API extraction, persistence, and data freshness reporting.
- Agent 2: Benchmark & Gap Explorer
  - runs `github_search_benchmark.py`.
  - builds competitor/query baseline and gap evidence.
- Agent 3: Strategist
  - ingests outputs + rubrics.
  - generates prioritized recommendations and draft artifacts for repo updates.

## 9. Execution Phases

### Phase 0 (Week 0): Infrastructure and Auth

- Define token model and required scopes.
- Create API client conventions (GraphQL + REST fallback, retry/backoff, error taxonomy).
- Define local persistence schema in `.github-seo-data/`.
- Define secrets handling and local/dev execution guidelines.

Deliverables:
- `GITHUB-AUTH-AND-API-PLAN.md`
- `GITHUB-DATA-SCHEMA.md`
- `GITHUB-EXECUTION-POLICY.md`

### Phase 1 (Week 1): Baseline and Benchmark

- Capture current metadata, README, topics, community profile status.
- Define query set and benchmark comparable repositories.
- Record initial traffic/conversion baseline snapshots.

Deliverables:
- `GITHUB-SEO-BASELINE.md`
- `GITHUB-QUERY-MAP.md`
- `GITHUB-COMPETITOR-BENCHMARK.md`

### Phase 2 (Week 2): Metadata + README Plan

- Produce metadata update plan and README SEO IA blueprint.
- Define social preview specs and variant test plan.

Deliverables:
- `GITHUB-METADATA-PLAN.md`
- `README-SEO-OUTLINE.md`
- `SOCIAL-PREVIEW-SPEC.md`

### Phase 3 (Week 3): Community + Release Framework

- Finalize governance/community artifact roadmap.
- Define release-note taxonomy and cadence policy.
- Validate `CITATION.cff` strategy.

Deliverables:
- `COMMUNITY-HEALTH-PLAN.md`
- `RELEASE-SEO-FRAMEWORK.md`

### Phase 4 (Week 4): Measurement System

- Finalize weekly scorecard and experiment protocol.
- Define go/no-go thresholds for rolling out metadata/readme changes.

Deliverables:
- `GITHUB-SEO-SCORECARD.md`
- `EXPERIMENT-LOG-TEMPLATE.md`

## 10. Risks and Assumptions

- GitHub ranking algorithm remains partially opaque; some factors are inferred and must be validated experimentally.
- API availability/rate limits can constrain data completeness for each run.
- GitHub traffic detail remains window-limited; persistent archiving is mandatory for trend analysis.
- Internal GitHub search optimization and Google indexing optimization are separate systems and may require different content choices.

## 11. Done Criteria

- Phase 0-4 deliverables defined and accepted.
- Agent responsibilities and script ownership are explicit.
- Data persistence and freshness policies are documented.
- KPI model is measurable with available API data.
- Execution backlog is implementation-ready without additional planning cycles.
