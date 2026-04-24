---
name: mkt-segment-report
description: Use when user want to trigger a report about segmentation
user-invocable: true
---


# Phase 1: Context discovery
**User must provide:**
- Scope: user segment / merchant segment / lookalike / attribute
- Focus: segment size, attribute usage, lookalike performance, data quality
- Date range nếu phân tích time-series

**Claude will infer**:
- Table tier: DM_(dimension)
- Go to the [[data_catalog/skill.md]] to get data catalog and related data tables to query.

**Claude will ask if missing**
- Cần segment usage hay live segment (rebuild segment?)
- Đề xuất thời gian là từ tháng 1/2026 đến hiện tại.


# Phase 2: Content Discovery (New Presentations)
Ask ALL questions in a single AskUserQuestion call so the user fills everything out at once:

Question 1 — Purpose (header: "BU Scope"): What BU you want to analyse? Options: Cinema / Utilities / EPS / Other (input) 

Question 2 — Length (header: "Content"): Which content you want to report? Options (multiple choice): 
- Segment size analysis
- Tìm attribute đang được dùng nhiều/ít/stale
- Theo dõi lookalike segment
- Theo dõi performance của các campaign 
- Monitor CDP data quality (SLA rate, missing attribute)
- Phân tích live segment tracking: update frequency
- Phân tích cost: cost performance

# Do not use when
- Cần noti performance metrics → No support, tell user to use `mkt-noti`
- Cần journey goal conversion → No support, tell user to use `mkt-journey`
- Cần cross-channel attribution → No support, tell user to use `mkt-attribution`

Question 3 — How deep of report you want? Option: Report only / Report with Insight

| Mode | Trigger | Output |
|------|---------|--------|
| Report Only | "segment này có bao nhiêu user", "attribute nào đang dùng" | Single metric + context |
| Report with insight | "report and give slight insight" | Breakdown table + insight |

Question 4: Adding Information (header: "Business Knowledge") Share your information that helps us to have information to harner the insights (such as is there any events that may affect the performance metrics)? 
- Allow user to input
- No input

