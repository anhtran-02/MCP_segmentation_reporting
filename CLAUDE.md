# Segment Analysis MCP

MoMo CDP marketing segmentation analysis platform. Analyzes user/merchant segments, CDP attributes, lookalike performance, and live segment tracking for internal BU teams.

MCP server: `bu-report-mcp/`

---

## Skill Routing

| User intent | Invoke | Notes |
|-------------|--------|-------|
| Trigger a segmentation report | `/mkt-segment-report` | Entry point — scopes BU, content type, depth |
| Look up schema, table names, metric definitions | `data-catalog` | VISHNU BigQuery schema reference |
| Query data / call report functions | `report_tool` | Team overview, condition analysis, size distribution |
| BU-specific report (Cinema / EPS / etc.) | `BU-segmentation-report` | Preview → generate → exec summary per BU |
| Build HTML slides from report data | `frontend-slides` | Zero-dependency self-contained HTML |

**Do NOT use this system for:** noti performance (`mkt-noti`), journey goal conversion (`mkt-journey`), cross-channel attribution (`mkt-attribution`).

---

## Domain Vocabulary

| Term | Meaning |
|------|---------|
| **BU** | Business Unit → Cinema, Utilities, EPS, Other |
| **CDP segment** | Built from VISHNU tag attributes |
| **BQ segment** | Built from custom BigQuery conditions |
| **Lookalike** | ML-based audience expansion from a seed segment |
| **Live segment** | Rebuilt on DAY / WEEK / HOUR schedule |
| **Creator** | Marketing operator who builds segments |
| **Condition** | A filter rule inside a segment (attribute OR BQ condition) |
| **Attribute** | A user property tag; lifecycle: SUBMIT → APPROVE → LIVE → USED |
| **Pool size** | Estimated user count for a segment before activation |

---

## Data Schema (Quick Reference)

Schema: `VISHNU` (BigQuery project `momovn-prod`)

| Table | Granularity | Use case |
|-------|-------------|----------|
| `DM_SEGMENT` | segment × date | Segment catalog, creator, condition count, pool size |
| `DM_ATTRIBUTE` | attribute × snapshot_date | Attribute catalog + usage tracking |
| `DM_CONDITION` | condition × date | BigQuery condition catalog |
| `LIVE_SEGMENT_TRACKING_V3` | segment × date (3×/day) | Rebuild frequency, live size, cost |
| `F_LOOKALIKE_PERFORMANCE_RAW` | user × campaign × channel × date | Raw lookalike performance |
| `CDP_VALIDATION_DAILY` | attribute × date | Data quality: row count vs SLA threshold |

Full schema + all metric definitions → `.claude/skills/data-catalog/SKILL.md`

---

## MCP Server Tools & Prompts

**Tools:** `list_bu_names` · `preview_bu_report(bu_name)` · `generate_bu_report(bu_name)`

**Prompts:** `analyze_bu` · `executive_summary` · `compare_bus` · `analyze_all_bus` · `generate_all_reports`

Routing rules for business users → see Skill Routing table above

---

## Report Workflow (Standard)

```
1. Scope BU → /mkt-segment-report (Phase 1 + 2)
2. Query data → report_tool functions
3. BU deep-dive → BU-segmentation-report (preview_bu_report → generate_slide_bu_report)
4. Present → frontend-slides
```
