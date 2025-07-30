from mcp.server.fastmcp import FastMCP
from pydantic import Field
import httpx
import json
import os
from dotenv import load_dotenv
import logging

logger = logging.getLogger("mcp")

# Initialize FastMCP server
mcp = FastMCP("weather")
# 加载环境变量
load_dotenv()


# 定义工具
@mcp.tool(description="高德天气查询，输入城市名，返回该城市的天气情况，例如：北京")
async def query_weather(city: str = Field(description="要查询天气的城市名称")) -> str:
    """
    高德天气查询

    Args:
        city: 要查询天气的城市名称

    Returns:
        要查询城市的天气信息
    """

    logger.info("收到查询天气请求，city_name：{}".format(city))
    api_key = os.getenv("GAODE_KEY")
    if not api_key:
        return "请先设置GAODE_KEY环境变量"
    api_domain = 'https://restapi.amap.com/v3'
    url = f"{api_domain}/config/district?keywords={city}"f"&subdistrict=0&extensions=base&key={api_key}"
    headers = {"Content-Type": "application/json; charset=utf-8"}
    async with httpx.AsyncClient(headers=headers) as client:
        response = await client.get(url)
        if response.status_code != 200:
            return "查询失败"

        city_info = response.json()
        if city_info["info"] != "OK":
            return "获取城市信息查询失败"
        CityCode = city_info['districts'][0]['adcode']
        weather_url = f"{api_domain}/weather/weatherInfo?city={CityCode}&extensions=all&key={api_key}"
        weatherInfo_response = await client.get(weather_url)
        if weatherInfo_response.status_code != 200:
            return "查询天气信息失败"
        weatherInfo = weatherInfo_response.json()
        if weatherInfo['info'] != "OK":
            return "查询天气信息失败"
        weatherInfo_data = weatherInfo_response.json()
        contents = []
        if len(weatherInfo_data.get('forecasts')) <= 0:
            return "没有获取到该城市的天气信息"
        for item in weatherInfo_data['forecasts'][0]['casts']:
            content = {
                'date': item.get('date'),
                'week': item.get('week'),
                'dayweather': item.get('dayweather'),
                'daytemp_float': item.get('daytemp_float'),
                'daywind': item.get('daywind'),
                'nightweather': item.get('nightweather'),
                'nighttemp_float': item.get('nighttemp_float')
            }
            contents.append(content)
        return json.dumps(contents, ensure_ascii=False)


if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')
