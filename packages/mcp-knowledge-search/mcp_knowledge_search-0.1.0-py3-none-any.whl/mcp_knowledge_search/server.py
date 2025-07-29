from fastmcp import FastMCP
import httpx
import os
import openai

# 创建 MCP 服务器
mcp = FastMCP("mcp_knowledge_search")

# 设置 API 密钥和端点
API_KEY = os.environ.get("API_KEY")
API_BASE_URL = os.environ.get("API_BASE_URL") 
DIFY_API_ENDPOINT = os.environ.get("DIFY_API_ENDPOINT", "http://115.231.220.17:17027/v1/workflows/run")  # 提供默认值
DIFY_API_KEY = os.environ.get("DIFY_API_KEY")

# 检查必要配置
if not all([API_KEY, DIFY_API_KEY]):
    raise ValueError("API_KEY 和 DIFY_API_KEY 环境变量必须设置")

if not API_BASE_URL:
    raise ValueError("API_BASE_URL 环境变量必须设置")

# 初始化 OpenAI 兼容客户端
client = openai.AsyncClient(
    api_key=API_KEY,
    base_url=API_BASE_URL
)

@mcp.tool()
async def query_mcp_knowledge(question: str) -> str:
    """
    处理用户关于 MCP 的问题：
    1. 将用户问题翻译成英文
    2. 使用 Dify 知识库检索相关信息
    3. 直接返回检索结果

    Args:
        question: 用户的 MCP 相关问题

    Returns:
        检索结果
    """
    try:
        # 步骤 1：将问题翻译成英文
        english_question = await translate_to_english(question)

        # 步骤 2：调用 Dify 知识库 API 并直接返回结果
        knowledge = await query_dify_knowledge_base(english_question)

        return knowledge

    except Exception as e:
        return f"处理过程中出现错误: {str(e)}"

async def translate_to_english(text: str) -> str:
    """使用兼容 OpenAI API 的服务将文本翻译成英文"""
    try:
        model_name = os.environ.get("TRANSLATION_MODEL")

        if not model_name:
            return "翻译模型未配置"

        response = await client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a translator. Translate the following text to English accurately."},
                {"role": "user", "content": text}
            ],
            temperature=0.3,
            max_tokens=4096
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"翻译错误: {str(e)}")
        return text  # 如果翻译失败，返回原文

async def query_dify_knowledge_base(question: str) -> str:
    """调用 Dify 知识库 API 检索相关信息，并提取所有 content 字段"""
    try:
        async with httpx.AsyncClient() as http_client:
            response = await http_client.post(
                DIFY_API_ENDPOINT,
                headers={
                    "Authorization": f"Bearer {DIFY_API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "inputs": {"query": question},
                    "response_mode": "blocking",
                    "conversation_id": "",
                    "user": "fastmcp-user"
                },
                timeout=30  # 设置超时时间
            )
            response.raise_for_status()  # 检查 HTTP 请求是否成功
            result = response.json()
            
            # 提取所有 content 字段
            contents = []
            if 'data' in result and 'outputs' in result.get('data', {}) and 'result' in result['data']['outputs']:
                for item in result['data']['outputs']['result']:
                    if 'content' in item:
                        contents.append(item['content'])
            
            # 如果没有找到任何内容，返回提示信息
            if not contents:
                return "未找到相关内容"
            
            # 拼接所有内容并返回
            return '\n\n\n'.join(contents)

    except httpx.HTTPStatusError as e:
        print(f"HTTP 错误: {e.response.status_code} - {e.response.text}")
        return f"HTTP 错误: {e.response.status_code} - {e.response.text}"

    except httpx.RequestError as e:
        print(f"请求错误: {str(e)}")
        return "无法连接到 Dify API，请检查网络连接"

    except Exception as e:
        print(f"Dify API 调用错误: {str(e)}")
        return "检索知识时出现错误"

# # 测试函数
# async def test_services():
#     try:
#         # 测试翻译功能
#         print("测试翻译功能...")
#         test_text = "什么是 MCP 服务器？"
#         translated = await translate_to_english(test_text)
#         print(f"原文: {test_text}\n翻译结果: {translated}\n")

#         # 测试知识库检索功能
#         print("测试知识库检索功能...")
#         test_question = "MCP server的基本开发流程？"
#         knowledge = await query_dify_knowledge_base(test_question)
#         print(f"问题: {test_question}\n检索结果: {knowledge}\n")

#     except Exception as e:
#         print(f"测试过程中出现错误: {str(e)}")

# 运行测试
if __name__ == "__main__":
    mcp.run(transport='stdio')