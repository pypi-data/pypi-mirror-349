from stash_data_mcp.server import mcp


async def test():
    tools = await mcp.list_tools()
    result = await mcp.call_tool("drop_table_traveling_dogs", {})

    result = await mcp.call_tool("create_table", {
        "table_name": "traveling_dogs",
        "columns": {
            "id": "integer",
            "name": "string",
            "country": "string",
            "owner": "string"
        },
        "partition_keys": ["id"]
    })


    result = await mcp.call_tool("drop_table_traveling_dogs", {})


if __name__ == "__main__":
    import asyncio
    asyncio.run(test())
