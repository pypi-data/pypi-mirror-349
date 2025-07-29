from fastmcp import Client  
from fastmcp.client.transports import PythonStdioTransport  
import asyncio  
import os  
import dotenv  
  
async def main():  
    # 加载.env文件中的环境变量（如果存在）  
    dotenv.load_dotenv()  
      
    # 准备环境变量  
    env_vars = {  
        # 必需的API密钥和端点  
        "API_KEY": os.environ.get("API_KEY", "your_default_api_key"),  
        "API_BASE_URL": os.environ.get("API_BASE_URL", "https://your-api-base-url.com/v1"),  
        "DIFY_API_KEY": os.environ.get("DIFY_API_KEY", "your_default_dify_api_key"),  
          
        # 可选的模型配置  
        "TRANSLATION_MODEL": os.environ.get("TRANSLATION_MODEL", "gpt-3.5-turbo"),  
    }  
      
    # 显式创建传输对象，包含环境变量  
    transport = PythonStdioTransport(  
        script_path="server.py",  
        env=env_vars,  
        # 可选：指定Python解释器路径  
        # python_cmd="/usr/bin/python3.10",  
        # 可选：指定工作目录  
        # cwd="/path/to/working/directory"  
    )  
      
    # 创建客户端  
    client = Client(transport)  
      
    try:  
        async with client:  
            # 列出服务器上的所有工具  
            tools = await client.list_tools()  
            print("可用工具:")  
            for tool in tools:  
                print(f"- {tool.name}: {tool.description}")  
              
            # 调用知识检索工具  
            print("\n调用知识检索工具:")  
            result = await client.call_tool("query_mcp_knowledge", {  
                "question": "什么是MCP协议？"  
            })  
              
            # 打印结果  
            print("\n结果:")  
            print(result[0].text)  
    except Exception as e:  
        print(f"错误: {str(e)}")  
  
if __name__ == "__main__":  
    asyncio.run(main())