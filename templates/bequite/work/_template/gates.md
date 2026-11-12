# Gates for this work

Each gate: state (pending / done / n/a - reason) and evidence (file or command). Project-level gates (initialized, mode, discovery, design DNA, release) live in `.bequite/state/WORKFLOW_GATES.md`.

## Core (all work)
| Gate | State | Evidence |
|---|---|---|
| `CLARIFY_ANSWERED` | pending | brief.md has answers or logged assumptions |
| `RESEARCH_COMPLETE` | pending | research.md has sourced findings |
| `SCOPE_LOCKED` | pending | spec.md approved by the user |
| `PLAN_APPROVED` | pending | plan.md approved by the user |
| `MULTI_PLAN_DECISION` | n/a | merged plan approved (only if /bq-multi-plan ran) |
| `TASKS_ASSIGNED` | pending | tasks.md has atomic tasks with profiles |
| `IMPLEMENTATION_STARTED` | pending | at least one task `[~]` or `[x]` |
| `IMPLEMENTATION_DONE` | pending | all required tasks `[x]` |
| `TESTS_PASS` | pending | evidence.md shows green tests |
| `REVIEW_APPROVED` | pending | review.md verdict Approved |
| `RED_TEAM_RESOLVED` | n/a | red-team blockers resolved (only if /bq-red-team ran) |
| `VERIFY_PASSED` | pending | verify.md verdict PASS |
| `CONVERGED` | pending | every acceptance criterion has evidence |

## Fix (type fix)
| Gate | State | Evidence |
|---|---|---|
| `BUG_REPRODUCED` | n/a | reproduction steps + failing output in evidence.md |
| `ROOT_CAUSE_IDENTIFIED` | n/a | root cause with file:line |
| `FIX_APPLIED` | n/a | smallest patch + regression test |
| `FIX_VERIFIED` | n/a | symptom gone; test green |

## Feature (type feature)
| Gate | State | Evidence |
|---|---|---|
| `FEATURE_TYPE_IDENTIFIED` | n/a | feature type recorded in README.md |
| `FEATURE_SPEC_APPROVED` | n/a | spec.md approved |
| `FEATURE_IMPLEMENTED` | n/a | tasks done |
| `FEATURE_TESTED` | n/a | tests green in evidence.md |

## Frontend / web (type web, or any UI change)
| Gate | State | Evidence |
|---|---|---|
| `DESIGN_CONTINUITY_PASS` | n/a | design continuity report for this work |
| `VISUAL_QA_DONE` | n/a | screenshots + visual QA notes |
| `PERF_BUDGET_PASS` | n/a | mobile Lighthouse run within the budget |

## Motion (type motion)
| Gate | State | Evidence |
|---|---|---|
| `SCRIPT_APPROVED` | n/a | spec.md script + beats approved |
| `STYLE_LOCKED` | n/a | styleframes approved |
| `RENDER_PLAN_APPROVED` | n/a | plan.md engine + render plan + costs approved |
| `PICTURE_LOCKED` | n/a | picture approved on a preview |
| `AUDIO_APPROVED` | n/a | voice + music + mix approved |
| `FINAL_QC_PASS` | n/a | QC commands + output in evidence.md |
| `DELIVERY_APPROVED` | n/a | deliverables approved; posting is user-run |
