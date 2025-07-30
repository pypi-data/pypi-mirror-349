import os
from typing import Any, Dict, Optional
import aiohttp
from datetime import datetime
import argparse

from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

mcp = FastMCP(
    name="zhxg_mcp_server", 
    instructions="""
        星光搜索：提供对互联网开源信息的布尔逻辑关键词表达式及指定时间范围的搜索能力。
    """
)

ZHXG_API_URL = "https://dowding-gwa.istarshine.com/api/v3/consult/search/simple"


class SimpleSearchParams(BaseModel):
    keywords: str = Field(..., description="搜索关键词")
    start_time: Optional[str] = Field(None, description="开始时间，格式：YYYY-MM-DD HH:MM:SS")
    end_time: Optional[str] = Field(None, description="结束时间，格式：YYYY-MM-DD HH:MM:SS")
    size: int = Field(default=10, description="返回搜索结果数量")


class SimpleSearchData(BaseModel):
    url: str = Field(..., description="原文URL")
    wtype: int = Field(..., description="原文类型")
    gather: Dict[str, Any] = Field(..., description="采集信息")
    content: str = Field(..., description="内容")
    retweeted: Optional[Dict[str, Any]] = Field(None, description="转发内容")
    user: Optional[Dict[str, Any]] = Field(None, description="用户信息")


class SimpleSearchResult(BaseModel):
    data: SimpleSearchData = Field(..., description="原文数据信息集合")


class SimpleSearchResponse(BaseModel):
    code: int = Field(..., description="响应状态码")
    msg: str = Field(..., description="响应消息")
    data: Dict[str, Any] = Field(..., description="响应数据")
    
class SearchServer:
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def simple_search(self, params: SimpleSearchParams) -> SimpleSearchResponse:
        # 如果没有设置start_time，则设置为当前时刻前 3 天
        time_range = []
        if params.start_time:
            start_timestamp = int(datetime.strptime(params.start_time, "%Y-%m-%d %H:%M:%S").timestamp())
            time_range.append(start_timestamp)
        else:
            start_timestamp = int(datetime.now().timestamp()) - 3 * 24 * 60 * 60
            time_range.append(start_timestamp)
    
        # 如果没有设置end_time，则设置为当前时刻
        if params.end_time:
            end_timestamp = int(datetime.strptime(params.end_time, "%Y-%m-%d %H:%M:%S").timestamp())
            time_range.append(end_timestamp)
        else:
            end_timestamp = int(datetime.now().timestamp())
            time_range.append(end_timestamp)

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
                async with session.post(ZHXG_API_URL, json=payload, headers=headers) as response:
                    result = await response.json()
                    return SimpleSearchResponse(**result)
        except Exception as e:
            return SimpleSearchResponse(
                code=500,
                msg=f"Search failed: {str(e)}",
                data={"took": 0, "total": 0, "result": []}
            )

@mcp.tool("simple_search", description="""
使用搜索 API 搜索文档。
此工具提供了一个简单的搜索接口，支持关键词搜索和时间范围过滤。

参数说明：
- keywords (str): 搜索关键词，支持布尔运算（注：OR、AND 必须大写），例如 "(人工智能 OR AI) AND (机器学习 OR 深度学习)"
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
) -> SimpleSearchResponse:
    """使用搜索API搜索文档

    Args:
        keywords: 搜索关键词
        start_time: 开始时间
        end_time: 结束时间
        size: 返回结果数量

    Returns:
        SimpleSearchResponse: 搜索结果，包含状态码、消息和数据
    """

    # 创建搜索服务器实例
    search_server = SearchServer(api_key=os.environ.get('ZHXG_API_KEY', ''))

    try:
        search_params = SimpleSearchParams(
            keywords=keywords,
            start_time=start_time,
            end_time=end_time,
            size=size
        )

        results = await search_server.simple_search(search_params)
        if results.code == 200:
            total = results.data.get("total", 0)
            took = results.data.get("took", 0)
            
            # 将结果转换为 SimpleSearchResult 类型
            result_list = [SimpleSearchResult(**item) for item in results.data.get("result", [])]
            
            return {
                "code": 200,
                "msg": "success",
                "data": {
                    "took": took,
                    "total": total,
                    "result": result_list
                }
            }
        else:
            return {
                "code": results.code,
                "msg": results.msg,
                "data": {"took": 0, "total": 0, "result": []}
            }
    except Exception as e:
        return {
            "code": 500,
            "msg": f"Search failed: {str(e)}",
            "data": {"took": 0, "total": 0, "result": []}
        }
        
def main():
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()