from universal_mcp.tools import Tool
from universal_mcp.tools.adapters import convert_tool_to_mcp_tool
from pprint import pprint


from universal_mcp_hubspot.app import HubspotApp

integration = None
app = HubspotApp(integration=integration)

tools = app.list_tools()

first_tool = tools[22]

mcp_t = Tool.from_function(first_tool)

mcp_t = convert_tool_to_mcp_tool(mcp_t)

pprint(mcp_t)


