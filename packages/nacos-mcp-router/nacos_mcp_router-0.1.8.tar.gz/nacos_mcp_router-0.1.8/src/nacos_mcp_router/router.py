import json
import os

import anyio
from mcp import types
from mcp.client.stdio import get_default_environment
from mcp.server import Server

from .logger import NacosMcpRouteLogger
from .mcp_manager import McpUpdater
from .nacos_http_client import NacosHttpClient
from .router_types import ChromaDb
from .router_types import CustomServer

nacos_addr = os.getenv("NACOS_ADDR","127.0.0.1:8848")
nacos_user_name = os.getenv("NACOS_USERNAME","nacos")
nacos_password = os.getenv("NACOS_PASSWORD","")
nacos_http_client = NacosHttpClient(nacosAddr=nacos_addr if nacos_addr != "" else "127.0.0.1:8848", userName=nacos_user_name if nacos_user_name != "" else "nacos",passwd=nacos_password)
chroma_db_service = ChromaDb()
mcp_updater = McpUpdater(nacosHttpClient=nacos_http_client, chromaDbService=chroma_db_service, update_interval=60)
mcp_servers_dict = {}

router_logger = NacosMcpRouteLogger.get_logger()

async def search_mcp_server(task_description: str, key_words: str) -> str:
  """
    Name:
        search_mcp_server

    Description:
        执行任务前首先使用本工具。根据任务描述及关键字搜索mcp server，制定完成任务的步骤。

    Args:
        task_description (string): 用户任务描述，使用中文
        key_words (string): 字符串数组，用户任务关键字，可以为多个，英文逗号分隔，最多为2个
  """
  try:
    mcp_servers1 = []
    keywords = key_words.split(",")
    for key_word in keywords:
      mcps = mcp_updater.search_mcp_by_keyword(key_word)
      if len(mcps) > 0:
        for mcp in mcps:
          mcp_servers1.append(mcp)

    if len(mcp_servers1) < 5:
      keywords.append(task_description)
      mcp_servers2 = mcp_updater.getMcpServer(task_description,5-len(mcp_servers1))
      for mcp in mcp_servers2:
        mcp_servers1.append(mcp)

    result = {}
    for mcpServer in mcp_servers1:
      dct = {}
      dct['name'] = str(mcpServer.get_name())
      dct['description'] = str(mcpServer.get_description())
      result[str(mcpServer.get_name())] = dct

    content = json.dumps(result, ensure_ascii=False)

    jsonString = ("## 获取" + task_description + "的步骤如下：\n"
                  + "### 1. 当前可用的mcp server列表为：" + content
                  + "\n### 2. 从当前可用的mcp server列表中选择你需要的mcp server调add_mcp_server工具安装mcp server")
    return jsonString
  except Exception as e:
    router_logger.warning("failed to search_mcp_server: " + task_description, exc_info=e)
    jsonString = "failed to search mcp server for " + task_description
    return jsonString


async def use_tool(mcp_server_name: str, mcp_tool_name: str, params:dict) -> str:
  try:
    if mcp_server_name not in mcp_servers_dict:
      router_logger.warning("mcp server {} not found, use search_mcp_server to get mcp servers".format(mcp_server_name))
      return "mcp server not found, use search_mcp_server to get mcp servers"

    mcp_server = mcp_servers_dict[mcp_server_name]
    if mcp_server.healthy():
      response = await mcp_server.execute_tool(mcp_tool_name, params)
    else:
      del mcp_servers_dict[mcp_server_name]
      return  "mcp server is not healthy, use search_mcp_server to get mcp servers"
    return str(response.content)
  except Exception as e:
    router_logger.warning("failed to use tool: " + mcp_tool_name, exc_info=e)
    return "failed to use tool: " + mcp_tool_name

async def add_mcp_server(mcp_server_name: str) -> str:
  """
  安装指定的mcp server
  :param mcp_server_name: mcp server名称
  :return: mcp server安装结果
  """
  try:
    mcp_server = nacos_http_client.get_mcp_server_by_name(mcp_server_name)
    if mcp_server is None or mcp_server.description == "":
      mcp_server = mcp_updater.get_mcp_server_by_name(mcp_server_name)

    if mcp_server is None:
      return mcp_server_name + " is not found" + ", use search_mcp_server to get mcp servers"

    disenabled_tools = {}
    tools_meta = mcp_server.mcp_config_detail.tool_spec.tools_meta
    for tool_name in tools_meta:
      meta = tools_meta[tool_name]
      if not meta.enabled:
        disenabled_tools[tool_name] = True

    if mcp_server_name not in mcp_servers_dict:
      env = get_default_environment()
      if mcp_server.agentConfig is None:
        mcp_server.agentConfig = {}
      if 'mcpServers' not in mcp_server.agentConfig or mcp_server.agentConfig['mcpServers'] is None:
        mcp_server.agentConfig['mcpServers'] = {}

      mcp_servers = mcp_server.agentConfig["mcpServers"]
      for key, value in mcp_servers.items():
        server_config = value
        if 'env' in server_config:
          for k in server_config['env']:
            env[k] = server_config['env'][k]
        server_config['env'] = env
        if 'headers' not in server_config:
          server_config['headers'] = {}

      server = CustomServer(name=mcp_server_name,config=mcp_server.agentConfig)
      await server.wait_for_initialization()
      if server.healthy():
        mcp_servers_dict[mcp_server_name] = server

    server = mcp_servers_dict[mcp_server_name]

    tools = await server.list_tools()
    tool_list = []
    for tool in tools:
      if tool.name in disenabled_tools:
        continue
      dct = {}
      dct['name'] = tool.name
      dct['description'] = tool.description
      dct['inputSchema'] = tool.inputSchema
      tool_list.append(dct)

    nacos_http_client.update_mcp_tools(mcp_server_name,tools)

    result = "1. " + mcp_server_name + "安装完成, tool 列表为: " + json.dumps(tool_list, ensure_ascii=False) +  "\n2." + mcp_server_name + "的工具需要通过nacos-mcp-router的use_tool工具代理使用"
    return result
  except Exception as e:
    router_logger.warning("failed to install mcp server: " + mcp_server_name, exc_info=e)
    return "failed to install mcp server: " + mcp_server_name

def main() -> int:
  app = Server("nacos_mcp_router")

  @app.call_tool()
  async def call_tool(
          name: str, arguments: dict
  ) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    match name:
      case "search_mcp_server":
        content = await search_mcp_server(arguments["task_description"], arguments["key_words"])
        return [types.TextContent(type="text", text=content)]
      case "add_mcp_server":
        content = await add_mcp_server(arguments["mcp_server_name"])
        return [types.TextContent(type="text", text=content)]
      case "use_tool":
        params = json.loads(arguments["params"])
        content = await use_tool(arguments["mcp_server_name"],arguments["mcp_tool_name"], params)
        return [types.TextContent(type="text", text=content)]
      case _:
        return [types.TextContent(type="text", text="not implemented tool")]
    

  @app.list_tools()
  async def list_tools() -> list[types.Tool]:
    return [
      types.Tool(
        name="search_mcp_server",
        description="执行任务前首先使用本工具。根据任务描述及关键字搜索mcp server, 制定完成任务的步骤。",
        inputSchema={
          "type": "object",
          "required": ["task_description", "key_words"],
          "properties": {
            "task_description": {
              "type": "string",
              "description": "用户任务描述 ",
            },
            "key_words": {
              "type": "string",
              "description": "用户任务关键字，可以为多个，英文逗号分隔，最多为2个"
            }
          },
        },
      ),
      types.Tool(
        name="add_mcp_server",
        description="安装指定的mcp server",
        inputSchema={
          "type": "object",
          "required": ["mcp_server_name"],
          "properties": {
            "mcp_server_name": {
              "type": "string",
              "description": "MCP Server名称"
            }
          }
        }
      ),
      types.Tool(
        name="use_tool",
        description="使用某个MCP Server的工具",
        inputSchema={
           "type": "object",
          "required": ["mcp_server_name","mcp_tool_name","params"],
          "properties": {
            "mcp_server_name": {
              "type": "string",
              "description": "需要使用的MCP Server名称"
            },
            "mcp_tool_name":{
              "type": "string",
              "description": "需要使用的MCP Server工具名称"
            },
            "params": {
              "type": "string",
              "description": "需要使用的MCP Server工具的参数"
            }
          }
        }
      )
    ]

  from mcp.server.stdio import stdio_server

  async def arun():
    async with stdio_server() as streams:
      await app.run(
        streams[0], streams[1], app.create_initialization_options()
      )

  anyio.run(arun)
  
  return 0