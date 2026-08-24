

"""
@tool("tool_name", "description for Claude", {"param": type})
async def my_tool(args):
    ...
    return {"content": [{"type": "text", "text": "result"}]}

Then register it via create_sdk_mcp_server(...), add its server to mcp_servers, and reference it in allowed_tools as mcp__<server_name>__<tool_name>.
"""