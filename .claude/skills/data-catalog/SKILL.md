---
name: segment-data-catalog
description: MKT Segmentation & CDP analysis — segment performance, attribute usage, lookalike performance, live segment tracking, user/merchant profiling
user-invocable: false
---

# I. Metric Definition:
| Metric | Định nghĩa | 
| Average segment size | average segment size of segment having size > 0 | 
| User adoption | % Creators use attribute / All Creators |
| Segment adoption | % Segment use attributes / All segments |
| Live Attributes | Attribute has status = LIVE |
| Condition (Enable) | Enable conditions



# II. Data model knowledge:
tables are in project .VISHNU
## Table hierachy

### 1. Attribute, condition view
**When to use**: When user ask about attribute, condition information, and how they are used.
```
Raw Tags (VISHNU_USER_*/VISHNU_MERCHANT_MASTER_ATTRIBUTE)
  ↓
D_ATTRIBUTE / D_CONDITION  ← base catalog from CDP system (dim tables about conditions and attributes)
  ↓
DM_ATTRIBUTE / DM_CONDITION  ← enriched dimensions for attribute and conditions
  ↓
DM_CONDITION_LATEST_USE_IN_SEGMENT ← information about last use of condition/attribute to create a segment.
```
### 2. Segment view
**when to use**: when user ask about segmentation usage performance, segment size and performance of segments
```
DM_SEGMENT (all version snapshot of segments, having attributes and conditions that create the segment, like to the #1. Attribute, condition view to enrich information)
  ↓
DM_SEGMENT_LATEST ← get the latest version of segments (get segment size metrics from here)
  ↓
D_SEGMENT_GOAL ← segments that are activated in marketing channels (notification, journey, promotion, advertising and widget) through campaigns
```

### 3. Live segment / Rebuild segments view
DM_SEGMENT (all version snapshot of segments, having attributes and conditions that create the segment, like to the #1. Attribute, condition view to enrich information)
  ↓
LIVE_SEGMENT_TRACKING_V3 <- rebuild version of segment, frequency to rebuild a segment, operation monitoring


##  Key tables
| Table | Schema | Granularity | Dùng khi |
|-------|--------|-------------|---------|
| `DM_SEGMENT` | VISHNU | segment × date | Segment catalog với creator, condition, pool |
| `DM_ATTRIBUTE` | VISHNU | attribute × snapshot_date | Attribute catalog + usage tracking |
| `DM_CONDITION` | VISHNU | condition × date | BQ condition catalog |
| `LIVE_SEGMENT_TRACKING_V3` | MBI_DA | segment × date (3x/day) | Live size, update freq, cost |
| `F_LOOKALIKE_PERFORMANCE_RAW` | VISHNU | user × campaign × channel × date | Raw lookalike performance |
| `D_LOOKALIKE_SEGMENT_CAMPAIGN_META` | VISHNU | segment × campaign | Lookalike config |
| `CDP_VALIDATION_DAILY` | VISHNU | attribute × date | Data quality: row count vs threshold |
| `REBUILD_SEGMENT_OUTPUT` | VISHNU | segment × date | Rebuild tracking |

**Merchant-specific:**

| Table | Schema | Dùng khi |
|-------|--------|---------|
| `MERCHANT_INFO` | VISHNU_MERCHANT | Merchant master dim |
| `VISHNU_MERCHANT_MASTER_ATTRIBUTE_{DtFlag}` | MBI_DA | 12 merchant attributes |
| `alert_cdp_table` | MBI_DA | Merchant CDP SLA monitoring |


# III. Metadata definition

## 1. Segment types

```
CDP        → VISHNU attributes (tag-based)
BQ         → Custom BigQuery conditions
lookalike  → ML-based lookalike từ seed audience
```

## 2. Attribute metadata dimensions

| Dimension | Values |
|-----------|--------|
| **By Categorized** | BEHAVIOURS (~84%), DEMOGRAPHICS (~12%), GEOGRAPHICS (~2%), PSYCHOGRAPHICS, UNKNOWN |
| **By Source** | BATCH_INPUT (~73%), STREAMING (~26%), others |
| **By Type** | STANDARD (~54%), EXTENDED (~46%) |
| **By Integration Level** | TAG_ID (~94%), PARTIAL_VALUE_BY_TAG (~3%), PARTIAL_VALUE (~3%), UNKNOWN |

## 3. Attribute status lifecycle

```
SUBMIT → APPROVE → LIVE → USED_CREATE_SEGMENT
         (89%)    (73%)

Other statuses: DISABLED, REJECTED, FAILED_TO_SYNC, WAITING_FOR_APPROVE,
                STAGING, DRAFT, COMPLETED, DELETED

L90D thresholds:
  Used in L90D    = attribute được dùng trong segment trong 90 ngày gần nhất
  Unused >90D     = LIVE nhưng không dùng >90 ngày → candidates for cleanup
```

## 4. Attribute/Condition healh:
**Attribute**
- Total attribute -> live attribute (attribute status = LIVE) -> Attribute used to create segment in L90D (absolute value and percentage value)
- Total conditions -> enable conditions (attribute status = ENABLE) -> Conditions used to create segment in L90D vs Conditions not used in L90D (absolute value and percentage value)

## 5. Live segment (rebuild types)
- Rebuild frequency: DAY, WEEK, HOUR
- Rebuild volume

## 6. Cost performance BQ
```
Actual_cost = On-demand cost * $6.25 + Shared Slot * $0.06/hour
Jobs_id     = Số lượng job query mỗi khi load 1 page/component
Max Loading = Thời gian dài nhất để hoàn thành 1 job

Cost breakdown (ref):
  Create Table Push Noti - Phone Info: 73.1% of cost
  Estimate:                            24.5%
  Adhoc Query:                         minimal

Service accounts:
  hermes@momovn-prod.iam.gserviceaccount.com
  opencdp-prod@momovn-prod.iam.gserviceaccount.com
```

## 7. Lookalike performance:
Metrics per tag:
  login_user, visitor, campaign_impression, click, CTR_noti
  Comparison: lookalike vs random (baseline)
Campaign status logic:
  FINISHED / COMPLETED → có data (campaign đã setup và chạy)
  Các status khác      → chưa có data (campaign chưa chạy)

## Segmentation Campaign performance:
Metrics: Impression, Click, CTR
Use table: 



* Format show:
- When show information, done show id, show the segment_name, attribute_name_id, condition_name so that easy to read.
- 