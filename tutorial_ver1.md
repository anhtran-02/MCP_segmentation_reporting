# 🧠 MCP BU Segmentation Report Generator — Version 1 Summary

## 🎯 Objective

Build a **local MCP (Model Context Protocol) tool** for a Data Analyst that can:

- Read segmentation usage data from a **local CSV file**
- Analyze performance for a specific **Business Unit (BU)**
- Generate a **consulting-style PowerPoint report**
- Be triggered directly from **Claude Desktop via natural language**

---

# 🏗️ System Architecture

## End-to-End Flow



---

# 📦 Project Structure

```text
bu-report-mcp/
  data/
    segmentation_usage.csv
  templates/
    utilities_reference.pptx   # reference only (not parsed in V1)
  outputs/
    UTILITIES_report.pptx
  src/
    server.py           # MCP server (tool interface)
    csv_reader.py       # load & validate CSV
    metrics.py          # compute KPIs + logic
    ppt_writer.py       # generate slides
    report_builder.py   # main pipeline (CLI entry)
  requirements.txt
  README.md
---
⚠️ Limitations of V1
No LLM-generated insights
No advanced charting
No template parsing from reference PPT
No batch multi-BU generation
Basic visual styling (not pixel-perfect)
🔮 Next Steps (Future Versions)
V2 Ideas
LLM-generated insights and recommendations
Multi-BU batch reporting
Better charts (distribution, trends)
Operator clustering using ML
V3 Ideas
Use Utilities PPT as real template
Advanced design system (icons, layouts)
Dashboard + reporting integration
Automated scheduling (n8n / Airflow)





Do these in order:

install mcp[cli]
create src/server.py
test python src/server.py
add it to claude_desktop_config.json
fully restart Claude Desktop
ask Claude: “What BU names are available in my report tool?”



In step 4, you will build a normal Python script first, not MCP yet.

Goal of step 4:

read the CSV
filter one BU
calculate a few KPIs
print the result in terminal

At the end of this step, you should be able to run:

python src/report_builder.py --bu UTILITIES

and see a clean summary printed out.

In step 5, you will make the output more structured so it can be used by the slide generator.

Think of step 5 as:

CSV → BU dataframe → report data dictionary

That dictionary will later be passed into PowerPoint writing.


output: path file and error if any


What “done” means for step 7

Step 7 is complete when:

python src/server.py runs without crashing
Claude Desktop shows your bu-report server
Claude can call list_bu_names
Claude can call generate_bu_report
your .pptx appears in outputs/