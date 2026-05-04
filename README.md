# TheDailyWorkflow MCP

> **A bridge between Claude/Cursor/Windsurf/Cline and the largest curated AI catalog.**
> Powered by [thedailyworkflow.com](https://thedailyworkflow.com) — bilingual (EN+RU) AI directory.

What you get inside your AI assistant:

- **3500+ MCP servers** — search by query/category/client/language, get ready-to-paste install configs
- **15000+ AI tools** — search, get pricing/features/target audience for any tool
- **200+ ready-made workflow pipelines** — step-by-step recipes with prompts for common AI tasks
- **147+ MCP tutorials** — install, build, comparison, troubleshooting guides
- **147+ Q&A cases** — curated solutions to real GitHub Issues (timeouts, ESM bugs, install errors)
- **1700+ AI prompts** — battle-tested prompts for ChatGPT, Claude, Midjourney, etc.
- **Custom pipeline builder** — for any goal, get a deep link to the AI builder that composes a workflow from 15k tools

Stop browsing tabs. Ask Claude:

- _"Find me an MCP for Notion that works with Cursor"_
- _"My fastapi-mcp is timing out after 5s, what's the fix?"_
- _"Give me a pipeline to turn a blog post into a podcast"_
- _"Find me a battle-tested ChatGPT prompt for cold outreach"_

— get answers with working configs, copy-paste prompts, and links to full guides.

## Quick install

### Claude Desktop

Add to `claude_desktop_config.json`:

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "thedailyworkflow": {
      "command": "uvx",
      "args": ["thedailyworkflow-mcp"]
    }
  }
}
```

### Cursor

Add to `~/.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "thedailyworkflow": {
      "command": "uvx",
      "args": ["thedailyworkflow-mcp"]
    }
  }
}
```

### Windsurf / Cline / Continue / Goose

Same config format — point the `command` to `uvx` with arg `thedailyworkflow-mcp`.

### Manual install (pip)

```bash
pip install thedailyworkflow-mcp
```

Then use `command: "thedailyworkflow-mcp"` (no args) in your client config.

## Tools provided (16 total)

### MCP servers — 5 tools

| Tool | What it does |
|---|---|
| `search_mcp_servers` | Search the catalog by query, category, client, language. |
| `get_mcp_install_config` | Get a ready-to-paste config snippet for a specific MCP + client. |
| `get_mcp_details` | Full info on an MCP: description, use cases, tools, configs. |
| `list_mcp_categories` | All MCP categories with counts. |
| `catalog_stats` | Total MCP servers, top languages. |

### AI Tools — 3 tools

| Tool | What it does |
|---|---|
| `search_ai_tools` | Search 15000+ tools by query, category, pricing. |
| `get_ai_tool_details` | Full tool info: features, pricing, target audience, USP. |
| `list_ai_tool_categories` | All tool categories with counts. |

### Pipelines — 4 tools

| Tool | What it does |
|---|---|
| `search_pipelines` | Search 200+ ready-made AI workflow pipelines. |
| `get_pipeline_details` | Full pipeline: title, goal, steps with prompts. |
| `get_popular_pipelines` | Top-N most-used pipelines (browse what works). |
| `build_custom_pipeline_url` | For unique tasks — get a deep link to the AI Pipeline Builder. |

### MCP Tutorials — 2 tools

| Tool | What it does |
|---|---|
| `search_mcp_tutorials` | Search 147+ tutorials (install, build, comparison, troubleshooting). |
| `get_tutorial_details` | Full tutorial markdown with steps, code blocks, screenshots. |

### Q&A cases — 1 tool

| Tool | What it does |
|---|---|
| `search_qa_cases` | Search 147+ curated GitHub-Issue solutions (problem → cause → fix). |

### Prompts — 1 tool

| Tool | What it does |
|---|---|
| `search_prompts` | Search 1700+ user-submitted AI prompts by query, AI tool, category. |

## Example prompts

Once installed, try these in your AI client:

**MCP discovery & setup:**
- _"Find me an MCP server for working with PostgreSQL, give install config for Cursor"_
- _"What MCP servers exist for Slack?"_
- _"How many MCP servers are in the catalog total?"_

**MCP troubleshooting (Q&A cases):**
- _"My fastapi-mcp is hitting httpx.ReadTimeout after 5s, fix?"_
- _"Cursor MCP shows 'ESM require' error, what's the cause?"_
- _"Windows path bug in my filesystem MCP — find me the fix"_

**MCP learning (tutorials):**
- _"How do I install MCP server in Cursor?"_
- _"Beginner tutorial for building my own Python MCP server"_
- _"Compare Windsurf vs Cursor for MCP support"_

**AI tools:**
- _"Find me a free AI tool for image generation"_
- _"Compare Notion AI vs Mem.ai — who is each one for?"_
- _"What categories of AI tools exist?"_

**Workflow pipelines:**
- _"Give me a workflow to turn a blog post into a podcast"_
- _"Show me popular AI pipelines — I want inspiration"_
- _"I want to make a kids book with AI. Find me a pipeline."_
- _"Build me a custom pipeline for: extract leads from LinkedIn and DM them"_

**Prompts library:**
- _"Find me a battle-tested ChatGPT prompt for cold email outreach"_
- _"Give me a Claude prompt for refactoring Python code"_
- _"Search prompts about marketing copy"_

## How it works

This MCP server is a thin client over the public REST API at `https://thedailyworkflow.com/api/v1/*`. No auth required, no API key, no tracking beyond standard server logs.

Source code is ~400 lines — read [`server.py`](src/thedailyworkflow_mcp/server.py) to see exactly what it does.

## About the catalog

[TheDailyWorkflow](https://thedailyworkflow.com) maintains the largest curated MCP knowledge base:

- **3500+ servers** parsed from GitHub, awesome-lists, and direct submissions
- **AI-generated descriptions and install configs** for every server (no scraped READMEs)
- **Bilingual** — English and Russian content for everything
- **Per-client install snippets** — Claude Desktop, Cursor, Cline, Windsurf, Continue, Goose
- **Curated Q&A** — real-world fixes from GitHub Issues, deduplicated and structured
- **Tutorials** — install, build, compare, troubleshooting guides for every major scenario
- Browse: [thedailyworkflow.com/mcp](https://thedailyworkflow.com/mcp)

## License

MIT — see [LICENSE](LICENSE).

## Contributing

Found a bug or want a new tool? [Open an issue](https://github.com/vlsky2603/thedailyworkflow-mcp/issues) or PR.

To submit a missing MCP server to the catalog itself: [thedailyworkflow.com/mcp/submit](https://thedailyworkflow.com/mcp/submit).

---

Built with [FastMCP](https://github.com/jlowin/fastmcp) by the [thedailyworkflow.com](https://thedailyworkflow.com) team.
