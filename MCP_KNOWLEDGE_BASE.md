# MCP Knowledge Base

A personal reference covering how MCP works, how Claude uses it, and best practices for setup.

---

## 1. What is MCP?

**Model Context Protocol (MCP)** is a standard that lets Claude connect to external servers that expose tools, prompts, and resources. Instead of Claude knowing everything upfront, MCP lets it call external functions at runtime to fetch data, run logic, or generate files.

```
User message
    ↓
Claude (reasoning)
    ↓ calls
MCP Server (your Python code)
    ↓ returns data
Claude (formats response)
    ↓
User sees answer
```

---

## 2. The 3 Things an MCP Server Can Expose

### Tools (`@mcp.tool()`)
Functions Claude can **call and execute**. They run code, read files, call APIs, generate outputs.

```python
@mcp.tool()
def preview_bu_report(bu_name: str) -> dict:
    """Use when user asks about a BU's performance or health."""
    ...
```

- Claude calls these automatically based on user intent
- Return value goes back to Claude as data
- Business users never see the tool name

### Prompts (`@mcp.prompt()`)
**Conversation starters** — reusable message templates that guide Claude to call the right tools and format output a specific way.

```python
@mcp.prompt()
def analyze_bu(bu_name: str) -> str:
    return f"""You are a data analyst.
Call: preview_bu_report(bu_name="{bu_name}")
Then respond using this structure: ..."""
```

- Only activated when a user explicitly selects them from the UI
- NOT auto-injected — they become the first user message when invoked
- Best for complex multi-step workflows

### Resources (`@mcp.resource()`)
**Files or data** Claude can read on demand (markdown docs, CSVs, configs).

```python
@mcp.resource("file://guide/report-guide.md")
def report_guide() -> str:
    return Path("guide/report-guide.md").read_text()
```

- Client fetches these when needed
- Good for background context, documentation, guides

---

## 3. How Claude Decides Which Tool to Call

Claude uses 3 layers in priority order:

### Layer 1 — System Prompt (most reliable)
Explicit routing rules you write in Claude Desktop Project Instructions.

```
When user asks about BU performance → call preview_bu_report
When user asks to generate a report → call generate_bu_report
When user doesn't know BU names → call list_bu_names first
```

### Layer 2 — Tool Docstrings (safety net)
Claude reads the function name + docstring and matches to user intent.
Write docstrings as **user intent**, not implementation detail.

```python
# Bad — implementation focused
"""Preview report data for one BU without generating the PowerPoint."""

# Good — intent focused
"""Use when user asks about a BU's performance, health, or segmentation data."""
```

### Layer 3 — Raw User Message (least reliable)
If no rule and no matching docstring, Claude guesses from the message.
Can pick wrong tool or call nothing.

### Decision Flow Example

```
User: "How is Cinema doing?"
    ↓
Layer 1: system prompt rule matches → call preview_bu_report ✅
    ↓
Claude calls: preview_bu_report(bu_name="Cinema")
    ↓
Gets: KPIs, conditions, issues, recommendations
    ↓
Claude formats clean response → user sees insights
```

---

## 4. Where Things Are Configured

| What | Where | Who sets it |
|---|---|---|
| Tools, Prompts, Resources | `server.py` | Developer |
| Which MCP servers to connect | `claude_desktop_config.json` | Developer / user |
| Always-on routing instructions (Claude Desktop) | Project Instructions in Claude Desktop UI | Developer / user |
| Always-on instructions (Claude Code) | `CLAUDE.md` in project root | Developer |
| Slash command skills | `~/.claude/commands/*.md` | Developer |

---

## 5. Claude Desktop vs Claude Code — Key Differences

| Feature | Claude Desktop | Claude Code CLI |
|---|---|---|
| MCP tools | ✅ | ✅ |
| MCP prompts | ✅ (appear in UI menu) | ✅ |
| MCP resources | ✅ | ✅ |
| Project system prompt | ✅ Project Instructions in UI | ✅ `CLAUDE.md` |
| Skills / slash commands | ❌ Not supported | ✅ `~/.claude/commands/*.md` |
| Auto-routing without setup | ❌ Needs Project Instructions | ✅ if `CLAUDE.md` exists |

---

## 6. MCP Prompts vs Skills vs CLAUDE.md

| | MCP Prompt | Skill (`.md`) | CLAUDE.md |
|---|---|---|---|
| **What it is** | Conversation starter template | Slash command | Instruction file |
| **Registered via** | `@mcp.prompt()` in server.py | `.md` file in `~/.claude/commands/` | File in project root |
| **Invoked by** | User selecting from UI menu | User typing `/skill-name` | Automatically on every conversation |
| **Works in Claude Desktop** | ✅ | ❌ | ✅ (as Project Instructions) |
| **Works in Claude Code** | ✅ | ✅ | ✅ |
| **Has arguments** | ✅ typed Python args | ✅ via `$ARGUMENTS` | N/A |
| **Runs code** | ✅ (returns message, then Claude calls tools) | ❌ (just text template) | ❌ (just instructions) |

---

## 7. Can CLAUDE.md or skills.md Make MCP Read Them?

**No — MCP server does not auto-read any markdown files.**

| File | Who reads it | MCP server reads it? |
|---|---|---|
| `CLAUDE.md` in project root | Claude Code (the AI) automatically | ❌ |
| `~/.claude/commands/*.md` | Claude Code as slash commands | ❌ |
| Any `.md` in project folder | Nobody, unless explicitly coded | ❌ |

To make MCP actually read a file → expose it as a `@mcp.resource()`.

---

## 8. Best Practices for MCP Prompts

### Write prompts as executable instructions, not descriptions
```
# Bad
Analyze the BU data and give insights.

# Good
Call: preview_bu_report(bu_name="{bu_name}")
Then respond using exactly this structure: ...
```

### Prevent hallucination with explicit rules
```
Rules:
- Use exact numbers from the tool result, never estimate
- issues_flagged = length of the issues list
- No markdown headers outside the template
```

### Specify output as a template, not prose
```
BU: {bu_name} | campaigns=<N> | segments=<N>
verdict=<one sentence>
```

### Sequence multi-tool workflows explicitly
```
Step 1 — Call: list_bu_names()
Step 2 — For each BU, call: preview_bu_report(bu_name=<BU>)
Step 3 — Respond with the ranked table below
```

### Set persona once at the top
```
You are a data analyst specializing in marketing segmentation quality.
```

### One prompt = one workflow
Don't combine unrelated actions. Smaller prompts are more predictable.

---

## 9. Making MCP Business-User Friendly

Business users don't know tool names — they just chat naturally. Three things make this work:

### Option 1 — Claude Desktop Project System Prompt (zero code)
Create a Project in Claude Desktop → Project Instructions → paste routing rules:

```
You are a BU segmentation analyst assistant with access to the bu-report MCP server.
Your job is to help business users — they do not know tool names, so handle all tool calls silently.

When the user mentions a BU and asks about performance, health, or insights:
→ Call preview_bu_report(bu_name=<BU name>)

When the user asks to generate, export, or download a report or PowerPoint:
→ Call generate_bu_report(bu_name=<BU name>)

When the user doesn't know which BU to look at:
→ Call list_bu_names() first, then ask them to pick one

When the user asks to compare two BUs:
→ Call preview_bu_report for each, then produce a comparison table

When the user asks for an overview of all BUs:
→ Call list_bu_names(), then preview_bu_report for each, return ranked summary

Never ask the user to call tools manually.
Never mention tool names in your response.
```

### Option 2 — Intent-focused docstrings (small code change)
Rewrite tool docstrings to describe user intent instead of implementation. Claude auto-routes better.

### Option 3 — Natural language entry point tool (more code)
A single `ask_about_segment(question: str)` tool that accepts free text. More maintenance but best UX.

**Recommended:** Option 1 + Option 2 together covers 95% of cases.

---

## 10. Common Mistakes and Fixes

| Problem | Cause | Fix |
|---|---|---|
| Claude calls wrong tool | Ambiguous docstrings | Rewrite as user intent |
| Claude calls no tool | No match found | Add explicit rule to system prompt |
| Claude asks user to call tools manually | Missing instruction | Add: "never ask user to call tools" to system prompt |
| Claude makes up data | No constraint in prompt | Add: "use exact numbers from tool result only" |
| MCP prompt not appearing in UI | Server not connected to project | Re-check MCP server connection in Claude Desktop settings |
| Skills not working in Claude Desktop | Skills are Claude Code only | Use MCP prompts instead |

---

## 11. This Project's MCP Setup Summary

**Server:** `bu-report-mcp/src/server.py`

### Tools (3)
| Tool | When to use |
|---|---|
| `list_bu_names` | User doesn't know available BUs |
| `preview_bu_report` | User asks about a BU's data, health, or insights |
| `generate_bu_report` | User wants a PowerPoint report exported |

### Prompts (5)
| Prompt | Args | Workflow |
|---|---|---|
| `analyze_bu` | `bu_name` | Deep dive — KPIs, conditions, issues, operator profiles, exec summary |
| `executive_summary` | `bu_name` | Concise 5-line summary card |
| `compare_bus` | `bu_name_1`, `bu_name_2` | Side-by-side comparison table |
| `analyze_all_bus` | — | Fleet health report across all BUs |
| `generate_all_reports` | — | Batch PowerPoint generation with status table |

### Business User Setup
- Claude Desktop Project Instructions → routing system prompt (see Section 9)
- No skills or CLAUDE.md needed for Claude Desktop users
