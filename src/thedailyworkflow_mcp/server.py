"""TheDailyWorkflow MCP server.

A bridge between Claude/Cursor/Windsurf/Cline and the largest curated AI catalog at
thedailyworkflow.com:

  - 3500+ MCP servers (with install configs for every major client)
  - 15000+ AI tools (search, compare, get pricing/features)
  - 200+ ready-made workflow pipelines (step-by-step recipes)
  - 147+ MCP tutorials (install, build, comparison, troubleshooting)
  - 147+ Q&A cases (curated solutions to real GitHub Issues)
  - 1700+ AI prompts (battle-tested for ChatGPT/Claude/Midjourney)
  - On-demand custom pipeline builder

Tools (16):
  - search_mcp_servers, get_mcp_install_config, get_mcp_details,
    list_mcp_categories, catalog_stats
  - search_ai_tools, get_ai_tool_details, list_ai_tool_categories
  - search_pipelines, get_pipeline_details, get_popular_pipelines,
    build_custom_pipeline_url
  - search_mcp_tutorials, get_tutorial_details
  - search_qa_cases
  - search_prompts
"""
from __future__ import annotations

import os
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

__version__ = "0.3.0"

API_BASE = os.getenv("THEDAILYWORKFLOW_API", "https://thedailyworkflow.com/api/v1")
HTTP_TIMEOUT = 15.0

mcp = FastMCP("thedailyworkflow-mcp")
_client = httpx.Client(timeout=HTTP_TIMEOUT, headers={
    "User-Agent": f"thedailyworkflow-mcp/{__version__}",
    "Accept": "application/json",
})


def _get(path: str, params: dict[str, Any] | None = None) -> dict:
    url = f"{API_BASE}{path}"
    r = _client.get(url, params=params or {})
    r.raise_for_status()
    return r.json()


@mcp.tool()
def search_mcp_servers(
    query: str = "",
    category: str = "",
    client: str = "",
    language: str = "",
    limit: int = 10,
) -> dict:
    """Search the catalog of 3500+ MCP servers at thedailyworkflow.com.

    Args:
        query: Free-text search (matches name, description, keywords). Example: "notion", "postgres database".
        category: Filter by category. Common values: databases, web, filesystem, cloud,
                  productivity, communication, dev, ai, search, monitoring.
        client: Filter by supported MCP client. Values: claude-desktop, cursor, cline,
                windsurf, continue, goose.
        language: Filter by implementation language. Values: typescript, python, go, rust, java.
        limit: Max results to return (1-25, default 10).

    Returns:
        Dict with `count` and `results` (list of MCP server summaries).
        Each result has: slug, name, description, categories, language, transport,
        supported_clients, stars, repo_url, page_url (link to full info).

    Use this when the user asks for an MCP server matching some need ("find me an MCP for X",
    "what MCP servers work with Cursor", "Slack MCP servers"). After choosing a candidate,
    call get_mcp_install_config to get ready-to-paste setup.
    """
    return _get("/mcp/search", {
        "q": query, "category": category, "client": client,
        "language": language, "limit": min(max(int(limit), 1), 25),
    })


@mcp.tool()
def get_mcp_install_config(slug: str, client: str = "claude-desktop") -> dict:
    """Get a ready-to-paste install config for a specific MCP server and client.

    Args:
        slug: MCP server slug (from search_mcp_servers `slug` field). Example: "github-mcp".
        client: Target client. Values: claude-desktop, cursor, cline, windsurf, continue, goose.
                Default: claude-desktop.

    Returns:
        Dict with `config` (JSON snippet ready to paste into client's config file),
        `install_command` (e.g. `npx @x/y`), `available_clients` (which clients have configs),
        and `page_url`. If config for requested client is missing, `config` will be null —
        try a different client from `available_clients`.

    Use this AFTER finding an MCP via search. Show the user the exact config snippet plus
    the path to their client's config file (e.g. for Claude Desktop on macOS:
    ~/Library/Application Support/Claude/claude_desktop_config.json).
    """
    return _get(f"/mcp/install/{slug}", {"client": client})


@mcp.tool()
def get_mcp_details(slug: str) -> dict:
    """Get complete details for a specific MCP server: description, use cases, tools, install configs.

    Args:
        slug: MCP server slug.

    Returns:
        Full MCP record with description, long description, use_cases (list of scenarios),
        tools (what the server exposes), install_configs (per-client snippets),
        license, author, stars, page_url.

    Use this when the user wants to learn more about a specific MCP before installing,
    or when they ask "what does X MCP do" or "show me use cases for X".
    """
    return _get(f"/mcp/{slug}")


@mcp.tool()
def list_mcp_categories() -> dict:
    """List all MCP categories in the catalog with counts.

    Returns:
        Dict with `count` (total categories) and `categories` (list of {name, count}).

    Useful when the user wants to browse by category or asks "what kinds of MCP servers exist".
    """
    return _get("/mcp/categories")


@mcp.tool()
def catalog_stats() -> dict:
    """Stats about the MCP catalog at thedailyworkflow.com.

    Returns:
        total_servers (int), top_languages (list of {language, count}), catalog_url.

    Use this for context-setting questions like "how many MCP servers exist" or
    "what's the most popular language for MCP servers".
    """
    return _get("/mcp/stats")


# ── AI Tools (15000+ services) ─────────────────────────────────────────────


@mcp.tool()
def search_ai_tools(
    query: str = "",
    category: str = "",
    pricing: str = "",
    limit: int = 10,
) -> dict:
    """Search 15000+ AI tools in the thedailyworkflow.com catalog.

    Args:
        query: Free-text search (matches name, description, tags). Example: "image generation",
               "transcription", "chatbot".
        category: Filter by category. Examples: "Image Generation", "Productivity",
                  "Code & Development", "Audio & Music", "Writing & Content".
        pricing: Filter by pricing model. Values: "Free", "Freemium", "Paid", "Enterprise".
        limit: Max results (1-25, default 10).

    Returns:
        Dict with `count` and `results`. Each result: slug, name, category, description,
        pricing, logo_url, official_url, page_url.

    Use this when the user asks for an AI tool for a specific task ("find me an AI for X",
    "what are good free AI tools for Y", "compare AI tools for Z"). Follow up with
    get_ai_tool_details for the chosen one.
    """
    return _get("/tools/search", {
        "q": query, "category": category, "pricing": pricing,
        "limit": min(max(int(limit), 1), 25),
    })


@mcp.tool()
def get_ai_tool_details(name: str) -> dict:
    """Full details for a specific AI tool: features, pricing, target audience, USP.

    Args:
        name: Tool name (case-insensitive) or slug. Example: "Notion AI", "Midjourney".

    Returns:
        Dict with full description, key_features, pricing_details, target_audience,
        unique_selling, tags, rating, page_url.

    Use this when the user wants deeper info on a tool before signing up — pricing
    breakdown, who it's for, what makes it different.
    """
    return _get(f"/tools/{name}")


@mcp.tool()
def list_ai_tool_categories() -> dict:
    """List all AI tool categories in the catalog with counts.

    Returns:
        Dict with `count` and `categories` (list of {name, count}).

    Useful when the user wants to browse tools by category.
    """
    return _get("/tools/categories")


# ── Pipelines (100+ ready-made workflows) ─────────────────────────────────


@mcp.tool()
def search_pipelines(query: str = "", lang: str = "en", limit: int = 10) -> dict:
    """Search 100+ ready-made AI workflow pipelines (step-by-step recipes).

    A pipeline is a complete plan: which AI tools to use in what order, with
    ready-to-paste prompts at each step, to accomplish a specific goal.

    Args:
        query: Free-text search over pipeline titles and queries. Examples: "podcast",
               "children book", "youtube channel automation".
        lang: Language for output ("en" or "ru"). Default: "en".
        limit: Max results (1-25, default 10).

    Returns:
        Dict with `count` and `results`. Each result: slug, title, goal, query,
        hits (popularity), step_count, page_url.

    Use this when the user describes a goal that involves multiple steps with multiple AI
    tools ("how do I make X using AI", "give me a workflow for Y"). After picking, call
    get_pipeline_details for full step-by-step plan with prompts.
    """
    return _get("/pipelines/search", {
        "q": query, "lang": lang,
        "limit": min(max(int(limit), 1), 25),
    })


@mcp.tool()
def get_pipeline_details(slug: str, lang: str = "en") -> dict:
    """Full pipeline: title, goal, all steps with tools, instructions, prompts, pricing.

    Args:
        slug: Pipeline slug (from search_pipelines).
        lang: "en" or "ru" (default "en").

    Returns:
        Dict with title, goal, steps (each: step number, title, tool_name, tool_type,
        instruction, prompt_example, pricing, category, tool_url), step_count, page_url.

    Use this to give the user a complete actionable plan with copy-paste prompts.
    """
    return _get(f"/pipelines/{slug}", {"lang": lang})


@mcp.tool()
def get_popular_pipelines(lang: str = "en", limit: int = 10) -> dict:
    """Top-N most-used pipelines by hit count — what other users have found valuable.

    Args:
        lang: "en" or "ru" (default "en").
        limit: Max results (1-25, default 10).

    Returns:
        Same shape as search_pipelines, sorted by hits descending.

    Use this for inspiration ("what can I do with AI?", "show me popular AI workflows").
    """
    return _get("/pipelines/popular", {
        "lang": lang, "limit": min(max(int(limit), 1), 25),
    })


@mcp.tool()
def build_custom_pipeline_url(task: str, lang: str = "en") -> dict:
    """For a custom task (no existing pipeline matches), get a deep link to the
    Pipeline Builder on thedailyworkflow.com.

    The builder composes a step-by-step pipeline from 15000+ AI tools with
    ready-to-paste prompts. The MCP server doesn't run it directly — it returns
    the prefilled URL where the user can run it.

    Args:
        task: Description of what the user wants to accomplish. Example:
              "create a YouTube channel with bedtime stories using AI for video and voice".
        lang: "en" or "ru" (default "en").

    Returns:
        Dict with builder_url (open this in browser), task (echoed), and a note explaining
        what happens.

    Use this when search_pipelines returns no good match. ALWAYS call search_pipelines first
    to check for existing solutions before suggesting the builder.
    """
    return _get("/pipelines/build-link", {"q": task, "lang": lang})


# ── MCP Tutorials (147+ guides) ────────────────────────────────────────────


@mcp.tool()
def search_mcp_tutorials(
    query: str = "",
    category: str = "",
    difficulty: str = "",
    lang: str = "en",
    limit: int = 10,
) -> dict:
    """Search 147+ MCP tutorials covering install, configuration, comparison, build guides.

    Tutorials are curated step-by-step guides for installing and using MCP servers
    with specific clients (Claude Desktop, Cursor, Cline, Windsurf), best-of-category
    roundups, build-your-own-server walkthroughs, and concept explainers.

    Args:
        query: Free-text search over titles, summaries, keywords. Example: "cursor mcp",
               "build python mcp server", "windsurf vs cursor".
        category: Filter by category. Values: client_setup, category_best, build, usecase,
                  install, comparison, concept, general.
        difficulty: Filter by level. Values: beginner, intermediate, advanced.
        lang: Output language (en|ru). Default: en.
        limit: Max results (1-25, default 10).

    Returns:
        Dict with `count` and `results`. Each result: slug, title, summary,
        difficulty, category, tutorial_type, estimated_minutes, related_servers,
        page_url.

    Use this when the user asks "how do I install X MCP", "best MCPs for Cursor",
    "how to build my own MCP server", or hits an MCP setup problem. Follow up with
    get_tutorial_details(slug) for the full markdown.
    """
    return _get("/tutorials/search", {
        "q": query, "category": category, "difficulty": difficulty,
        "lang": lang, "limit": min(max(int(limit), 1), 25),
    })


@mcp.tool()
def get_tutorial_details(slug: str, lang: str = "en") -> dict:
    """Full tutorial content (markdown) with all steps, code blocks, screenshots.

    Args:
        slug: Tutorial slug (from search_mcp_tutorials).
        lang: en | ru. Default: en.

    Returns:
        Dict with title, summary, content (full markdown), difficulty, category,
        target_client, target_server, target_category, estimated_minutes,
        word_count, views_count, page_url.

    Use this AFTER finding a relevant tutorial via search. The `content` field has
    full markdown — render it directly to the user, or extract the install commands
    / config snippets they asked about.
    """
    return _get(f"/tutorials/{slug}", {"lang": lang})


# ── Q&A cases (147+ curated GitHub-Issue solutions) ────────────────────────


@mcp.tool()
def search_qa_cases(
    query: str = "",
    server: str = "",
    category: str = "",
    lang: str = "en",
    limit: int = 10,
) -> dict:
    """Search 147+ Q&A cases — curated solutions to real GitHub Issues with MCP servers
    and AI tools. Each case is structured as: problem (symptom) → cause → solution
    (markdown with code).

    Use this FIRST when the user reports an error or unexpected behavior with an
    MCP server. Many common errors (timeouts, ESM/require issues, Windows path
    bugs, rate limits, connection failures) already have curated fixes.

    Args:
        query: Free-text search over title, problem, error keywords, tools used.
               Example: "ReadTimeout", "ESM require", "windows path", "rate limit".
        server: Filter by related MCP server slug. Example: "fastapi-mcp",
                "github-mcp-server".
        category: troubleshooting | install | config | usage. Default: any.
        lang: en | ru. Default: en.
        limit: Max results (1-25, default 10).

    Returns:
        Dict with `count` and `results`. Each result: slug, title, problem (preview),
        category, tools_used (list), error_keywords (list), related_server_slug,
        quality_score (0-10), helpful_count, page_url.

    The `slug` opens a full case at https://thedailyworkflow.com/qa/<slug> with the
    complete solution markdown.
    """
    return _get("/qa/search", {
        "q": query, "server": server, "category": category,
        "lang": lang, "limit": min(max(int(limit), 1), 25),
    })


# ── Prompts (1700+ battle-tested AI prompts) ───────────────────────────────


@mcp.tool()
def search_prompts(
    query: str = "",
    ai_tool: str = "",
    category: str = "",
    limit: int = 10,
) -> dict:
    """Search 1700+ user-submitted AI prompts for ChatGPT, Claude, Midjourney, DALL-E,
    Cursor, Gemini and more. Each prompt is a copy-paste-ready template for a
    specific task (writing, coding, marketing, design, business, etc).

    Args:
        query: Free-text search over title and prompt body. Example: "blog post outline",
               "code refactor", "logo design", "cold email".
        ai_tool: Filter by target AI. Values: ChatGPT, Claude, Midjourney, DALL-E 3,
                 Gemini, Cursor, Copilot.
        category: Filter by category. Values: Writing, Coding, Marketing, Design,
                  Business, Education, Creative, Productivity.
        limit: Max results (1-25, default 10).

    Returns:
        Dict with `count` and `results`. Each result: id, title, category, ai_tool,
        preview (first 200 chars of prompt), page_url.

    Use this when the user asks "give me a prompt for X" or "find a prompt to do Y".
    The full content is at the page_url.
    """
    return _get("/prompts/search", {
        "q": query, "ai_tool": ai_tool, "category": category,
        "limit": min(max(int(limit), 1), 25),
    })


def main() -> None:
    """Entry point for the `thedailyworkflow-mcp` CLI."""
    mcp.run()


if __name__ == "__main__":
    main()
