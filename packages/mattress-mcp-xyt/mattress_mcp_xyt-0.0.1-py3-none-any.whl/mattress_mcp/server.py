"""
MCP server for Odoo integration

Provides MCP tools and resources for interacting with Odoo ERP systems
"""

import json
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, AsyncIterator, Dict, List, Optional, Union, cast

from mcp.server.fastmcp import Context, FastMCP


# Create MCP server
mcp = FastMCP(
    "Odoo MCP Server",
    description="MCP Server for interacting with Odoo ERP systems",
    dependencies=["requests"]
)

# ----- MCP Tools -----

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