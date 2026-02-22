<!-- Change log
v2 2026-02-16: Revised after four-role review — added pre-release checklist, clarified runtime vs pre-deployment roles, and made mitigation trigger order explicit
v1 2026-02-16: First draft
-->

# Chapter 4 Verification and Validation Framework

---

> **Key Insight Box**
>
> In critical water infrastructure, autonomy without verification is not innovation; it is unmanaged risk. Trust must be engineered through reproducible evidence.

## Why verification is the architecture’s proof of trust

Chapter 3 defined how autonomous water networks should be built. This chapter addresses how those designs are proven safe and reliable before and during deployment. The core proposition is simple: autonomy claims are valid only if they are backed by traceable evidence under defined Operational Design Domain (ODD) conditions.

## SIM-SIL-HIL as the staged evidence pipeline

CHS adopts a staged verification chain:

- **SIM (Model-in-the-loop simulation)**: verifies dynamic consistency and scenario coverage;
- **SIL (Software-in-the-loop)**: verifies executable control logic and software interfaces;
- **HIL (Hardware-in-the-loop)**: verifies real-time performance, IO behavior, and fallback actions.

Each stage has different failure signatures and release criteria. Skipping stages compresses schedule but amplifies deployment risk.

[Figure 4-1: SIM-SIL-HIL verification pipeline]
{Description: Sequential pipeline showing entry criteria, test activities, and release gates for SIM, SIL, and HIL. Include feedback loops for defect correction.}
{Size: full page}
{Color scheme: blue theme}

## ODD-based test design

Verification is not “test everything”; it is “test what matters in declared ODD.” A practical ODD-based design includes:

1. boundary condition set (flow, level, communication quality, asset availability),
2. disturbance set (demand fluctuation, inflow pulses, sensor noise),
3. failure-injection set (component outage, packet loss, delayed actuation),
4. exit and takeover criteria.

This approach aligns test scope with autonomy claims and avoids false confidence.

## Runtime monitoring and safety enforcement

Pre-deployment verification is necessary but not sufficient. Runtime monitoring complements—rather than replaces—pre-deployment verification by continuously evaluating:

- ODD compliance,
- Safety Envelope margins,
- control action plausibility,
- model drift indicators,
- human takeover readiness.

When violations are detected, systems should execute a fixed mitigation order: constrain action first, degrade mode second, and trigger accountable human takeover third.

## Coverage metrics and acceptance criteria

CHS verification recommends multi-axis coverage rather than single test counts:

- **Scenario coverage**: representative normal + abnormal conditions,
- **Constraint coverage**: safety and operational boundaries exercised,
- **Interface coverage**: control and data contracts under stress,
- **Governance coverage**: takeover/audit workflows executed.

[Table 4-1: Minimum acceptance criteria for autonomy release]
| Dimension | Minimum evidence | Decision rule |
|---|---|---|
| Dynamic validity | Stable and bounded responses in declared ODD slices | pass/fix |
| Safety compliance | No unresolved red-zone violations in critical scenarios | pass/fix |
| Real-time behavior | Timing and fallback performance within limits | pass/fix |
| Governance readiness | Takeover drills and audit trails reproducible | pass/fix |

## Pre-release checklist (minimum deployment gate)

| Gate | Minimum condition |
|---|---|
| SIM gate | Scenario library executed with reproducible results |
| SIL gate | Control software and interfaces pass regression suite |
| HIL gate | Real-time and fallback behaviors satisfy timing limits |
| Safety gate | ODD and Safety Envelope triggers are enforceable |
| Governance gate | Takeover roles and audit chain pass drill validation |

## Regression testing and controlled evolution

Any model, policy, or software update must trigger regression tests across the preserved scenario baseline. Controlled evolution requires versioned artifacts, reproducible test environments, change impact mapping, and rollback paths. This discipline supports reproducibility across organizations and sites.

## Common verification anti-patterns

Frequent failures include:

- validating only nominal conditions,
- using non-repeatable ad hoc test benches,
- separating technical tests from governance drills,
- promoting pilots without regression evidence.

These anti-patterns create invisible risk accumulation.

## Chapter summary and bridge to Chapter 5

This chapter established the verification and validation framework for autonomous water networks: SIM-SIL-HIL pipeline, ODD-based test design, runtime monitoring, coverage metrics, and regression discipline. With trust evidence defined, Chapter 5 turns to case studies and shows how this framework performs in Jiaodong Water Transfer and Shaoping Hydropower contexts.
