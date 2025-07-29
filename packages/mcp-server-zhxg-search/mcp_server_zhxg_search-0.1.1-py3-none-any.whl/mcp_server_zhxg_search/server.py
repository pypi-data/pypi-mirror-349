#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MCP服务器：实现搜索API功能
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict, Optional
import aiohttp
from datetime import datetime
import sys
import argparse

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

# 设置日志
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("zhxg_search")

mcp = FastMCP("search_server", prompt="""
# 搜索 MCP 服务器

此服务器提供开源信息的搜索功能，支持关键词搜索和健康状态检查。

## 可用工具

### 1. simple_search 
使用搜索 API 搜索文档。支持以下功能：
- 布尔运算关键词搜索（OR、AND 必须大写）
- 时间范围过滤
- 自定义返回结果数量

返回数据包含：
- 文章 URL 和类型
- 网站信息（名称、域名）
- 文档内容
- 转发内容（如果有）
- 用户信息（认证状态、用户名）

### 2. health_check
检查服务器健康状态，验证服务是否正常运行。

## 错误处理

当发生以下情况时，服务将返回相应的错误信息：
- API 密钥缺失或无效
- 搜索请求失败
- 服务器异常
""")

class SimpleSearchParams(BaseModel):
    """简单搜索参数模型"""
    keywords: str = Field(..., description="搜索关键词")
    start_time: Optional[str] = Field(None, description="开始时间，格式：YYYY-MM-DD HH:MM:SS")
    end_time: Optional[str] = Field(None, description="结束时间，格式：YYYY-MM-DD HH:MM:SS")
    size: int = Field(default=10, description="返回结果数量")


class SimpleSearchData(BaseModel):
    """简单搜索数据模型"""
    url: str = Field(..., description="文档URL")
    wtype: int = Field(..., description="文档类型")
    gather: Dict[str, Any] = Field(..., description="采集信息")
    content: str = Field(..., description="文档内容")
    retweeted: Optional[Dict[str, Any]] = Field(None, description="转发内容")
    user: Optional[Dict[str, Any]] = Field(None, description="用户信息")


class SimpleSearchResult(BaseModel):
    """简单搜索结果模型"""
    data: SimpleSearchData = Field(..., description="文档数据")


class SimpleSearchResponse(BaseModel):
    """简单搜索响应模型"""
    code: int = Field(..., description="响应状态码")
    msg: str = Field(..., description="响应消息")
    data: Dict[str, Any] = Field(..., description="响应数据")


class SearchServer:
    """搜索服务器接口"""

    def __init__(self, api_key: str):
        """初始化搜索服务器"""
        self.api_url = "https://dowding-gwa.istarshine.com/api/v3/consult/search/simple"
        self.api_key = api_key

    async def simple_search(self, params: SimpleSearchParams) -> SimpleSearchResponse:
        """执行简单搜索

        Args:
            params: 搜索参数对象

        Returns:
            SimpleSearchResponse: 搜索结果
        """
        # 转换时间为时间戳
        time_range = []
        if params.start_time:
            start_timestamp = int(datetime.strptime(params.start_time, "%Y-%m-%d %H:%M:%S").timestamp())
            time_range.append(start_timestamp)
        if params.end_time:
            end_timestamp = int(datetime.strptime(params.end_time, "%Y-%m-%d %H:%M:%S").timestamp())
            time_range.append(end_timestamp)

        # 构建请求数据
        payload = {
            "keyword": params.keywords,
            "size": params.size
        }
        if time_range:
            payload["time"] = time_range

        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(self.api_url, json=payload, headers=headers) as response:
                    result = await response.json()
                    return SimpleSearchResponse(**result)
        except Exception as e:
            logger.error(f"Search request failed: {str(e)}")
            return SimpleSearchResponse(
                code=500,
                msg=f"Search failed: {str(e)}",
                data={"took": 0, "total": 0, "result": []}
            )


@mcp.tool("simple_search", description="""
使用搜索 API 搜索文档。
此工具提供了一个简单的搜索接口，支持关键词搜索和时间范围过滤。

参数说明：
- keywords (str): 搜索关键词，支持布尔运算（注：OR、AND 必须大写），例如 "香菇 OR 金针菇 OR (蘑菇 AND 美食)"
- start_time (str, optional): 开始时间，格式：YYYY-MM-DD HH:MM:SS
- end_time (str, optional): 结束时间，格式：YYYY-MM-DD HH:MM:SS
- size (int, optional): 返回结果数量，默认为 10

返回格式：
{
    "code": 200,
    "msg": "success",
    "data": {
        "took": 查询耗时,
        "total": 总结果数,
        "result": [
            {
                "data": {
                    "url": "文章URL",
                    "wtype": "文章发表类型,1：原创、2：转发、7：评论、8：弹幕",
                    "gather": {
                        "site_name": "网站名称",
                        "site_domain": "网站域名",
                        "info_flag": ["01:全量新闻、02:论坛、03:博客、04:微博、06:微信、07:视频、11:短视频、17:电视监控、21:音频电台"]
                    },
                    "content": "文档内容",
                    "retweeted": {
                        "content": "转发内容"
                    },
                    "user": {
                        "verified": "认证状态，0：未认证/未知、1：普通认证、2：机构认证",
                        "name": "用户名"
                    }
                }
            }
        ]
    }
}

示例调用：
await session.call_tool("simple_search", {
    "keywords": "香菇 OR 金针菇 OR (蘑菇 AND 美食)",
    "start_time": "2023-05-04 12:00:00",
    "end_time": "2023-05-05 12:00:00",
    "size": 10
})
""")
async def simple_search_tool(
    keywords: str,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    size: int = 10,
) -> Dict[str, Any]:
    """使用搜索API搜索文档

    Args:
        keywords: 搜索关键词
        start_time: 开始时间
        end_time: 结束时间
        size: 返回结果数量

    Returns:
        Dict[str, Any]: 搜索结果，包含状态码、消息和数据
    """
    logger.info(f"[Tool Call] 收到 simple_search 工具调用请求")
    logger.info(f"[Tool Call] 参数: keywords={keywords}, start_time={start_time}, end_time={end_time}, size={size}")

    # 创建搜索服务器实例
    search_server = SearchServer(api_key=os.environ.get('ZHXG_API_KEY', ''))

    try:
        # 构造搜索参数
        search_params = SimpleSearchParams(
            keywords=keywords,
            start_time=start_time,
            end_time=end_time,
            size=size
        )

        # 执行搜索
        logger.info("[Tool Call] 执行简单搜索...")
        results = await search_server.simple_search(search_params)
        
        # 记录结果
        if results.code == 200:
            total = results.data.get("total", 0)
            took = results.data.get("took", 0)
            logger.info(f"[Tool Call] 搜索完成 - 找到 {total} 个结果")
            logger.info(f"[Tool Call] 搜索耗时: {took}ms")
        else:
            logger.warning(f"[Tool Call] 搜索失败 - {results.msg}")

        return results.model_dump()
    except Exception as e:
        logger.error(f"[Tool Call] 搜索失败: {str(e)}")
        return {
            "code": 500,
            "msg": f"Search failed: {str(e)}",
            "data": {"took": 0, "total": 0, "result": []}
        }


@mcp.tool("health_check", description="""
检查服务器健康状态。
此工具用于验证服务器是否正常运行。

参数：
- 无需参数

返回格式：
{
    "status": "ok" 或 "error",
    "service": "服务名称"
}

示例调用：
await session.call_tool("health_check", {})
""")
async def health_check() -> Dict[str, Any]:
    """检查服务器健康状态

    Returns:
        Dict[str, Any]: 包含状态和服务名称的字典
    """
    logger.info("[Tool Call] 收到健康检查请求")
    result = {"status": "ok", "service": "search_server"}
    logger.info(f"[Tool Call] 返回健康状态: {result}")
    return result 


def main():
    parser = argparse.ArgumentParser(description="Start MCP Search Server.")
    parser.add_argument('--api-key', type=str, default=os.environ.get('ZHXG_API_KEY'), help='API key for the search API (or set ZHXG_API_KEY env variable)')
    args = parser.parse_args()
    if not args.api_key:
        print("[Error] API key must be provided via --api-key or ZHXG_API_KEY environment variable.")
        sys.exit(1)

    logger.info("[Server] 创建 MCP 服务器实例: search_server")

    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()