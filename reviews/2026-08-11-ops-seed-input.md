# OPS domain — prior-art seed input (parked for the dedicated mining pass)

- **Source:** Fable-class orchestrator handoff, 2026-08-11 (relayed by maintainer)
- **Status:** Adjudicated; **NOT seeded.** Parked as seed input for the dedicated
  OPS mining pass. `domains/ops.yml` is **not** created by this doc.
- **Ruling (2026-08-11):** OPS is seeded via a **dedicated corpus-mining pass**
  (chosen over hand-seed-now). This payload is prior-art input the pass
  corroborates and extends with recurrence evidence — not a drop-in.

## Why parked, not applied

The payload is a *hand-authored, prior-art* set. The maintainer ruled OPS must
be **corpus-grounded** (mine an IaC/cloud corpus, seed several entries at once
per the charter's "no skeleton" discipline). So this is the seed the pass starts
from, not the seeded domain. It originates from the `ARC-I` resilience candidates
withdrawn at the 0.1 ratification and parked for OPS (Appendix C/D).

## Adjudication (sandbox-validated 2026-08-11)

- **Schema: clean.** Validated alongside the 7 shipped domains: 387 entries,
  0 errors / 0 warnings, and stability-clean vs `v0.1.0` (OPS is additive).
- **Charter coverage: good.** Timeout, retry/backoff, circuit-breaking, graceful
  shutdown, health checks, idempotency — matches the charter's OPS concerns.
- **Severities: sound** under the "outage / data-integrity / silently-wrong-at-
  scale" bar (HIGH: timeout, shutdown, idempotency; MEDIUM: retry, breaker, health).

### Three fixes the mining pass MUST apply before seeding

1. **Single-homing `see_also` cross-refs** (the hand-seed skipped the cross-domain
   check): `OPS-B3A non-idempotent-handler` ↔ `DAT-B1D non-idempotent-migration`
   (mutual); `OPS-B1A graceful-shutdown-handler` ↔ `COD-F3D unsafe-signal-handler`.
   Distinct hazards (single-homing holds), but the pointers are required, and this
   means editing `dat.yml`/`cod.yml` too. (Timeout is clean — the only existing
   "timeout" hit is a *test* subprocess timeout, a different context.)
2. **Provenance too thin.** `provenance: [prior-art]` must cite the real source
   (the ARC-I withdrawal / Appendix C resilience list), not a bare marker.
3. **CWE verify/enrich.** Confirm `CWE-1088` resolves to the timeout weakness on
   `OPS-A1A`; if CWEs are cited, cite them consistently across the six (CWE-703,
   CWE-770, etc.).

Also fold in `missing-resource-allocation-limit` (the Gemini-rerouted IaC item)
as an OPS candidate for the same pass.

## The payload (verbatim, for the pass)

```yaml
# OCRDb domain file - 0.2 (Draft) — SEED INPUT, not applied
domain: OPS
name: production-readiness
areas:
  A:
    name: resilience-and-fault-tolerance
    categories:
      '1': timeouts-and-retries
      '2': circuit-breaking
  B:
    name: lifecycle-and-state
    categories:
      '1': shutdown-handling
      '2': observability-and-health
      '3': idempotency
entries:
  OPS-A1A:
    name: missing-timeout-on-remote-call
    typical_severity: HIGH
    status: active
    provenance: [prior-art]
    cwe: [CWE-1088]
    examples:
    - Network call to third-party API lacks a timeout, risking thread exhaustion during upstream outages
    - requests.get(url) called without the timeout parameter
  OPS-A1B:
    name: missing-retry-transient-failure
    typical_severity: MEDIUM
    status: active
    provenance: [prior-art]
    examples:
    - Database connection drop fails the entire job instead of attempting an exponential backoff retry
    - Flaky external webhook invoked exactly once with no fallback
  OPS-A2A:
    name: missing-circuit-breaker-for-downstream
    typical_severity: MEDIUM
    status: active
    provenance: [prior-art]
    examples:
    - Service continuously hammers a failing downstream dependency without tripping a circuit breaker, worsening the outage
  OPS-B1A:
    name: missing-graceful-shutdown-handler
    typical_severity: HIGH
    status: active
    provenance: [prior-art]
    examples:
    - Process exits immediately on SIGTERM without draining active HTTP requests
    - Background worker fails to flush state to disk upon receiving a kill signal
  OPS-B2A:
    name: inadequate-health-check-surface
    typical_severity: MEDIUM
    status: active
    provenance: [prior-art]
    examples:
    - /health returns 200 OK simply because the HTTP server is up, without verifying backing database connectivity
    - Liveness probe cannot distinguish between a busy process and a deadlocked process
  OPS-B3A:
    name: non-idempotent-handler
    typical_severity: HIGH
    status: active
    provenance: [prior-art]
    examples:
    - Webhook processing logic duplicates database records if the provider sends a natural retry
    - apply() loop has no resumability tracking, risking duplicate GitHub API actions if interrupted mid-batch
```
