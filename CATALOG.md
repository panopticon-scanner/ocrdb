# OCRDb Catalog — v0.4.1

392 finding types across 10 domains. Generated from `domains/` by `tools/build_catalog.py` — do not edit by hand. For a searchable view, open `build/ocrdb-0.4.1.html`.

**Severity** INFO · LOW · MEDIUM · HIGH · CRITICAL — the *typical* grade for the defect type, not a per-instance verdict. **character**: `defect` (absent) or `opportunity`.

## Domains

| Domain | Name | Entries |
|---|---|---:|
| [`ACC`](#acc--accessibility) | accessibility | 8 |
| [`AGT`](#agt--agentic-trust) | agentic-trust | 16 |
| [`ARC`](#arc--architecture) | architecture | 70 |
| [`COD`](#cod--correctness) | correctness | 55 |
| [`DAT`](#dat--data-and-persistence) | data-and-persistence | 27 |
| [`LNG`](#lng--language-and-internationalization) | language-and-internationalization | 8 |
| [`OPS`](#ops--production-readiness) | production-readiness | 9 |
| [`QAL`](#qal--quality-maintainability) | quality-maintainability | 51 |
| [`SEC`](#sec--security) | security | 72 |
| [`TST`](#tst--testing) | testing | 76 |

## ACC — accessibility

### ACC-A · semantics

**ACC-A1 · accessible-names**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ACC-A1A` | icon-only-control-missing-accessible-name | HIGH | — | — |
| `ACC-A1B` | non-text-content-missing-alternative | MEDIUM | — | — |

### ACC-B · keyboard

**ACC-B1 · keyboard-operability**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ACC-B1A` | non-interactive-element-used-as-control | HIGH | — | — |
| `ACC-B1B` | focus-indicator-suppressed | MEDIUM | — | — |

### ACC-C · forms

**ACC-C1 · form-labeling**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ACC-C1A` | input-missing-programmatic-label | MEDIUM | — | — |

### ACC-D · live-regions

**ACC-D1 · dynamic-announcements**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ACC-D1A` | dynamic-status-not-announced | MEDIUM | — | — |

### ACC-E · contrast

**ACC-E1 · perceivable-distinction**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ACC-E1A` | info-conveyed-by-color-alone | LOW | — | — |

### ACC-F · motion

**ACC-F1 · motion-preferences**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ACC-F1A` | motion-ignores-reduced-motion-preference | LOW | — | — |

## AGT — agentic-trust

### AGT-A · prompt-injection-surfaces

**AGT-A1 · injection-channels**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `AGT-A1A` | indirect-prompt-injection-untrusted-content-in-agent-context | HIGH | CWE-1427 | — |
| `AGT-A1B` | untrusted-content-in-agent-context | MEDIUM | CWE-1427 | — |

### AGT-B · tool-and-permission-scoping

**AGT-B1 · authority-scope**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `AGT-B1A` | incomplete-mediation-coverage-gap | HIGH | CWE-863, CWE-284 | — |
| `AGT-B1B` | missing-approval-gate-for-destructive-action | HIGH | CWE-862 | — |
| `AGT-B1C` | unscoped-write-authority | HIGH | CWE-284 | — |
| `AGT-B1D` | overbroad-tool-grant | MEDIUM | CWE-269 | — |

### AGT-C · output-trust-boundaries

**AGT-C1 · unverified-trust**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `AGT-C1A` | self-asserted-trust-metadata-spoofing | HIGH | CWE-290, CWE-345, CWE-807 | — |
| `AGT-C1B` | findings-from-undeclared-source-merged-despite-flagging | MEDIUM | CWE-693 | — |
| `AGT-C1C` | unauthenticated-external-data-rebuilds-trust-mapping | MEDIUM | CWE-345, CWE-290 | — |
| `AGT-C1D` | unstructured-llm-output-trusted-for-control-decision | MEDIUM | CWE-345 | — |

### AGT-D · autonomy-and-oversight

**AGT-D1 · verifier-and-action-integrity**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `AGT-D1A` | agent-confabulated-action | HIGH | — | — |
| `AGT-D1B` | secret-materialized-into-agent-output | HIGH | CWE-532 | — |
| `AGT-D1C` | single-verifier-unilateral-override-authority | MEDIUM | CWE-863 | — |

### AGT-E · resource-and-cost-safety

**AGT-E1 · budget-and-loops**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `AGT-E1A` | unbounded-agent-loop | HIGH | CWE-834 | — |
| `AGT-E1B` | unbounded-tool-call-budget | MEDIUM | — | — |

### AGT-F · data-egress

**AGT-F1 · provider-egress**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `AGT-F1A` | sensitive-data-sent-to-model-provider | MEDIUM | CWE-200 | — |

## ARC — architecture

### ARC-A · module-boundaries

**ARC-A1 · cohesion**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ARC-A1A` | fragmented-logic-no-single-owner | MEDIUM | CWE-710 | — |
| `ARC-A1B` | mixed-responsibility-module | MEDIUM | CWE-1120 | — |
| `ARC-A1C` | monolithic-function-mixed-concerns | MEDIUM | CWE-1120 | — |

**ARC-A2 · coupling**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ARC-A2A` | circular-or-load-order-coupling | MEDIUM | CWE-1047 | — |
| `ARC-A2B` | hidden-contract-via-informal-parsing | MEDIUM | CWE-1008, CWE-710 | — |
| `ARC-A2C` | unpackaged-module-resolution-hack | MEDIUM | CWE-710 | — |
| `ARC-A2D` | leaky-module-interface | LOW | CWE-1061 | — |

**ARC-A3 · duplication**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ARC-A3A` | duplicated-business-logic-without-shared-module | MEDIUM | CWE-1041 | — |
| `ARC-A3B` | duplicated-configuration-or-mapping-table | LOW | CWE-1041 | — |

**ARC-A4 · extension-point-consistency**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ARC-A4A` | adapter-implementation-inconsistency | MEDIUM | CWE-710 | — |
| `ARC-A4C` | shadow-registry-without-enforced-parity | MEDIUM | CWE-710 | — |
| `ARC-A4D` | silent-failure-on-unrecognized-extension | MEDIUM | CWE-390, CWE-392 | — |

**ARC-A5 · canonical-ownership**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ARC-A5A` | non-canonical-constant-duplication | LOW | — | opportunity |
| `ARC-A5B` | redundant-derived-structure | LOW | — | opportunity |

### ARC-B · dependency-and-build-architecture

**ARC-B1 · packaging-metadata**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ARC-B1A` | missing-dependency-manifest-declarations | MEDIUM | — | — |
| `ARC-B1C` | stale-project-metadata-urls | MEDIUM | CWE-1059 | — |
| `ARC-B1D` | incomplete-build-system-declaration | LOW | — | — |
| `ARC-B1E` | self-contradictory-lint-configuration | LOW | CWE-710 | — |
| `ARC-B1F` | nonstandard-install-mechanism-bypasses-package-manager | INFO | — | — |

**ARC-B3 · container-image-design**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ARC-B3A` | divergent-execution-path-across-environments | MEDIUM | — | — |
| `ARC-B3B` | monolithic-multi-toolchain-image | MEDIUM | — | — |
| `ARC-B3C` | circular-build-dependency | LOW | CWE-1047 | — |

### ARC-C · ci-cd-pipeline-architecture

**ARC-C1 · pipeline-gating**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ARC-C1A` | ci-gate-bypasses-domain-verdict-model | HIGH | CWE-693 | — |
| `ARC-C1B` | ci-trigger-path-filter-incomplete | MEDIUM | — | — |
| `ARC-C1C` | untested-integration-path-in-ci | MEDIUM | — | — |
| `ARC-C1D` | ci-lint-gate-scope-gap | LOW | — | — |
| `ARC-C1E` | inconsistent-workflow-permissions-scoping | LOW | CWE-732 | — |

**ARC-C2 · failure-handling**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ARC-C2A` | silent-fallback-masks-pipeline-failure | LOW | CWE-390 | — |
| `ARC-C2B` | swallowed-ci-step-failure | INFO | CWE-392 | — |

### ARC-D · contracts-and-interfaces

**ARC-D1 · schema-implementation-drift**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ARC-D1A` | lossy-round-trip-between-producer-and-recovery-path | HIGH | CWE-436 | — |
| `ARC-D1B` | report-contract-out-of-sync-with-schema | HIGH | CWE-1059, CWE-436 | — |
| `ARC-D1C` | fingerprint-identity-instability | MEDIUM | CWE-436 | — |
| `ARC-D1D` | id-format-schema-mismatch | MEDIUM | CWE-436 | — |
| `ARC-D1E` | redundant-independent-derivation-of-shared-fact | MEDIUM | CWE-1041 | — |
| `ARC-D1F` | unversioned-inter-phase-data-contract | LOW | — | — |

**ARC-D2 · contract-completeness**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ARC-D2A` | cli-interface-contract-drift | HIGH | CWE-1059 | — |
| `ARC-D2B` | inconsistent-handling-of-equivalent-edge-case-inputs | MEDIUM | CWE-436 | — |
| `ARC-D2C` | missing-coordination-contract-between-agents | MEDIUM | CWE-662 | — |
| `ARC-D2D` | orphaned-schema-field-never-populated | MEDIUM | — | — |
| `ARC-D2E` | required-field-never-emitted-by-producer | MEDIUM | CWE-436 | — |
| `ARC-D2F` | undefined-or-ambiguous-spec-terminology | MEDIUM | CWE-1059 | — |

**ARC-D3 · missing-referenced-artifacts**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ARC-D3A` | missing-referenced-file | HIGH | — | — |
| `ARC-D3B` | documented-artifact-not-present-in-repo | MEDIUM | CWE-1059 | — |

### ARC-E · configuration-architecture

**ARC-E1 · hardcoded-values**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ARC-E1A` | hardcoded-absolute-path-in-source | HIGH | CWE-547 | — |
| `ARC-E1B` | hardcoded-environment-specific-artifact-path | HIGH | CWE-547 | — |
| `ARC-E1C` | hardcoded-identifier-scattered-across-modules | MEDIUM | CWE-547 | — |

**ARC-E2 · implicit-and-global-state**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ARC-E2A` | durable-state-in-ephemeral-scratch-location | MEDIUM | — | — |
| `ARC-E2B` | global-scope-write-conflicts-with-project-scoped-model | MEDIUM | — | — |
| `ARC-E2C` | implicit-runtime-contract-unenforced | MEDIUM | — | — |
| `ARC-E2D` | implicit-config-discovery-action-at-a-distance | LOW | — | — |

**ARC-E3 · config-model-complexity**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ARC-E3A` | orthogonal-config-axes-increase-complexity | MEDIUM | CWE-1120 | — |
| `ARC-E3B` | asymmetric-domain-coverage-across-artifacts | LOW | — | — |
| `ARC-E3C` | cross-host-config-parity-gap | LOW | — | — |

### ARC-F · enforcement-and-security-boundary

**ARC-F1 · enforcement-gap**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ARC-F1A` | enforcement-relies-on-stale-flag-not-live-verification | HIGH | CWE-367, CWE-693 | — |
| `ARC-F1B` | audit-accounting-excludes-in-scope-actors | MEDIUM | CWE-778 | — |
| `ARC-F1C` | inconsistent-authorization-gate-across-sibling-scripts | MEDIUM | CWE-862 | — |
| `ARC-F1D` | partial-batch-operation-lacks-failure-recovery-path | MEDIUM | CWE-755 | — |
| `ARC-F1E` | policy-or-verdict-not-enforced-by-code | MEDIUM | CWE-693 | — |

**ARC-F2 · fail-open-defaults**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ARC-F2A` | compensating-control-has-scope-blind-spot | HIGH | CWE-693 | — |
| `ARC-F2B` | enforcement-hook-cannot-scope-to-individual-actor | HIGH | CWE-284 | — |
| `ARC-F2C` | security-control-assumes-undocumented-input-shape | HIGH | CWE-20 | — |
| `ARC-F2D` | component-fails-open-on-malformed-input | MEDIUM | CWE-636 | — |
| `ARC-F2E` | security-control-fails-open-on-misconfiguration | MEDIUM | CWE-636, CWE-280 | — |
| `ARC-F2G` | overbroad-exception-handling-masks-errors | LOW | CWE-396 | — |

### ARC-G · documentation-and-spec-integrity

**ARC-G1 · doc-reality-drift**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ARC-G1A` | contributor-instructions-diverge-from-ci | MEDIUM | CWE-1059 | — |
| `ARC-G1B` | divergent-duplicate-source-of-truth | MEDIUM | CWE-1059 | — |
| `ARC-G1C` | reference-documentation-incomplete | LOW | CWE-1059 | — |

**ARC-G2 · design-doc-lifecycle**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ARC-G2A` | superseded-doc-without-deprecation-marker | MEDIUM | CWE-1059 | — |
| `ARC-G2B` | design-doc-drifts-from-delivered-scope | LOW | CWE-1059 | — |

**ARC-G3 · repo-hygiene-and-meta-config**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `ARC-G3B` | tracked-file-violates-own-gitignore-rule | LOW | — | — |

## COD — correctness

### COD-A · resource-lifecycle

**COD-A1 · handle-and-timing-safety**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `COD-A1A` | unclosed-file-handle-leak | MEDIUM | CWE-772 | — |

**COD-A2 · bounds-and-indexing-safety**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `COD-A2A` | unbounded-buffer-write | CRITICAL | CWE-787, CWE-120 | — |
| `COD-A2B` | off-by-one-argument-index-error | MEDIUM | CWE-193 | — |
| `COD-A2C` | unchecked-index-or-empty-sequence-access | MEDIUM | CWE-129 | — |

### COD-B · defensive-checking-discipline

**COD-B1 · guard-and-permission-scope**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `COD-B1A` | fail-open-on-missing-or-corrupt-config | HIGH | CWE-636 | — |
| `COD-B1C` | overly-broad-permission-scope-in-shared-guard | MEDIUM | CWE-284 | — |

**COD-B2 · silent-failure-and-diagnostics**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `COD-B2A` | unguarded-null-crashes-downstream | MEDIUM | CWE-476 | — |
| `COD-B2B` | error-message-misattributes-root-cause | LOW | — | — |
| `COD-B2C` | missing-error-handling-around-auxiliary-load | LOW | CWE-755 | — |
| `COD-B2D` | result-not-revalidated-after-transform | LOW | — | — |
| `COD-B2E` | silent-truncation-without-warning | LOW | — | — |

### COD-C · tool-adapter-normalization

**COD-C1 · severity-confidence-conflation**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `COD-C1A` | analyzer-confidence-conflated-with-severity | HIGH | — | — |
| `COD-C1B` | severity-hardcoded-ignoring-tool-value | HIGH | — | — |

**COD-C2 · parsing-and-selection-logic**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `COD-C2A` | incorrect-source-file-selection-heuristic | HIGH | CWE-706 | — |
| `COD-C2B` | instance-state-not-propagated-through-lifecycle | MEDIUM | — | — |
| `COD-C2C` | regex-rejects-valid-input-variant | MEDIUM | — | — |
| `COD-C2D` | unnormalized-identifier-causes-lookup-mismatch | MEDIUM | CWE-706 | — |

**COD-C3 · output-conformance-gaps**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `COD-C3A` | required-output-field-missing-or-empty | HIGH | — | — |
| `COD-C3B` | incomplete-lookup-catalog-silent-fallback-gap | MEDIUM | CWE-1059 | — |
| `COD-C3C` | nonstandard-key-silently-dropped-downstream | LOW | — | — |

### COD-D · interface-contract-drift

**COD-D1 · schema-definition-drift**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `COD-D1A` | schema-enum-incomplete-vs-actual-values | HIGH | — | — |
| `COD-D1B` | schema-pattern-stricter-than-producer-output | HIGH | — | — |
| `COD-D1C` | inconsistent-record-shape-across-array | MEDIUM | — | — |
| `COD-D1D` | schema-omits-documented-required-fields | MEDIUM | — | — |

**COD-D2 · doc-implementation-divergence**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `COD-D2B` | documented-feature-or-flag-not-implemented | HIGH | — | — |
| `COD-D2C` | self-contradicting-specification-documents | HIGH | — | — |
| `COD-D2D` | implemented-capability-missing-from-docs | MEDIUM | — | — |

**COD-D3 · boundary-type-and-protocol-mismatch**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `COD-D3A` | external-api-invoked-with-wrong-parameter-shape | HIGH | CWE-628 | — |
| `COD-D3B` | adapter-violates-declared-protocol-interface | MEDIUM | CWE-573 | — |
| `COD-D3C` | inconsistent-field-type-across-boundary | MEDIUM | CWE-704 | — |

### COD-E · control-flow-and-execution-order

**COD-E1 · iteration-and-shortcut-logic**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `COD-E1A` | dedup-logic-drops-entry-sharing-coarse-key | MEDIUM | — | — |
| `COD-E1B` | loop-exits-before-exhausting-valid-entries | LOW | — | — |

**COD-E2 · execution-context-and-ordering**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `COD-E2A` | unreachable-code-due-to-guard-placed-before-definition | CRITICAL | CWE-670 | — |
| `COD-E2B` | path-resolved-against-wrong-base-directory | MEDIUM | CWE-706 | — |

### COD-F · concurrency-and-asynchrony

**COD-F1 · shared-state**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `COD-F1A` | atomicity-violation-compound-operation | MEDIUM | CWE-362 | — |
| `COD-F1B` | check-then-act-race | MEDIUM | CWE-367 | — |
| `COD-F1C` | shared-mutable-state-without-synchronization | MEDIUM | CWE-362 | — |

**COD-F2 · liveness-and-blocking**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `COD-F2A` | deadlock-lock-ordering | HIGH | CWE-833 | — |
| `COD-F2B` | blocking-call-in-async-context | MEDIUM | — | — |

**COD-F3 · async-correctness**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `COD-F3A` | stale-cache-read-without-invalidation | MEDIUM | — | — |
| `COD-F3B` | thread-unsafe-lazy-initialization | MEDIUM | CWE-543 | — |
| `COD-F3C` | unawaited-async-result | MEDIUM | — | — |
| `COD-F3D` | unsafe-signal-handler | MEDIUM | CWE-479 | — |

### COD-G · data-representation-and-time

**COD-G1 · temporal**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `COD-G1A` | dst-unsafe-time-arithmetic | MEDIUM | — | — |
| `COD-G1B` | epoch-unit-confusion-ms-vs-s | MEDIUM | — | — |
| `COD-G1C` | naive-aware-datetime-mixing | MEDIUM | — | — |
| `COD-G1D` | wall-clock-used-for-elapsed-time | LOW | — | — |

**COD-G2 · numeric**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `COD-G2A` | monetary-value-in-float | HIGH | CWE-681 | — |
| `COD-G2B` | integer-overflow-or-truncation | MEDIUM | CWE-190 | — |
| `COD-G2C` | precision-loss-in-numeric-conversion | MEDIUM | CWE-681 | — |
| `COD-G2D` | float-equality-comparison | LOW | — | — |

**COD-G3 · encoding-and-units**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `COD-G3A` | bytes-string-conflation | MEDIUM | — | — |
| `COD-G3B` | default-encoding-assumption | MEDIUM | CWE-176 | — |
| `COD-G3C` | unit-confusion-in-quantity | MEDIUM | — | — |
| `COD-G3D` | unicode-normalization-mismatch | LOW | CWE-176 | — |

## DAT — data-and-persistence

### DAT-A · schema-design

**DAT-A1 · integrity-and-modeling**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `DAT-A1A` | inappropriate-type-for-domain | MEDIUM | — | — |
| `DAT-A1B` | missing-constraint-for-invariant | MEDIUM | — | — |
| `DAT-A1C` | missing-foreign-key-relationship | MEDIUM | — | — |
| `DAT-A1D` | nullable-column-ambiguous-semantics | LOW | — | — |

### DAT-B · migrations

**DAT-B1 · safety-and-reversibility**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `DAT-B1A` | destructive-migration-without-backfill | HIGH | — | — |
| `DAT-B1B` | table-lock-heavy-migration | HIGH | — | — |
| `DAT-B1C` | irreversible-migration-no-rollback | MEDIUM | — | — |
| `DAT-B1D` | non-idempotent-migration | MEDIUM | — | — |
| `DAT-B1E` | no-op-or-disabled-migration | MEDIUM | — | — |
| `DAT-B1F` | migration-error-swallowed-marked-applied | HIGH | — | — |

### DAT-C · query-patterns

**DAT-C1 · efficiency-and-scale**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `DAT-C1A` | missing-index-for-hot-query | MEDIUM | — | — |
| `DAT-C1B` | n-plus-one-query | MEDIUM | — | — |
| `DAT-C1C` | unbounded-result-set | MEDIUM | CWE-770 | — |
| `DAT-C1D` | select-star-in-production-path | LOW | — | — |

### DAT-D · transactions-and-concurrency

**DAT-D1 · isolation-and-atomicity**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `DAT-D1A` | isolation-level-mismatch | HIGH | — | — |
| `DAT-D1B` | missing-transaction-boundary | HIGH | — | — |
| `DAT-D1C` | read-modify-write-race | HIGH | CWE-362 | — |
| `DAT-D1D` | long-running-transaction | MEDIUM | — | — |

### DAT-E · data-lifecycle

**DAT-E1 · retention-and-drift**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `DAT-E1A` | code-schema-drift-without-migration | HIGH | — | — |
| `DAT-E1B` | orphaned-rows-on-delete | MEDIUM | — | — |
| `DAT-E1C` | soft-delete-inconsistency | MEDIUM | — | — |
| `DAT-E1D` | mirror-source-divergence | MEDIUM | — | — |

### DAT-F · durable-file-and-local-state

**DAT-F1 · write-durability-and-atomicity**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `DAT-F1A` | destructive-rewrite-without-backup | HIGH | — | — |
| `DAT-F1B` | non-atomic-file-write | MEDIUM | — | — |
| `DAT-F1C` | lost-update-on-unsynchronized-file | MEDIUM | — | — |

**DAT-F2 · format-and-read-safety**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `DAT-F2A` | unversioned-persisted-format | MEDIUM | — | — |
| `DAT-F2B` | unbounded-persisted-file-read | LOW | CWE-789 | — |

## LNG — language-and-internationalization

### LNG-A · externalization

**LNG-A1 · string-externalization**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `LNG-A1A` | hardcoded-user-facing-string | MEDIUM | — | — |
| `LNG-A1B` | string-assembled-outside-i18n | LOW | — | — |

### LNG-B · locale-formatting

**LNG-B1 · locale-aware-formatting**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `LNG-B1A` | locale-unaware-number-date-format | LOW | — | — |
| `LNG-B1B` | naive-pluralization | LOW | — | — |

### LNG-C · grammar

**LNG-C1 · translation-composition**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `LNG-C1A` | translation-assembled-by-concatenation | MEDIUM | — | — |

### LNG-D · key-drift

**LNG-D1 · key-management**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `LNG-D1A` | translation-key-drift-or-missing-fallback | LOW | — | — |

### LNG-E · encoding

**LNG-E1 · text-encoding**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `LNG-E1A` | byte-vs-codepoint-length-confusion | LOW | CWE-176 | — |

### LNG-F · directionality

**LNG-F1 · directionality**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `LNG-F1A` | missing-rtl-bidi-support | LOW | — | — |

## OPS — production-readiness

### OPS-A · resilience

**OPS-A1 · external-call-resilience**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `OPS-A1A` | missing-timeout-on-external-call | HIGH | — | — |
| `OPS-A1B` | retry-without-backoff-or-jitter | MEDIUM | — | — |

### OPS-B · lifecycle

**OPS-B1 · startup-and-shutdown**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `OPS-B1A` | no-graceful-shutdown-drain | HIGH | — | — |
| `OPS-B1B` | fake-or-noop-health-check | MEDIUM | — | — |

### OPS-C · deployment-config

**OPS-C1 · startup-configuration**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `OPS-C1A` | unvalidated-startup-configuration | MEDIUM | — | — |
| `OPS-C1B` | unconditional-startup-side-effect | LOW | — | — |

### OPS-D · resource-limits

**OPS-D1 · resource-bounds**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `OPS-D1A` | unbounded-resource-consumption | HIGH | — | — |
| `OPS-D1B` | missing-pagination-or-result-cap | MEDIUM | — | — |

### OPS-E · observability

**OPS-E1 · failure-visibility**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `OPS-E1A` | silent-failure-without-telemetry | MEDIUM | — | — |

## QAL — quality-maintainability

### QAL-A · readability

**QAL-A1 · naming**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `QAL-A1B` | inconsistent-naming-convention | INFO | — | opportunity |
| `QAL-A1C` | name-collision-with-domain-concept | INFO | — | — |

**QAL-A2 · clarity**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `QAL-A2B` | confusing-expression-precedence | LOW | CWE-1078 | — |
| `QAL-A2C` | magic-number-or-fragile-hardcoded-index | LOW | — | opportunity |
| `QAL-A2D` | comment-noise | INFO | — | opportunity |

### QAL-B · style-and-formatting

**QAL-B1 · imports**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `QAL-B1A` | combined-imports-single-line | LOW | CWE-1078 | auto: ruff:E401 |
| `QAL-B1B` | mid-file-or-inline-import-placement | LOW | CWE-1078 | auto: ruff:E402 |
| `QAL-B1C` | redundant-shadowing-import | LOW | CWE-1041 | auto: ruff:F811 |

**QAL-B2 · whitespace-and-layout**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `QAL-B2A` | line-too-long | LOW | CWE-1078 | auto: ruff:E501 |
| `QAL-B2B` | misaligned-or-awkward-continuation | LOW | CWE-1078 | — |
| `QAL-B2C` | missing-blank-line-separation | LOW | CWE-1078 | — |
| `QAL-B2D` | inconsistent-literal-whitespace | INFO | CWE-1078 | — |

**QAL-B3 · string-formatting**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `QAL-B3A` | inconsistent-diagnostic-prefix-convention | LOW | CWE-1078 | — |
| `QAL-B3B` | mixed-fstring-percent-formatting | LOW | CWE-1078 | — |
| `QAL-B3C` | string-concatenation-instead-of-fstring | LOW | CWE-1078 | — |

### QAL-C · documentation

**QAL-C1 · stale-references**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `QAL-C1A` | stale-external-url-reference | MEDIUM | — | — |
| `QAL-C1B` | inconsistent-ordering-in-docs | LOW | — | — |
| `QAL-C1C` | stale-file-path-reference | LOW | CWE-1059 | — |
| `QAL-C1D` | stale-version-number | LOW | CWE-1059 | — |

**QAL-C2 · docs-code-drift**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `QAL-C2A` | schema-or-example-stricter-than-reality | MEDIUM | — | — |
| `QAL-C2B` | self-contradictory-documentation | MEDIUM | — | — |
| `QAL-C2C` | cli-docs-out-of-sync-with-implementation | LOW | — | — |
| `QAL-C2D` | docstring-inaccurate-error-contract | LOW | — | — |
| `QAL-C2E` | typo-in-shipped-text | LOW | — | — |
| `QAL-C2F` | undocumented-configuration-behavior | LOW | — | — |

### QAL-D · duplication

**QAL-D1 · duplicated-logic**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `QAL-D1A` | duplicated-business-logic-block | MEDIUM | CWE-1041 | opportunity |
| `QAL-D1B` | duplicated-constant-definition | MEDIUM | CWE-1041 | — |
| `QAL-D1C` | duplicated-helper-function | MEDIUM | CWE-1041 | opportunity |

### QAL-E · dead-code

**QAL-E1 · dead-configuration**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `QAL-E1A` | dead-configuration-setting | LOW | CWE-561 | — |
| `QAL-E1B` | unused-duplicate-validator-left-in-code | LOW | CWE-561, CWE-1041 | — |

**QAL-E2 · stale-artifacts**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `QAL-E2B` | retired-component-still-registered | MEDIUM | CWE-561 | — |
| `QAL-E2C` | orphaned-asset-rules | INFO | — | — |

**QAL-E3 · unused-code**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `QAL-E3A` | dead-code-unused-function | LOW | — | — |

### QAL-F · structure-and-convention

**QAL-F1 · import-dependency-structure**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `QAL-F1A` | implicit-sys-path-or-import-dependency | MEDIUM | — | — |
| `QAL-F1B` | inconsistent-import-style-across-modules | MEDIUM | CWE-1099 | — |

**QAL-F2 · code-placement**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `QAL-F2A` | logic-embedded-in-non-standard-location | LOW | — | — |
| `QAL-F2B` | main-guard-or-block-misplaced-mid-file | LOW | CWE-1078 | — |

**QAL-F3 · convention-divergence**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `QAL-F3B` | inconsistent-noqa-annotation-usage | LOW | — | auto: ruff:RUF100 |
| `QAL-F3C` | inconsistent-per-host-field-naming | INFO | CWE-1099 | — |
| `QAL-F3D` | partial-type-hint-adoption | INFO | — | opportunity |

### QAL-G · efficiency

**QAL-G1 · redundant-computation**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `QAL-G1A` | loop-invariant-not-hoisted | LOW | — | opportunity |
| `QAL-G1B` | missing-memoization | LOW | — | opportunity |
| `QAL-G1C` | repeated-filesystem-stat | LOW | — | opportunity |

**QAL-G2 · memory-and-scale**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `QAL-G2A` | unbounded-collection-load | MEDIUM | CWE-400 | — |

### QAL-H · complexity-and-simplification

**QAL-H1 · complexity**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `QAL-H1A` | overly-complex-function | MEDIUM | — | opportunity |
| `QAL-H1B` | excess-nesting-complexity | LOW | — | opportunity |

**QAL-H2 · simplification-judgment**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `QAL-H2A` | harmful-oversimplification | MEDIUM | — | — |
| `QAL-H2B` | correctness-entangled-duplication-deferred | LOW | — | opportunity |
| `QAL-H2C` | needless-abstraction | LOW | — | opportunity |

### QAL-I · observability

**QAL-I1 · diagnostics**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `QAL-I1A` | missing-trace-context-propagation | LOW | — | — |
| `QAL-I1B` | vague-log-message-without-context | INFO | CWE-778 | — |

## SEC — security

### SEC-A · injection-and-unsafe-execution

**SEC-A1 · command-execution**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-A1A` | os-command-injection | HIGH | CWE-78, CWE-88 | — |
| `SEC-A1B` | unsafe-subprocess-invocation-pattern | LOW | CWE-78, CWE-88 | — |

**SEC-A2 · code-injection-and-deserialization**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-A2A` | eval-of-untrusted-input | CRITICAL | CWE-95, CWE-94 | — |
| `SEC-A2B` | insecure-deserialization-of-untrusted-data | HIGH | CWE-502 | — |

**SEC-A3 · sql-injection**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-A3A` | sql-injection-via-string-concatenation | CRITICAL | CWE-89 | — |

**SEC-A4 · xml-and-entity-processing**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-A4A` | xxe-vulnerable-xml-parsing | MEDIUM | CWE-611, CWE-776 | — |
| `SEC-A4B` | xml-library-import-flagged | LOW | CWE-611 | — |

### SEC-B · output-handling-and-data-exposure

**SEC-B1 · output-encoding-and-report-hardening**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-B1A` | markdown-mention-injection-in-automated-comments | MEDIUM | CWE-74 | — |
| `SEC-B1B` | unsafe-url-scheme-allowed-in-links | MEDIUM | CWE-79, CWE-601 | — |
| `SEC-B1C` | untrusted-content-unsanitized-in-generated-output | MEDIUM | CWE-79, CWE-116 | — |
| `SEC-B1D` | unintended-external-resource-load-in-offline-report | LOW | CWE-200 | — |
| `SEC-B1E` | missing-content-security-policy-in-generated-report | INFO | CWE-1021, CWE-693 | — |

**SEC-B2 · information-disclosure**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-B2A` | debug-endpoint-secret-exposure | HIGH | CWE-215, CWE-200 | — |
| `SEC-B2B` | credentials-printed-to-output-or-logs | MEDIUM | CWE-532 | — |
| `SEC-B2C` | incomplete-sensitive-data-redaction | MEDIUM | CWE-200 | — |
| `SEC-B2D` | verbose-error-message-disclosure | LOW | CWE-209 | — |

**SEC-B3 · secrets-handling**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-B3A` | embedded-credential-or-api-key-in-repo | HIGH | CWE-798 | — |
| `SEC-B3B` | full-environment-inherited-by-subprocess | MEDIUM | CWE-200 | — |
| `SEC-B3C` | hardcoded-secret-heuristic-flag | LOW | CWE-259, CWE-798 | — |

**SEC-B4 · privacy-and-data-protection**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-B4A` | pii-in-logs | MEDIUM | CWE-532 | — |
| `SEC-B4B` | excessive-data-collection | LOW | CWE-359 | — |
| `SEC-B4C` | missing-retention-limit | LOW | — | — |

### SEC-C · identity-access-and-cryptography

**SEC-C1 · access-control**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-C1A` | excessive-container-network-and-filesystem-privilege | HIGH | CWE-250, CWE-1008 | — |
| `SEC-C1B` | hardcoded-backdoor-trigger | HIGH | CWE-506, CWE-489 | — |
| `SEC-C1C` | missing-function-level-authorization | HIGH | CWE-862, CWE-285 | — |
| `SEC-C1D` | ambient-authority-unscoped-mutation | MEDIUM | CWE-284 | — |
| `SEC-C1E` | container-runs-as-root | LOW | CWE-250 | — |
| `SEC-C1F` | missing-object-level-authorization | HIGH | CWE-639, CWE-566 | — |

**SEC-C2 · authentication**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-C2A` | missing-brute-force-protection | MEDIUM | CWE-307 | — |
| `SEC-C2B` | timing-unsafe-credential-comparison | MEDIUM | CWE-208 | — |
| `SEC-C2C` | user-enumeration-via-response-discrepancy | MEDIUM | CWE-203, CWE-204, CWE-205 | — |

**SEC-C3 · cryptography**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-C3A` | weak-prng-for-security-token | HIGH | CWE-338 | — |
| `SEC-C3B` | weak-standard-crypto-algorithm | HIGH | CWE-327 | — |
| `SEC-C3C` | non-cryptographic-hash-in-security-context | MEDIUM | CWE-328, CWE-327 | — |

**SEC-C4 · logging-and-monitoring**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-C4B` | missing-audit-logging-for-sensitive-action | LOW | CWE-778, CWE-223 | — |

### SEC-D · untrusted-path-and-resource-resolution

**SEC-D1 · path-and-search-resolution**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-D1A` | path-traversal-via-unvalidated-input | HIGH | CWE-22 | — |
| `SEC-D1B` | uncontrolled-search-path-element | HIGH | CWE-426, CWE-427 | — |
| `SEC-D1C` | unsafe-symlink-following-on-copy | HIGH | CWE-61, CWE-59 | — |

**SEC-D2 · ssrf**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-D2A` | server-side-request-forgery-to-internal-service | HIGH | CWE-918 | — |
| `SEC-D2B` | unvalidated-url-fetch-target-ssrf-precursor | LOW | CWE-918 | — |

### SEC-E · supply-chain-and-build-integrity

**SEC-E1 · dependency-management**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-E1A` | dependabot-missing-cooldown-period | MEDIUM | CWE-1357 | — |
| `SEC-E1B` | known-vulnerable-dependency | MEDIUM | CWE-1104, CWE-937 | — |
| `SEC-E1C` | missing-lockfile-integrity-hash | MEDIUM | CWE-494, CWE-1357 | — |
| `SEC-E1D` | abandoned-unmaintained-dependency | LOW | CWE-1104 | — |

**SEC-E2 · pinning-and-provenance**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-E2A` | unpinned-build-dependency-install | HIGH | CWE-1357, CWE-829 | — |
| `SEC-E2B` | mutable-ci-action-reference | MEDIUM | CWE-829, CWE-1357 | — |
| `SEC-E2C` | unpinned-third-party-source-reference | MEDIUM | CWE-829 | — |

**SEC-E3 · unverified-code-execution**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-E3A` | arbitrary-code-execution-via-untrusted-build-file | CRITICAL | CWE-94, CWE-829 | — |
| `SEC-E3B` | unverified-binary-download-no-integrity-check | MEDIUM | CWE-494, CWE-345 | — |
| `SEC-E3C` | unverified-remote-script-execution-curl-pipe-shell | MEDIUM | CWE-494, CWE-829 | — |

### SEC-F · robustness-under-adversarial-input

**SEC-F1 · exception-handling**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-F1A` | crash-on-malformed-input | MEDIUM | CWE-248, CWE-755 | — |
| `SEC-F1B` | silent-exception-swallowing | LOW | CWE-390, CWE-703 | — |

**SEC-F2 · resource-management**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-F2A` | unbounded-external-response-read | MEDIUM | CWE-400, CWE-770 | — |

### SEC-G · security-tooling-and-scan-integrity

**SEC-G1 · severity-and-triage-fidelity**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-G1B` | tool-citation-cwe-mismatch | LOW | — | — |

**SEC-G2 · scan-coverage-integrity**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-G2A` | security-surface-not-routed-to-review-lens | HIGH | — | — |
| `SEC-G2B` | silent-scan-coverage-loss | MEDIUM | CWE-778 | — |
| `SEC-G2C` | unpinned-scan-ruleset | LOW | CWE-1357 | — |

**SEC-G3 · security-testing-and-governance**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-G3B` | insufficient-negative-test-coverage-for-security-guard | LOW | CWE-1120 | — |
| `SEC-G3C` | security-invariant-enforced-only-via-assert | LOW | CWE-617 | — |
| `SEC-G3D` | missing-vulnerability-disclosure-policy | INFO | — | — |

### SEC-H · web-session-and-browser-boundary

**SEC-H1 · session-management**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-H1A` | session-fixation | HIGH | CWE-384 | — |
| `SEC-H1B` | missing-secure-cookie-flags | MEDIUM | CWE-614 | — |
| `SEC-H1C` | missing-session-expiry | MEDIUM | CWE-613 | — |

**SEC-H2 · cross-site-request**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-H2A` | csrf-missing-token-protection | HIGH | CWE-352 | — |
| `SEC-H2B` | cors-misconfiguration | MEDIUM | CWE-942 | — |
| `SEC-H2C` | open-redirect | MEDIUM | CWE-601 | — |
| `SEC-H2D` | missing-frame-protection-clickjacking | LOW | CWE-1021 | — |

**SEC-H3 · token-and-federation**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-H3A` | jwt-algorithm-confusion | HIGH | CWE-347 | — |
| `SEC-H3B` | oauth-redirect-uri-validation-gap | HIGH | CWE-601 | — |
| `SEC-H3C` | jwt-missing-expiry-or-audience-validation | MEDIUM | CWE-613 | — |

**SEC-H4 · adversarial-request-processing**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `SEC-H4A` | redos-catastrophic-backtracking | MEDIUM | CWE-1333 | — |
| `SEC-H4B` | unbounded-request-size | MEDIUM | CWE-400 | — |

## TST — testing

### TST-A · coverage

**TST-A1 · untested-units**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `TST-A1A` | zero-coverage-script | HIGH | — | — |
| `TST-A1B` | uncovered-function-or-method | MEDIUM | — | — |
| `TST-A1C` | untested-critical-recovery-function | MEDIUM | — | — |
| `TST-A1D` | untested-cli-flag-or-entrypoint-wiring | LOW | — | — |

**TST-A2 · partial-branch-coverage**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `TST-A2A` | growth-blind-invariant-check | MEDIUM | — | — |
| `TST-A2B` | untested-error-handling-path | MEDIUM | — | — |
| `TST-A2C` | untested-fallback-default-branch | MEDIUM | — | — |
| `TST-A2D` | untested-malformed-or-boundary-input | MEDIUM | — | — |
| `TST-A2E` | single-case-enum-mapping-coverage | LOW | — | — |
| `TST-A2F` | untested-negative-boolean-branch | LOW | — | — |

**TST-A3 · shallow-scenario-coverage**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `TST-A3A` | mocked-or-absent-integration-path | MEDIUM | — | — |
| `TST-A3B` | unverified-planted-fixture-detection | MEDIUM | — | — |
| `TST-A3C` | narrow-scenario-matrix | LOW | — | — |

**TST-A4 · tooling-and-output-validation**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `TST-A4A` | unvalidated-subprocess-output-format | MEDIUM | — | — |
| `TST-A4B` | unvalidated-tool-output-schema | MEDIUM | — | — |
| `TST-A4C` | unenforced-fixture-presence-check | LOW | — | — |

### TST-B · assertion-quality

**TST-B1 · weak-and-incomplete-assertions**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `TST-B1A` | regression-test-verifies-wrong-property | MEDIUM | — | — |
| `TST-B1B` | substring-instead-of-structural-assertion | MEDIUM | — | — |
| `TST-B1C` | truthy-or-presence-only-assertion | MEDIUM | — | — |
| `TST-B1D` | unverified-critical-mock-argument | MEDIUM | — | — |
| `TST-B1E` | missing-positive-assertion | LOW | — | — |
| `TST-B1F` | universal-invariant-only-example-tested | LOW | — | — |

**TST-B2 · vacuous-and-tautological-tests**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `TST-B2A` | always-true-assertion | HIGH | — | — |
| `TST-B2B` | environment-branch-vacuous-test | MEDIUM | — | — |
| `TST-B2C` | incomplete-loop-assertion-coverage | MEDIUM | — | — |
| `TST-B2D` | inverted-logic-assertion | MEDIUM | — | — |

**TST-B3 · fragile-and-gameable-assertions**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `TST-B3A` | unsafe-index-based-assertion | HIGH | — | — |
| `TST-B3B` | unmanaged-golden-snapshot-assertion | LOW | — | — |

### TST-C · test-design

**TST-C1 · discovery-and-organization**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `TST-C1A` | test-defined-after-main-guard | MEDIUM | — | — |
| `TST-C1B` | undiscoverable-test-function | LOW | — | — |

**TST-C2 · duplication-and-reuse**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `TST-C2A` | monolithic-test-module | MEDIUM | CWE-710 | — |
| `TST-C2B` | duplicated-test-helper-across-cases | LOW | — | — |

**TST-C3 · naming-and-intent-mismatch**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `TST-C3A` | unrepresentative-test-input | MEDIUM | — | — |
| `TST-C3B` | misleading-test-name | LOW | — | — |
| `TST-C3C` | misnamed-helper-inverted-semantics | LOW | CWE-710 | — |
| `TST-C3D` | misnamed-test-artifact | LOW | CWE-561, CWE-1041 | — |

**TST-C4 · test-double-fidelity**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `TST-C4A` | incomplete-test-double-masks-behavior | MEDIUM | — | — |
| `TST-C4B` | inconsistent-mocking-pattern | MEDIUM | CWE-710, CWE-1099 | — |
| `TST-C4C` | mock-asserts-internal-behavior-not-output | LOW | — | — |
| `TST-C4D` | undocumented-test-double-contract | LOW | — | — |

**TST-C5 · test-hygiene-and-setup**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `TST-C5A` | missing-import-for-referenced-symbol | MEDIUM | — | — |
| `TST-C5B` | overengineered-fixture-builder | MEDIUM | — | — |
| `TST-C5C` | nonstandard-import-placement | LOW | — | — |
| `TST-C5D` | unexplained-magic-value-in-test | LOW | — | — |

### TST-D · isolation-hermeticity

**TST-D1 · state-and-resource-cleanup**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `TST-D1A` | manual-state-patch-without-context-manager | MEDIUM | — | — |
| `TST-D1B` | unclosed-file-handle | MEDIUM | — | — |
| `TST-D1C` | unscoped-env-var-mutation | MEDIUM | — | — |

**TST-D2 · filesystem-path-hermeticity**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `TST-D2A` | cwd-relative-fixture-path | MEDIUM | CWE-710 | — |
| `TST-D2B` | hardcoded-shared-tmp-path | MEDIUM | — | — |

### TST-E · fixtures-test-data

**TST-E1 · fixture-hygiene**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `TST-E1A` | unvalidated-fixture-existence-assumption | HIGH | — | — |
| `TST-E1B` | orphaned-unused-fixture | LOW | CWE-561 | — |

**TST-E2 · fixture-fidelity-and-drift**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `TST-E2A` | degenerate-fixture-values | MEDIUM | — | — |
| `TST-E2B` | fixture-lockfile-version-drift | MEDIUM | — | — |
| `TST-E2C` | hardcoded-machine-specific-path-in-fixture-data | LOW | — | — |
| `TST-E2D` | unrealistic-synthetic-fixture-data | LOW | — | — |

### TST-F · flakiness-determinism

**TST-F1 · skip-and-environment-gated-execution**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `TST-F1A` | cascading-skip-guard-chain | HIGH | — | — |
| `TST-F1B` | environment-gated-test-execution | MEDIUM | — | — |
| `TST-F1C` | unexpected-outcome-silently-skipped | MEDIUM | — | — |
| `TST-F1D` | unseeded-randomness-dependent-test | MEDIUM | — | — |
| `TST-F1E` | wall-clock-dependent-test | MEDIUM | — | — |
| `TST-F1F` | unisolated-external-service-call | LOW | — | — |

**TST-F2 · ambiguous-pass-signals**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `TST-F2A` | unverified-test-selection-filter | HIGH | — | — |
| `TST-F2B` | exit-code-conflates-pass-with-no-op | MEDIUM | — | — |
| `TST-F2C` | test-order-coupling | MEDIUM | — | — |

### TST-G · suite-architecture

**TST-G1 · organization**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `TST-G1A` | test-suite-sys-path-import-hack | HIGH | CWE-710, CWE-1041 | — |
| `TST-G1B` | test-fixture-scaffolding-duplicated-across-files | MEDIUM | CWE-1041 | — |
| `TST-G1C` | unit-and-integration-tests-not-separated | MEDIUM | CWE-710 | — |

**TST-G2 · hygiene-and-consistency**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `TST-G2A` | inconsistent-import-convention-in-test-methods | MEDIUM | CWE-710 | — |
| `TST-G2D` | hardcoded-test-constant-duplicated | LOW | CWE-1041 | — |
| `TST-G2E` | inconsistent-assertion-style-in-test-suite | LOW | CWE-710 | — |
| `TST-G2F` | missing-test-module-documentation | LOW | CWE-1059 | — |

**TST-G3 · coverage-and-verification-gaps**

| Code | Issue | Severity | CWE | Notes |
|---|---|---|---|---|
| `TST-G3A` | exit-code-remap-path-never-exercised-by-tests | MEDIUM | — | — |
| `TST-G3B` | long-running-subprocess-test-has-no-timeout | MEDIUM | CWE-400 | — |
| `TST-G3D` | test-fixture-not-validated-against-authoritative-source | MEDIUM | — | — |
| `TST-G3E` | security-critical-path-only-unit-tested-never-e2e | LOW | — | — |
| `TST-G3F` | weak-test-assertion-doesnt-verify-real-behavior | LOW | — | — |

