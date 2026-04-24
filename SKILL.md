---
name: mkt-segment
description: MKT Segmentation & CDP analysis — segment performance, attribute usage, lookalike performance, live segment tracking, user/merchant profiling
user-invocable: true
---

# Skill: MKT Segmentation & CDP Analysis

> Phân tích CDP platform cho MoMo MKT Platform
> Core: `VISHNU.DM_SEGMENT` + `VISHNU.DM_ATTRIBUTE` + `MBI_DA.LIVE_SEGMENT_TRACKING_V3`

---

## ─── LAYER 02: Context Requirements ────────────────

## Context requirements

**User must provide:**
- Scope: user segment / merchant segment / lookalike / attribute
- Focus: segment size, attribute usage, lookalike performance, data quality
- Date range nếu phân tích time-series

**Claude will infer:**
- Table tier: DM_ (dimension) vs raw tag tables vs validation tables
- CDP_UID_TYPE: MOMO_AGENT_ID (user) vs MOMO_MERCHANT_CODE (merchant)
- Segment type: CDP / BQ / lookalike

**Claude will ask if missing:**
- Specific segment_id / attribute_name_id / team/department cần filter?
- Cần live tracking hay historical trend?

---

## ─── LAYER 03: Usage Boundary ──────────────────────

## When to use

- Phân tích segment size, composition, và health
- Tìm attributes nào đang được dùng nhiều / ít / stale
- Theo dõi lookalike campaign performance (Ads + Noti + Promo channels)
- Monitor CDP data quality (SLA rate, missing attributes)
- Phân tích user/merchant behavior profile (RFM, KYC, transaction patterns)
- Live segment tracking: update frequency, cost performance

**Trigger keywords:** "segment", "attribute", "CDP", "lookalike", "RFM", "user profile", "merchant profile", "tag", "condition", "DM_SEGMENT", "VISHNU"

## Do NOT use when

- Cần noti performance metrics → `mkt-noti`
- Cần journey goal conversion → `mkt-journey`
- Cần cross-channel attribution → `mkt-attribution`

---

## ─── LAYER 04: Priority & Conflict ─────────────────

## Priority

Dominates khi request mention **"segment"**, **"attribute"**, **"CDP"**, **"VISHNU"**, **"lookalike"**, **"user profile"**.

## Conflict resolution

- Overlap với `mkt-noti`: Segment có notification settings attributes nhưng delivery performance = mkt-noti
- Overlap với `analyst`: Segment xử lý audience/profile analysis, analyst xử lý media performance

---

## ─── LAYER 05: Usage Mode ──────────────────────────

## Usage mode

| Mode | Trigger | Output |
|------|---------|--------|
| Quick | "segment này có bao nhiêu user", "attribute nào đang dùng" | Single metric + context |
| Full | "phân tích segment composition", "attribute usage trend" | Breakdown table + insight |
| Strategic | "segment nào cần rebuild", "lookalike nào hiệu quả nhất" | Full + health score + recommendation |

---

## ─── LAYER 06: Thinking Framework ─────────────────

## Dashboard structure (5 tabs)

| Tab | Mục đích |
|-----|---------|
| **Segments** | Health check: total, creators, adoption, attribute/condition mix, live attributes, enabled conditions |
| **Attributes** | OKR progress (Live Attrs), asset quality (Used/Unused L90D), phân loại by type/source/integration |
| **Conditions** | Enabled conditions + usage within last 90 days |
| **Live Segment** | Config rebuild, total rebuild count, rebuild frequency (DAY/WEEK/HOUR) |
| **Lookalike** | Segment–campaign mapping, CTR noti vs random (data từ 10.3.2025) |

⚠️ **Date Range vs Latest Status:**
- Date Range filter = áp dụng cho time-based charts, trend visualizations
- "Latest status" = snapshot mới nhất, KHÔNG bị ảnh hưởng bởi Date Range

## Segment KPIs & OKR targets

| Metric | Định nghĩa | OKR / Benchmark |
|--------|-----------|----------------|
| **Segments** | Total segments (condition/attribute/custom/lookalike) | — |
| **Average Segment Size** | Avg size của segments có size > 0 | OKR tracked |
| **User Adoption** | % Creators dùng Attribute / All Creators | ~74% |
| **Segment Adoption** | % Segments dùng Attribute / All Segments | ~44.69% |
| **Live Attributes** | Attributes ở status LIVE | OKR target: **500** |
| **Conditions (Enable)** | Enabled conditions | ~748 |

### Segment platform types

| Platform | Định nghĩa | % (ref) |
|----------|-----------|---------|
| `SEGMENT_HAS_CONDITION` | Tạo trên Segment V1/V2 với condition | ~55.7% |
| `ATHENA` | Tạo qua Athena platform | ~40.8% |
| `CUSTOM_SEGMENT` | Custom list (upload phone/agentId) | ~2.2% |
| `LOOKALIKE_SEGMENT` | ML-based lookalike từ seed | ~0.9% |
| `STANDARD_CREATE_API` | Tạo qua API | ~0.3% |

### Segment classification (by attribute/condition usage)

| Category | Định nghĩa | % (ref) |
|----------|-----------|---------|
| `Only condition` | Chỉ dùng BQ condition | ~33.1% |
| `Only attribute` | Chỉ dùng CDP attribute | ~30.2% |
| `Both` | Dùng cả condition + attribute | ~12.9% |
| `No condition, No attribute` | Không dùng cái nào | ~23.8% |

## Data model knowledge

### Table hierarchy

```
Raw Tags (VISHNU_USER_*/VISHNU_MERCHANT_MASTER_ATTRIBUTE)
  ↓
D_ATTRIBUTE / D_CONDITION  ← base catalog from CDP system
  ↓
DM_ATTRIBUTE / DM_SEGMENT / DM_CONDITION  ← enriched dimensions
  ↓
LIVE_SEGMENT_TRACKING_V3  ← operational monitoring
  ↓
F_LOOKALIKE_PERFORMANCE_RAW  ← cross-channel perf
```

### Key tables

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

### Segment types

```
CDP        → VISHNU attributes (tag-based)
BQ         → Custom BigQuery conditions
lookalike  → ML-based lookalike từ seed audience
```

### Attribute metadata dimensions

| Dimension | Values |
|-----------|--------|
| **By Categorized** | BEHAVIOURS (~84%), DEMOGRAPHICS (~12%), GEOGRAPHICS (~2%), PSYCHOGRAPHICS, UNKNOWN |
| **By Source** | BATCH_INPUT (~73%), STREAMING (~26%), others |
| **By Type** | STANDARD (~54%), EXTENDED (~46%) |
| **By Integration Level** | TAG_ID (~94%), PARTIAL_VALUE_BY_TAG (~3%), PARTIAL_VALUE (~3%), UNKNOWN |

### Attribute status lifecycle

```
SUBMIT → APPROVE → LIVE → USED_CREATE_SEGMENT
         (89%)    (73%)

Other statuses: DISABLED, REJECTED, FAILED_TO_SYNC, WAITING_FOR_APPROVE,
                STAGING, DRAFT, COMPLETED, DELETED

L90D thresholds:
  Used in L90D    = attribute được dùng trong segment trong 90 ngày gần nhất
  Unused >90D     = LIVE nhưng không dùng >90 ngày → candidates for cleanup
```

### Attribute health benchmarks (ref Apr 2026)

| Metric | Value |
|--------|-------|
| Total Attributes (all status) | ~599–711 |
| Live Attributes | 327 (OKR target: **500**, ~65.4% goal) |
| Used in L90D (of Live) | 179 (~54.7%) |
| Unused >90D (of Live) | 148 (~45.3%) |

### Top used attributes (by # segments)

| Attribute | Category | Group | Segments |
|-----------|----------|-------|---------|
| `user_blacklist_risk` | DEMOGRAPHICS | Account Information | 812 |
| `user_created_segment` | SYSTEMS | — | 779 |
| `user_active_in_range` | BEHAVIOURS | Transactions Information | 246 |
| `user_login_in_range` | BEHAVIOURS | Interaction Information | 197 |
| `user_age_group_age` | DEMOGRAPHICS | PII Information | 163 |
| `user_account_staff_by_work_place` | DEMOGRAPHICS | — | 60 |
| `user_location_most_city_a30` | GEOGRAPHICS | Spatial Location | 58 |
| `user_project_noti_device_setting` | BEHAVIOURS | — | 48 |
| `user_kyc_nfc_verified_status_detail` | DEMOGRAPHICS | — | 46 |

### Key attribute categories (user)

| Category | Attributes tiêu biểu |
|----------|---------------------|
| Demographic | age_group, gender, location_city, kyc_status |
| Transaction | bu_name_gmv, service_code_count, merchant_count |
| RFM | offline_rfm_type (best/good/at_risk/lost), rfm_score |
| Engagement | login_7day/30day, visit_daily, follow_oa |
| Financial | credit_score_tier (G1-G10), bank_account_linked |
| Journey | journey_goal_campaign_detail (goal per campaign) |
| Advertising | ads_retarget_eligible, special_segment |

### Condition health

```
Total Enabled: 748
  YES use in L90D: 219 (29.3%)  → Healthy
  NO use in L90D:  529 (70.7%)  → Stale candidates

L90D = được dùng trong segment trong 90 ngày gần nhất
Data available: Sep 30, 2023 – Jan 25, 2026
```

### Live Segment (rebuild) types

| Type | Mô tả | % |
|------|-------|---|
| `FIXED` | Snapshot cố định | ~57.8% |
| `TIME_WINDOW` | Rolling window (vd 30 ngày gần nhất) | ~39.7% |
| `FIXED_TO_WINDOW` | Fixed start, rolling end | ~2.5% |

```
Rebuild frequency: DAY (~98.5%), WEEK (~1.4%), HOUR (~0.1%)
Daily rebuild volume: ~1,875–2,124 segments/day
```

### Cost Performance BQ

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

### Lookalike Performance

```
Data available from: 10.3.2025
Creators: 11 | Segments: 35 | Adoption: ~0.92%

Campaign status logic:
  FINISHED / COMPLETED → có data (campaign đã setup và chạy)
  Các status khác      → chưa có data (campaign chưa chạy)

Metrics per tag per day:
  login_user, visitor, campaign_impression, click, CTR_noti
  Comparison: lookalike vs random (baseline)
```

### Key attribute categories (merchant)

| Attribute | Values |
|-----------|--------|
| merchant_size | small / medium / large |
| merchant_aov | 0-40k / 40-70k / 70-190k / 190k-2000k / 2000k+ |
| merchant_location_city | Hanoi / HCM / etc. |
| merchant_active_in_range | 30/60/90 day activity flags |
| merchant_acquired_in_range | 30/60/90 day acquisition cohort |
| merchant_bu_group_code_l1-l4 | Hierarchical business category |

### Lookalike performance channels

```
Ads:    GR_ADVERTISING.2022_DM_ADVERTISING_DAILY_LONG_TABLE_CAA_REVAMP_2025
Noti:   MBI_DA.NOTI_DAILY_V5
Promo:  MBI_DA.PROMO_EV_RAW_VOUCHER_TOUCHPOINT_EVENTS_PARAMS
```

Metrics: impression, click → CTR per channel per lookalike segment

### Live Segment Tracking (3x/day: 7:30, 12:30, 19:30)

```
Tracks per segment:
  - segment_size: current user count
  - update_frequency: how often updated
  - cost_performance: từ extract_cost_hermes.sql
  - lookalike_performance: raw → aggregated
```

### Data quality (CDP Validation)

```
sla_rate = current_day_count / avg(prior_10_days)
Alert thresholds:
  sla_rate < 0.8  → missing data (undercount)
  sla_rate > 1.2  → data spike (overcount / duplicates)
```

---

## ─── LAYER 07: Templates ───────────────────────────

## Template: Segment health check

```sql
-- Purpose: Segment catalog với size, creator, usage stats
WITH
segment_health AS (
  SELECT
    s.segment_id,
    s.segment_name,
    s.type_condition,
    s.created_by,
    s.department,
    s.team,
    s.platform,
    -- Size & usage
    l.segment_size,
    l.update_frequency,
    -- Attribute usage
    s.cnt_segment_using_this_attribute,
    s.last_used_date,
    DATE_DIFF(CURRENT_DATE(), s.last_used_date, DAY) AS days_since_last_use,
    -- Status flags
    CASE
      WHEN DATE_DIFF(CURRENT_DATE(), s.last_used_date, DAY) > 90 THEN 'stale'
      WHEN l.segment_size < 100 THEN 'too_small'
      WHEN l.segment_size > 10000000 THEN 'very_large'
      ELSE 'healthy'
    END AS health_status
  FROM `project-5400504384186300846.VISHNU.DM_SEGMENT` s
  LEFT JOIN `momovn-prod.MBI_DA.LIVE_SEGMENT_TRACKING_V3` l
    ON s.segment_id = l.segment_id
    AND l.tracking_date = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
  WHERE s.date = DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
),
final AS (
  SELECT * FROM segment_health
  ORDER BY days_since_last_use DESC, segment_size DESC
)
SELECT * FROM final
```

## Template: Attribute usage tracking

```sql
-- Purpose: Which attributes are actively used vs stale?
WITH
attribute_usage AS (
  SELECT
    attribute_name_id,
    attribute_type,
    status,
    created_by,
    department,
    team,
    cnt_segment,
    cnt_segment_name,
    last_used_date,
    latest_used_date,
    last_used_interval,
    -- Health classification
    CASE
      WHEN last_used_interval > 90  THEN 'stale'
      WHEN last_used_interval BETWEEN 30 AND 90 THEN 'low_use'
      WHEN cnt_segment >= 5 THEN 'high_demand'
      ELSE 'active'
    END AS usage_status
  FROM `project-5400504384186300846.VISHNU.DM_ATTRIBUTE`
  WHERE snapshot_date = (SELECT MAX(snapshot_date) FROM `project-5400504384186300846.VISHNU.DM_ATTRIBUTE`)
    AND status = 'ACTIVE'
),
final AS (
  SELECT * FROM attribute_usage ORDER BY last_used_interval DESC
)
SELECT * FROM final
```

## Template: Lookalike performance by channel

```sql
-- Purpose: Lookalike segment CTR across channels
WITH
perf AS (
  SELECT
    r.date,
    m.segment_id,
    m.campaign_name,
    m.created_by,
    r.channel,
    SUM(r.impression) AS impression,
    SUM(r.click)      AS click,
    ROUND(SAFE_DIVIDE(SUM(r.click), SUM(r.impression)), 4) AS ctr
  FROM `project-5400504384186300846.VISHNU.F_LOOKALIKE_PERFORMANCE_RAW` r
  JOIN `project-5400504384186300846.VISHNU.D_LOOKALIKE_SEGMENT_CAMPAIGN_META` m
    USING (segment_id)
  WHERE r.date BETWEEN '[start]' AND '[end]'
  GROUP BY 1, 2, 3, 4, 5
),
pivot AS (
  SELECT
    date, segment_id, campaign_name,
    MAX(IF(channel = 'Ads',   ctr, NULL)) AS ctr_ads,
    MAX(IF(channel = 'Noti',  ctr, NULL)) AS ctr_noti,
    MAX(IF(channel = 'Promo', ctr, NULL)) AS ctr_promo
  FROM perf
  GROUP BY 1, 2, 3
)
SELECT * FROM pivot ORDER BY date DESC, ctr_ads DESC
```

## Template: RFM segment breakdown

```sql
-- Purpose: User RFM distribution (offline channel)
WITH
rfm AS (
  SELECT
    DATE(created_at) AS tag_date,
    -- tagsAdd chứa values như 'offline_rfm_type_best', 'offline_rfm_type_at_risk'
    REGEXP_EXTRACT(tag_value, r'offline_rfm_type_(.+)') AS rfm_type,
    COUNT(DISTINCT uid) AS user_count
  FROM `project-5400504384186300846.VISHNU.VISHNU_USER_PROJECT_OFFLINE_RFM_TYPE_*`
  CROSS JOIN UNNEST(tagsAdd) AS tag_value
  WHERE valid_tag = 'valid'
    AND type_modified = 0
    AND _TABLE_SUFFIX = FORMAT_DATE('%Y%m%d', '[date]')
  GROUP BY 1, 2
),
final AS (
  SELECT * FROM rfm ORDER BY tag_date DESC, user_count DESC
)
SELECT * FROM final
```

---

## ─── LAYER 08: Output Contract ─────────────────────

## Output contract

- **Segment health:** Flag stale (>90 days unused), too_small (<100 users), SLA breach
- **Segment mix:** Always report by platform type (ATHENA/CDP/Custom/Lookalike) + by classification (Only condition / Only attribute / Both / None)
- **Attribute usage:** Show cnt_segment + last_used_interval + status + L90D flag
- **Attribute OKR:** Flag if Live Attributes < 500 (OKR target), show % toward goal
- **Condition health:** Flag conditions with NO use in L90D (70%+ unused is normal, but individual stale conditions = cleanup candidate)
- **Live segment:** Show rebuild type (FIXED/TIME_WINDOW/FIXED_TO_WINDOW) + frequency
- **Lookalike:** Compare CTR_noti vs random baseline; only report FINISHED/COMPLETED campaigns
- **Data quality:** sla_rate range [0.8, 1.2] = healthy; outside = flag
- **Privacy:** Không expose individual uid trong output — luôn aggregate
- **"Latest status" vs date range:** Luôn note rõ số là latest snapshot hay time-series

---

## ─── LAYER 09: Decision Checklist ──────────────────

## Decision checklist

- [ ] CDP_UID_TYPE đúng chưa? MOMO_AGENT_ID (user) vs MOMO_MERCHANT_CODE (merchant)
- [ ] Segment platform type rõ chưa? ATHENA / SEGMENT_HAS_CONDITION / CUSTOM / LOOKALIKE có data source khác nhau
- [ ] Segment classification rõ chưa? Only condition / Only attribute / Both / None → dùng bảng nào khác nhau
- [ ] Valid tag filter: `valid_tag = 'valid'`, `type_modified = 0`, `length(agentId) BETWEEN 5 AND 9`
- [ ] DM_ATTRIBUTE snapshot_date dùng latest date chưa? (truncate + insert pattern)
- [ ] Attribute L90D: Used vs Unused rõ chưa? Stale = Unused >90D (không dùng trong L90D)
- [ ] Attribute status = LIVE mới tính vào OKR và analytics (không dùng DISABLED/REJECTED)
- [ ] Condition: 70.7% NO use in L90D là bình thường — chỉ flag nếu user hỏi specific condition
- [ ] Live segment: biết rebuild type (FIXED/TIME_WINDOW) để estimate size staleness
- [ ] Lookalike: chỉ report nếu status = FINISHED/COMPLETED; data từ 10.3.2025 trở đi
- [ ] "Latest status" vs date-range filter: phân biệt rõ trước khi report số

## Escalation

- Segment users nhận notification → `mkt-noti`
- Segment users trong journey campaign → `mkt-journey`
- Segment users as attribution touchpoint → `mkt-attribution`
- Cần build new attribute/condition SQL → `sql-skill`
- Data quality investigation sâu → `python-dbt`
