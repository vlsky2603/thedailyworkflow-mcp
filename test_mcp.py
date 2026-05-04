"""End-to-end test of the MCP server: spawn, list tools, call each tool."""
import asyncio
import json
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def main():
    params = StdioServerParameters(
        command=sys.executable,
        args=["-m", "thedailyworkflow_mcp.server"],
    )

    print("[test] spawning MCP server via stdio...\n")
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("[test] initialized OK\n")

            # 1. List tools
            tools = await session.list_tools()
            print(f"[test] {len(tools.tools)} tools registered:")
            for t in tools.tools:
                print(f"   - {t.name}")
            print()

            # 2. catalog_stats
            print("[test] >>> catalog_stats()")
            r = await session.call_tool("catalog_stats", {})
            payload = json.loads(r.content[0].text)
            print(f"   total_servers: {payload['total_servers']}")
            print(f"   top_languages: {[(x['language'], x['count']) for x in payload['top_languages'][:3]]}")
            print()

            # 3. list_mcp_categories
            print("[test] >>> list_mcp_categories()")
            r = await session.call_tool("list_mcp_categories", {})
            payload = json.loads(r.content[0].text)
            print(f"   total categories: {payload['count']}")
            print(f"   top 5: {[(x['name'], x['count']) for x in payload['categories'][:5]]}")
            print()

            # 4. search_mcp_servers
            print("[test] >>> search_mcp_servers(query='postgres', limit=3)")
            r = await session.call_tool("search_mcp_servers", {"query": "postgres", "limit": 3})
            payload = json.loads(r.content[0].text)
            print(f"   matches: {payload['count']}")
            for s in payload['results']:
                print(f"   - {s['name']} ({s['stars']} stars) - {s['description'][:80]}...")
            print()

            # 5. search filtered by client
            print("[test] >>> search_mcp_servers(client='cursor', category='databases', limit=3)")
            r = await session.call_tool("search_mcp_servers", {"client": "cursor", "category": "databases", "limit": 3})
            payload = json.loads(r.content[0].text)
            print(f"   matches: {payload['count']}")
            for s in payload['results']:
                print(f"   - {s['name']} - clients: {s['supported_clients']}")
            print()

            # 6. get_mcp_install_config
            sample_slug = payload['results'][0]['slug'] if payload['results'] else 'blockrun-mcp'
            print(f"[test] >>> get_mcp_install_config(slug='{sample_slug}', client='claude-desktop')")
            r = await session.call_tool("get_mcp_install_config", {"slug": sample_slug, "client": "claude-desktop"})
            payload = json.loads(r.content[0].text)
            print(f"   name: {payload.get('name')}")
            print(f"   available_clients: {payload.get('available_clients')}")
            print(f"   config: {(payload.get('config') or '')[:160]}...")
            print()

            # 7. get_mcp_details
            print(f"[test] >>> get_mcp_details(slug='{sample_slug}')")
            r = await session.call_tool("get_mcp_details", {"slug": sample_slug})
            payload = json.loads(r.content[0].text)
            print(f"   name: {payload['name']}")
            print(f"   stars: {payload['stars']}")
            print(f"   page_url: {payload['page_url']}")
            print(f"   has install_configs: {bool(payload.get('install_configs'))}")
            print(f"   use_cases count: {len(payload.get('use_cases') or [])}")
            print()

            # 8. error case — non-existent slug
            print("[test] >>> get_mcp_install_config(slug='this-does-not-exist-xyz')")
            r = await session.call_tool("get_mcp_install_config", {"slug": "this-does-not-exist-xyz"})
            print(f"   raw response: {r.content[0].text[:200]}")
            print()

            # 9. AI tools search
            print("[test] >>> search_ai_tools(query='image generation', limit=2)")
            r = await session.call_tool("search_ai_tools", {"query": "image generation", "limit": 2})
            payload = json.loads(r.content[0].text)
            print(f"   matches: {payload['count']}")
            for s in payload['results']:
                print(f"   - {s['name']} [{s['pricing']}] - {(s.get('description') or '')[:80]}...")
            tool_name = payload['results'][0]['name'] if payload['results'] else 'Notion AI'
            print()

            # 10. AI tool details
            print(f"[test] >>> get_ai_tool_details(name='{tool_name}')")
            r = await session.call_tool("get_ai_tool_details", {"name": tool_name})
            payload = json.loads(r.content[0].text)
            print(f"   name: {payload.get('name')}")
            print(f"   category: {payload.get('category')}")
            print(f"   pricing: {payload.get('pricing')}")
            print(f"   page_url: {payload.get('page_url')}")
            print()

            # 11. Pipeline search
            print("[test] >>> search_pipelines(query='podcast', limit=2)")
            r = await session.call_tool("search_pipelines", {"query": "podcast", "limit": 2})
            payload = json.loads(r.content[0].text)
            print(f"   matches: {payload['count']}")
            for p in payload['results']:
                print(f"   - {p['title']} ({p['hits']} hits, {p['step_count']} steps)")
            sample_pipeline = payload['results'][0]['slug'] if payload['results'] else None
            print()

            # 12. Pipeline details
            if sample_pipeline:
                print(f"[test] >>> get_pipeline_details(slug='{sample_pipeline}')")
                r = await session.call_tool("get_pipeline_details", {"slug": sample_pipeline})
                payload = json.loads(r.content[0].text)
                print(f"   title: {payload['title']}")
                print(f"   step_count: {payload['step_count']}")
                if payload.get('steps'):
                    s1 = payload['steps'][0]
                    print(f"   step 1: {s1['title']} (tool: {s1['tool_name']})")
                print()

            # 13. Popular pipelines
            print("[test] >>> get_popular_pipelines(limit=3)")
            r = await session.call_tool("get_popular_pipelines", {"limit": 3})
            payload = json.loads(r.content[0].text)
            print(f"   count: {payload['count']}")
            for p in payload['results']:
                print(f"   - {p['title']} ({p['hits']} hits)")
            print()

            # 14. Build custom pipeline URL
            print("[test] >>> build_custom_pipeline_url(task='generate Instagram posts from RSS feed')")
            r = await session.call_tool("build_custom_pipeline_url", {"task": "generate Instagram posts from RSS feed"})
            payload = json.loads(r.content[0].text)
            print(f"   builder_url: {payload['builder_url']}")
            print()

            print("[test] ALL TESTS PASSED")


if __name__ == "__main__":
    asyncio.run(main())
