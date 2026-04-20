User: "Generate report for Utilities BU"

→ MCP receives request
→ call load_segment_data("Utilities")
→ call calculate_kpi()
→ call detect_issue()
→ call generate_insight()  ← LLM
→ call generate_slide()

→ return PPT

# Phase 2 target architecture
User
  ↓
Claude Desktop / MCP Host
  ↓
MCP Server (Python)
  ↓
Tool: generate_bu_report(bu_names)
  ↓
1. load data
2. filter by BU
3. calculate KPI
4. generate insight with LLM
5. return structured report