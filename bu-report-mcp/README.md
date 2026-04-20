What V1 does

User says in Claude Desktop:

Create a segmentation report for BU TELCO

Your MCP tool then:

reads segmentation_usage.csv
filters rows where BU = TELCO
calculates a few KPIs
generates a simple .pptx
returns the file path

Do not start with:

auto-reading every shape from the Utilities deck
generating all BUs
advanced agent logic
perfect visual cloning

Build the dumb but working version first.
-----------
For V1, keep only 3 slides:

Slide 1 — Title + KPI summary

Show:

BU name
reporting period
total campaigns
total segments
total operators
avg conditions per segment
Slide 2 — Top conditions

Show:

top 5 most used conditions
maybe condition type if available
Slide 3 — Simple issues + recommendations

Show:

zero-condition segments count
low reuse note
naming issue note
2–3 recommendations

This is enough to prove the flow.
-----------
# Decide input and output
Input:
- bu_name: string

Fixed local files:
- data/segmentation_usage.csv
- templates/utilities_reference.pptx

Output:
- outputs/{bu_name}_report.pptx

## Example:
Input:
- bu_name: string

Fixed local files:
- data/segmentation_usage.csv
- templates/utilities_reference.pptx

Output:
- outputs/{bu_name}_report.pptx
---------
# What done means
done means:

I can choose one BU
Python reads the CSV
Python filters that BU
Python computes some metrics
Python creates a PowerPoint file
I can open the PPT and see the content
---------
# Scope:
# BU Report MCP - V1 Scope

Goal:
Generate one PowerPoint report for one BU from a local CSV.

Input:
- BU name

Output:
- One PPTX file in /outputs

Slides:
1. Title + KPI summary
2. Top conditions
3. Issues + recommendations

Not included in V1:
- full visual cloning of Utilities deck
- advanced charts
- all BU batch generation
- automatic slide layout understanding

# Data grain:
One row represents one campaign x one segment x one condition.

# Data dictionary
## CSV contract

Required columns:
- bu_name: business unit name
- campaign_id: unique campaign id
- segment_name: segment identifier/name
- operator_name: operator or creator
- condition_name: filtering condition
- condition_type: CDP or BQ
- channel: promo/journey/noti/ads
- goal: campaign goal
- size_pool: audience size
- month: reporting month

Data grain:
- one row = one campaign x one segment x one condition