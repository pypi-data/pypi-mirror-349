from typing import Any, Dict, List, Generator
import httpx
from mcp.server.fastmcp import FastMCP
import os
from openai import OpenAI

# Initialize FastMCP server
mcp = FastMCP("essay_spider_xhs_mcp_server_lc")

# Constants
NWS_API_BASE = "http://bitouessay.com:44451"

# 获取环境中的小红书的Cookies
xhs_cookies = os.getenv("COOKIES", "")


async def make_nws_request(url: str, data: dict) -> dict[str, Any] | None:
    """Make a request to the NWS API with proper error handling."""
    headers = {
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, params=data, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None


def list_note_format_alert(note: dict) -> str:
    #     """Format an alert feature into a readable string."""
    return f"""
用户: {note.get('note_type', '')}
帖子链接: {note.get('url', '')}
帖子类型: {note.get('severity', '暂无')}
帖子标题: {note.get('display_title', '暂无')}
帖子信息列表: {note.get('note_info_list', '暂无')}
"""


def item_note_format_alert(note: dict) -> str:
    return f"""
    帖子链接: {note.get('note_url', '')}
    帖子类型: {note.get('note_type', '暂无')}
    帖子标题: {note.get('title', '暂无')}
    帖子描述: {note.get('desc', '暂无')}
    帖子喜欢数：{note.get('liked_count', '0')}
    帖子评论数：{note.get('comment_count', '0')}
    帖子收藏数：{note.get('collected_count', '0')}
    """



@mcp.tool()
async def spider_note(note_url: str) -> str | dict[str, Any] | None:
    """获取小红书一篇帖子内容

    Args:
        :param cookies: 小红书Cookies
        :param note_url: 小红书帖子链接
    """
    if not xhs_cookies or len(xhs_cookies) < 10:  # 简单验证
        raise ValueError("无效的cookies格式，请提供有效的小红书cookies")
    url = f"{NWS_API_BASE}/notes/item"
    data = {'note_url': note_url, 'cookies_str': xhs_cookies}
    result = await make_nws_request(url, data)
    if not result or "info" not in result:
        return "爬取失败，请检查cookies或者小红书帖子是否正确"

    if not result["info"]:
        return "爬取失败，请检查cookies或者小红书帖子是否正确"
    # 将图片数组组合成字符串
    media = ''
    if result['info']['note_type'] == '图集':
        media = ";\n".join(result["info"]["image_list"])
        media = '帖子图片列表：' + media
    elif result['info']['note_type'] == '视频':
        media = '帖子视频需要单独获取'
    return item_note_format_alert(result['info']) + media


@mcp.tool()
async def spider_user_notes(user_url: str) -> str | list[str]:
    """获取用户下的所有帖子

    Args:
        :param user_url: 用户主页链接
        :param cookies: 小红书Cookies
    """
    if not xhs_cookies or len(xhs_cookies) < 10:  # 简单验证
        raise ValueError("无效的cookies格式，请提供有效的小红书cookies")
    url = f"{NWS_API_BASE}/user/item"
    data = {'user_url': user_url, 'cookies_str': xhs_cookies}
    result = await make_nws_request(url, data)
    if not result or "list" not in result:
        return "爬取失败，请检查cookies或者小红书帖子是否正确"

    if not result["list"]:
        return "爬取失败，请检查cookies或者小红书帖子是否正确"
    return [list_note_format_alert(note) for note in result['list']]


@mcp.tool(name="获取小红书视频链接", description="通过对小红书的链接获取到里面的视频链接，note_url: 小红书链接")
async def get_video_src(note_url: str) -> str | dict[str, Any] | None:
    url = f"{NWS_API_BASE}/notes/video"
    data = {'note_url': note_url}
    result = await make_nws_request(url, data)
    if not result or "video" not in result:
        return "爬取失败，请检查小红书帖子链接是否正确"

    if not result["video"]:
        return "爬取失败，请检查小红书帖子链接是否正确"
    return result


def run():
    mcp.run()


if __name__ == "__main__":
    run()
