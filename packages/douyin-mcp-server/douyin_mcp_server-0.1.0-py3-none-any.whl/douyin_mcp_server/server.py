#!/usr/bin/env python3
"""
抖音无水印链接提取 MCP 服务器
"""

import json
import re
import requests
from mcp.server.fastmcp import FastMCP

# 创建 MCP 服务器
mcp = FastMCP("Douyin Link Extractor")

# 请求头
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/121.0.2277.107 Version/17.0 Mobile/15E148 Safari/604.1'
}


@mcp.tool()
def get_douyin_video_url(share_text: str) -> str:
    """
    从抖音分享文本中提取无水印视频链接
    
    Args:
        share_text: 包含抖音分享链接的文本
        
    Returns:
        无水印视频下载链接
    """
    try:
        # 提取分享链接
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        urls = re.findall(url_pattern, share_text)
        if not urls:
            return "错误：未找到有效的分享链接"
        
        share_url = urls[0]
        
        # 获取视频ID
        share_response = requests.get(share_url, headers=HEADERS, timeout=10)
        video_id = share_response.url.split("?")[0].strip("/").split("/")[-1]
        target_url = f'https://www.iesdouyin.com/share/video/{video_id}'
        
        # 获取视频页面
        response = requests.get(target_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        
        # 提取视频数据
        pattern = re.compile(r"window\._ROUTER_DATA\s*=\s*(.*?)</script>", re.DOTALL)
        match = pattern.search(response.text)
        
        if not match:
            return "错误：无法解析视频数据"
        
        # 解析JSON
        json_data = json.loads(match.group(1).strip())
        
        # 查找视频信息
        video_info = None
        for key in ["video_(id)/page", "note_(id)/page"]:
            if key in json_data["loaderData"]:
                video_info = json_data["loaderData"][key]["videoInfoRes"]
                break
        
        if not video_info:
            return "错误：无法找到视频信息"
        
        # 获取无水印链接
        video_data = video_info["item_list"][0]
        video_url = video_data["video"]["play_addr"]["url_list"][0]
        
        # 去除水印
        clean_url = video_url.replace("playwm", "play")
        
        return clean_url
        
    except Exception as e:
        return f"错误：{str(e)}"


def main():
    """主函数"""
    mcp.run()


if __name__ == "__main__":
    main()