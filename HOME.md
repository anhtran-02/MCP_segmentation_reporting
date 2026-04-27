---
title: Segment Analysis MCP — Vault Home
tags: [index, mcp, segmentation]
---

# Segment Analysis MCP

> MoMo CDP segmentation analysis platform. Use this vault to navigate skills, schema, and prompting context for Claude.

---

## Core Context Files

| File | Purpose |
|------|---------|
| [[CLAUDE.md]] | Master context — auto-loaded by Claude Code every session |
| [[MCP_KNOWLEDGE_BASE]] | How MCP works, tool routing, prompts vs skills reference |
| [[readme]] | Project overview and setup |

---

## Skills Map

```
/mkt-segment-report  ──┐
                        ├──► [[.claude/skills/data-catalog/SKILL|data-catalog]]  (schema + metrics)
                        ├──► [[.claude/skills/report_tool/SKILL|report_tool]]    (query functions)
                        └──► [[.claude/skills/report-helper/BU-analysis|BU-analysis]] (per-BU reports)
                                    │
                                    └──► frontend-slides  (HTML presentation)
```

### Skills Detail

- [[.claude/skills/SKILL|mkt-segment-report]] — Entry point. Scopes BU, content type, report depth.
- [[.claude/skills/data-catalog/SKILL|data-catalog]] — VISHNU schema, metric definitions, attribute lifecycle.
- [[.claude/skills/report_tool/SKILL|report_tool]] — 6 report functions: team overview, condition analysis, size distribution, creator profiling, segment health, recommendations.
- [[.claude/skills/report-helper/BU-analysis|BU-analysis]] — `list_bu_name`, `preview_bu_report`, `generate_slide_bu_report`, `executive_summary`.

---

## MCP Tools (bu-report-mcp server)

| Tool | Trigger phrase |
|------|---------------|
| `list_bu_names` | "What BUs are available?" |
| `preview_bu_report(bu_name)` | "How is Cinema doing?" |
| `generate_bu_report(bu_name)` | "Generate the Cinema report" |

| Prompt | Workflow |
|--------|----------|
| `analyze_bu` | Deep dive — KPIs, conditions, issues, operator profiles |
| `executive_summary` | Concise 5-line card per BU |
| `compare_bus` | Side-by-side BU comparison |
| `analyze_all_bus` | Fleet health across all BUs |
| `generate_all_reports` | Batch PowerPoint generation |

---

## Domain Quick Reference

| Term | Definition |
|------|-----------|
| **BU** | Business Unit → Cinema · Utilities · EPS · Other |
| **CDP segment** | Built from VISHNU tag attributes |
| **BQ segment** | Built from custom BigQuery conditions |
| **Lookalike** | ML-based audience expansion from seed segment |
| **Live segment** | Rebuilt DAY / WEEK / HOUR |
| **Creator** | Marketing operator who builds segments |
| **Pool size** | Estimated user count before activation |
| **Attribute lifecycle** | SUBMIT → APPROVE → LIVE → USED_CREATE_SEGMENT |

---

## Key Tables (VISHNU schema, BigQuery `momovn-prod`)

| Table | Granularity | Key use |
|-------|-------------|---------|
| `DM_SEGMENT` | segment × date | Catalog, pool size, creator |
| `DM_ATTRIBUTE` | attribute × snapshot_date | Usage, status, category |
| `DM_CONDITION` | condition × date | BQ condition catalog |
| `LIVE_SEGMENT_TRACKING_V3` | segment × date 3×/day | Rebuild freq, live size, cost |
| `F_LOOKALIKE_PERFORMANCE_RAW` | user × campaign × channel × date | Lookalike CTR, impressions |
| `CDP_VALIDATION_DAILY` | attribute × date | SLA: row count vs threshold |

---

## Out of Scope

- Notification performance → `mkt-noti`
- Journey goal conversion → `mkt-journey`
- Cross-channel attribution → `mkt-attribution`
