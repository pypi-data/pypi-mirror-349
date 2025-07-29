import sys
import os
import traceback
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import requests

# 加载.env
load_dotenv()

CLOUD_API_URL = os.getenv("CLOUD_API_URL")
CLOUD_API_KEY = os.getenv("CLOUD_API_KEY")

mcp = FastMCP("foxbobbyMCP 多模态大模型MCP")

@mcp.tool()
def fox_chat(prompt: str, model: str = "gpt-4.1") -> str:
    """对话：调用OpenAI/Deepseek等大模型"""
    url = f"{CLOUD_API_URL}/v1/chat/completions"
    headers = {"Authorization": f"Bearer {CLOUD_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}]
    }
    resp = requests.post(url, json=data, headers=headers, timeout=60)
    resp.raise_for_status()
    return resp.json()["choices"][0]["message"]["content"]

@mcp.tool()
def fox_image(prompt: str, model: str = "dall-e-3", size: str = "1024x1024") -> str:
    """生图：调用OpenAI/Midjourney等生图接口"""
    url = f"{CLOUD_API_URL}/v1/images/generations"
    headers = {"Authorization": f"Bearer {CLOUD_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": model,
        "prompt": prompt,
        "size": size,
        "n": 1
    }
    resp = requests.post(url, json=data, headers=headers, timeout=60)
    resp.raise_for_status()
    result = resp.json()["data"][0]
    return result.get("url") or result.get("b64_json")

@mcp.tool()
def fox_audio(text: str, model: str = "tts-1", voice: str = "alloy") -> str:
    """文本转音频：调用OpenAI音频接口"""
    url = f"{CLOUD_API_URL}/v1/audio/speech"
    headers = {"Authorization": f"Bearer {CLOUD_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": model,
        "input": text,
        "voice": voice
    }
    resp = requests.post(url, json=data, headers=headers, timeout=60)
    resp.raise_for_status()
    # 这里只返回成功提示，实际可根据平台需求返回音频内容或下载链接
    return "音频已生成，请在平台查看或下载。"

def main():
    try:
        print("foxbobbyMCP 服务器启动...", file=sys.stderr)
        mcp.run()
    except Exception as e:
        print(f"启动或运行时发生错误: {str(e)}", file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 