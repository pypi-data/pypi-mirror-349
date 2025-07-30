from typing import Any, Dict, Optional
import httpx
import csv
import os
import sys
from mcp.server.fastmcp import FastMCP


import requests
from datetime import datetime, timedelta
import json

def main() -> int:
    mcp = FastMCP("amap-weather-mcp-server")

    AMAP_API_BASE = "https://restapi.amap.com/v3/weather/weatherInfo"
    AMAP_API_KEY = os.environ.get("AMAP_API_KEY", "")
    USER_AGENT = "amap-weather-mcp-server/1.0"

    city_to_adcode = {}

def load_city_adcode_map():
    """加载城市名称到adcode的映射"""
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(current_dir, "AMap_adcode_citycode.csv")
        
        with open(csv_file_path, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # 跳过表头
            for row in reader:
                if len(row) >= 2:
                    city_name = row[0].strip()
                    adcode = row[1].strip()
                    city_to_adcode[city_name] = adcode
        return True
    except Exception as e:
        print(f"加载城市编码文件失败: {e}")
        return False

# 初始加载城市编码数据
load_city_adcode_map()

def get_adcode_by_city(city_name: str) -> Optional[str]:
    """根据城市名称查找对应的adcode
    
    Args:
        city_name: 城市名称，如"北京市"、"上海市"等
        
    Returns:
        城市对应的adcode，如果未找到则返回None
    """
    # 先尝试直接匹配
    if city_name in city_to_adcode:
        return city_to_adcode[city_name]
    
    # 如果未找到，尝试添加"市"或"省"后缀再查找
    if not city_name.endswith("市") and not city_name.endswith("省"):
        city_with_suffix = city_name + "市"
        if city_with_suffix in city_to_adcode:
            return city_to_adcode[city_with_suffix]
            
        city_with_suffix = city_name + "省"
        if city_with_suffix in city_to_adcode:
            return city_to_adcode[city_with_suffix]
    
    # 对于区级城市，尝试判断是否为区名
    for full_name, code in city_to_adcode.items():
        if city_name in full_name and (full_name.endswith("区") or "区" in full_name):
            return code
    
    return None

async def make_amap_request(params: Dict[str, str]) -> Dict[str, Any]:
    """向高德地图API发送请求并获取天气数据
    
    Args:
        params: API请求参数
        
    Returns:
        API返回的JSON数据，如果请求失败则返回None
    """
    # 添加公共参数
    params["key"] = AMAP_API_KEY
    
    headers = {
        "User-Agent": USER_AGENT
    }
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(AMAP_API_BASE, params=params, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"API请求失败: {e}")
            return None

def format_current_weather(weather_data: Dict[str, Any]) -> str:
    """格式化实时天气信息
    
    Args:
        weather_data: 高德地图API返回的天气数据
        
    Returns:
        格式化后的天气信息字符串
    """
    if not weather_data or "lives" not in weather_data or not weather_data["lives"]:
        return "无法获取天气信息或数据格式错误"
    
    live = weather_data["lives"][0]
    
    return f"""
城市: {live.get('city', '未知')}
天气: {live.get('weather', '未知')}
温度: {live.get('temperature', '未知')}°C
风向: {live.get('winddirection', '未知')}
风力: {live.get('windpower', '未知')}级
湿度: {live.get('humidity', '未知')}%
发布时间: {live.get('reporttime', '未知')}
"""

def format_forecast_weather(weather_data: Dict[str, Any]) -> str:
    """格式化天气预报信息
    
    Args:
        weather_data: 高德地图API返回的天气预报数据
        
    Returns:
        格式化后的天气预报信息字符串
    """
    if not weather_data or "forecasts" not in weather_data or not weather_data["forecasts"]:
        return "无法获取天气预报信息或数据格式错误"
    
    forecast = weather_data["forecasts"][0]
    city = forecast.get('city', '未知')
    casts = forecast.get('casts', [])
    
    if not casts:
        return f"{city}: 无天气预报数据"
    
    forecasts = []
    for cast in casts:
        day_forecast = f"""
日期: {cast.get('date', '未知')}
白天天气: {cast.get('dayweather', '未知')}
白天温度: {cast.get('daytemp', '未知')}°C
白天风向: {cast.get('daywind', '未知')}
白天风力: {cast.get('daypower', '未知')}级
夜间天气: {cast.get('nightweather', '未知')}
夜间温度: {cast.get('nighttemp', '未知')}°C
夜间风向: {cast.get('nightwind', '未知')}
夜间风力: {cast.get('nightpower', '未知')}级
"""
        forecasts.append(day_forecast)
    
    return f"城市: {city}\n\n" + "\n---\n".join(forecasts)

@mcp.tool()
async def get_current_weather(city: str) -> str:
    """获取指定城市的实时天气
    
    Args:
        city: 中国城市名称，如"北京市"、"上海市"、"广州市"等
    """
    adcode = get_adcode_by_city(city)
    if not adcode:
        return f"无法找到城市'{city}'的编码，请检查城市名称是否正确"
    
    params = {
        "city": adcode,
        "extensions": "base"  # 获取实时天气
    }
    
    data = await make_amap_request(params)
    
    if not data:
        return f"获取{city}的天气信息失败"
    
    if data.get("status") != "1":
        return f"API返回错误: {data.get('info', '未知错误')}"
    
    return format_current_weather(data)


@mcp.tool()
async def get_weather_forecast(city: str) -> str:
    """获取指定城市的天气预报（未来3-4天）

    Args:
        city: 中国城市名称，如"北京市"、"上海市"、"广州市"等
    """
    adcode = get_adcode_by_city(city)
    if not adcode:
        return f"无法找到城市'{city}'的编码，请检查城市名称是否正确"

    params = {
        "city": adcode,
        "extensions": "all"  # 获取未来天气预报
    }

    data = await make_amap_request(params)

    if not data:
        return f"获取{city}的天气预报失败"

    if data.get("status") != "1":
        return f"API返回错误: {data.get('info', '未知错误')}"

    return format_forecast_weather(data)
def get_date_based_on_check_date(check_date):
    # 获取今天的日期
    today = datetime.today().date()

    # 根据输入的 check_date 返回相应的日期
    if check_date == "昨天":
        return today.strftime('%Y-%m-%d')
    elif check_date == "前天":
        yesterday = today - timedelta(days=1)
        return yesterday.strftime('%Y-%m-%d')
    else:
        return "Invalid input: check_date should be '昨天' or '前天'."


@mcp.tool()
async def get_sleep_data(check_date: str) -> str:
    """查询某个日期的睡眠报告、睡眠情况、睡得怎么样

    Args:
         check_date: 需要查询的日期，如"昨天"、"昨天晚上"、"昨晚"、"昨晚"、"前天"、"前天晚上"、"%Y-%m-%d"、"某个日期"等
    """
    if (check_date == "昨天" or check_date == "昨天晚上" or check_date == "昨晚"):
        check_date = "昨天"
        check_date = get_date_based_on_check_date(check_date)
    if (check_date == "前天" or check_date == "前天晚上"):
        check_date = "前天"
        check_date = get_date_based_on_check_date(check_date)
    check_date = check_date + " 08:00:00"
    deviceid = "00:11:22:33:44:55"

    url = "http://58.59.43.166:8083/test/getms?deviceid=" + deviceid + "&datetime=" + check_date

    response = requests.get(url)
    response.raise_for_status()

    sleep_status_map = {
        "5": "清醒",
        "4": "眼动睡眠",
        "3": "浅睡",
        "2": "中睡",
        "1": "深睡",
        "0": "深度睡眠"
    }
    parsed_data = json.loads(response.text)
    devices = parsed_data.get("data", [])
    # 遍历设备数据并生成自然语言
    # 定义字符串变量 notelist 来保存输出
    notelist = ""
    # return devices
    # 遍历设备数据并生成自然语言
    for device in devices:
        mac = device.get("mac")
        sleeptime = datetime.strptime(device.get("sleeptime"), "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")
        waketime = datetime.strptime(device.get("waketime"), "%Y-%m-%dT%H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

        time_format = "%Y-%m-%d %H:%M:%S"
        time1 = datetime.strptime(sleeptime, time_format)
        time2 = datetime.strptime(waketime, time_format)
        # 计算时间差
        time_difference = time2 - time1

        # 提取总秒数
        total_seconds = time_difference.total_seconds()

        # 转换为小时和分钟
        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)

        # 输出结果
        print(f"时间差: {hours}小时{minutes}分")
        heartrate = device.get("heartrate")
        resp = device.get("resp")
        device_note = device.get("device_note")
        sleep_status = device.get("sleep_status", "").split(",")

        # 转换 sleep_status 为自然语言描述
        sleep_status_descriptions = [sleep_status_map.get(status, "未知") for status in sleep_status]

        # 计算各种睡眠状态的占比
        total_status_count = len(sleep_status)
        sleep_status_counts = {status: sleep_status.count(status) for status in sleep_status_map.keys()}
        sleep_status_ratios = {
            sleep_status_map[status]: f"{(count / total_status_count) * 100:.2f}%"
            for status, count in sleep_status_counts.items() if count > 0
        }

        # 构造字符串并追加到 notelist
        notelist += f"设备别名：（{device_note}）：\n"
        notelist += f"- 入睡时间：{sleeptime}\n"
        notelist += f"- 起床时间：{waketime}\n"
        notelist += f"- 睡眠时长：{hours}小时{minutes}分\n"
        notelist += f"- 静息心率：{heartrate}\n"
        notelist += f"- 静息呼吸率：{resp}\n"
        # notelist += f"- 睡眠状态：{'，'.join(sleep_status_descriptions)}\n"
        notelist += f"- 各种睡眠状态占比：\n"
        for status, ratio in sleep_status_ratios.items():
            notelist += f"  - {status}: {ratio}\n"
        notelist += "\n"

    # 打印 notelist 字符串
    print(notelist)
    if not devices:
        return "抱歉，未能获取到睡眠报告。"
    # lang="英语"
    # selected_news={}
    # selected_news['title']="睡眠报告"
    # selected_news ['pubDate']= check_date
    # selected_news = "睡的不错"
    sleep_report = (
        f"查询到以下睡眠报告{notelist}\n\n"

        f"结合用户需要的查询的设备别名和查询到的睡眠报告，给用户提供睡眠报告\n"
        f"(请以自然、流畅的方式向用户播报这条睡眠报告，输出睡眠报告时不要用‘我’，睡眠报告对象是‘设备别称’的使用者，请详细入睡时间、起床时间、静息心率、静息呼吸率、深度睡眠。"

    )

    return sleep_report


@mcp.tool()
async def get_monitor_data(checkname: str) -> str:
    """查询服务器监控数据 包括 CPU利用率、内存使用量、内存利用率、内网出带宽、内网入带宽

    Args:
         checkname: 需要查询指标，如"CPU利用率"、"内存使用量"、"内存利用率"、"内网出带宽"、"内网入带宽""等
    """
    type="-1"
    if (checkname == "CPU利用率" ):
        type = "0"

    if (checkname == "内存使用量"):
        type = "1"
    if (checkname == "内存利用率" ):
        type = "2"
    if (checkname == "内网出带宽" ):
        type = "3"
    if (checkname == "内网入带宽" ):
        type = "4"

    #  http://58.59.43.166:8083/test/getms1

    url = "http://58.59.43.166:8083/test/getms1?type=" + type

    response = requests.get(url)
    response.raise_for_status()


    parsed_data = json.loads(response.text)
    devices = parsed_data.get("data", "")
    # 遍历设备数据并生成自然语言
    # 定义字符串变量 notelist 来保存输出

    if devices == "":
        return "抱歉，未能获取到相关信息。"
    if type=="-1":
        return "抱歉，未能获取到相关信息。"
    if type!="-1":
        url = "http://58.59.43.166:8083/test/getmsmo?type=" + type

        response = requests.get(url)
        response.raise_for_status()


        parsed_data = json.loads(response.text)
        datas = parsed_data.get("data", [])

        if len(datas)==1:
            if datas[0]["name"]=="百分比":
                return "当前的"+str(datas[0]["title"])+"是百分之"+str(datas[0]["value"])
            else:
                return "当前的" + str(datas[0]["title"]) + "是" + str(datas[0]["value"])+ str(datas[0]["name"])
        else:
            return "抱歉，未能获取到相关信息。"




    return "抱歉，未能获取到相关信息。"


@mcp.tool()
async def search_city(keyword: str) -> str:
    """根据关键词搜索匹配的城市
    
    Args:
        keyword: 城市名称关键词
    """
    matched_cities = []
    
    for city_name in city_to_adcode.keys():
        if keyword in city_name:
            matched_cities.append(city_name)
    
    if not matched_cities:
        return f"未找到包含'{keyword}'的城市"
    
    return "找到以下匹配的城市:\n" + "\n".join(matched_cities[:20])

#if __name__ == "__main__":
    # 初始化并运行服务器
    # mcp.run(transport='stdio')
   # mcp.run(transport='sse')

if __name__ == "__main__":
    sys.exit(main())
