from datetime import datetime, timedelta 
from enum import Enum 
import json 
from typing import Sequence 

from zoneinfo import ZoneInfo
from mcp.server import Server 
from mcp.server.stdio import stdio_server 
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource 
from mcp.shared.exceptions import McpError 

from pydantic import BaseModel 


class TimeTools(str, Enum):
    GET_CURRENT_TIME = "get_current_time"
    COVERT_TIME = "covert_time"

class TimeResult(BaseModel):
    timezone: str 
    datetime: str 
    is_dst: bool 

class TimeConversionResult(BaseModel):
    # 输入， 输出， 时差
    source: TimeResult 
    target: TimeResult 
    time_difference: str 

class TimeConversionInput(BaseModel):
    # 输入的市区，当前时间， 目标时区的列表
    source_tz: str 
    time: str 
    target_tz_list: list[str] 

def get_local_tz(local_tz_override: str | None = None) -> ZoneInfo:
    # 如果需要覆盖为新的时区，更新为下一个时区，要等
    if local_tz_override:
        return ZoneInfo(local_tz_override)
    
    # Get local timezone from datetime.now()    
    tzinfo = datetime.now().astimezone(tz=None).tzinfo
    """
    .now() 获取当前时间
    .astimezone(tz=none) # 将时间转换为带时区的对象，tz=None表示默认时区
    .tzinfo 提取时区信息  
    """
    if tzinfo is not None:
        return ZoneInfo(str(tzinfo))
    raise McpError("Could not determine local timezone - tzinfo is None")

def get_zoneinfo(timezone_name: str) -> ZoneInfo:
    try: 
        return ZoneInfo(timezone_name)
    except Exception as e:
        raise McpError(f"Invalid timezone: {str(e)}")
    
class TimeServer:
    def get_current_time(self, timezone_name: str) -> TimeResult:
        """Get currrent time in specified timezone_name"""
        timezone = get_zoneinfo(timezone_name)
        current_time = datetime.now(timezone)

        return TimeResult(
            timezone=timezone_name,
            datetime=current_time.isoformat(timespec="seconds"), # ISO格式时间，精确到秒
            is_dst=bool(current_time.dst()), # 是否夏令时
        )
    
    def convert_time(self, source_tz: str, time_str: str, target_tz: str) -> TimeConversionResult:
        """Convert time between timezones"""
        # 获取时区对象
        source_timezone = get_zoneinfo(source_tz)
        target_timezone = get_zoneinfo(target_tz)

        # 解析输入时间，确保输入格式无误
        try:
            parsed_time = datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            raise ValueError("Invalid time format. Expected HH:MM [24-hour format]")
        
        now = datetime.now(source_timezone)
        source_time = datetime(
            now.year, 
            now.month,
            now.day, 
            parsed_time.hour, 
            parsed_time.minute, 
            tzinfo=source_timezone,
        )

        # 转为目标时区
        target_time = source_time.astimezone(target_timezone)
        # 获取时差
        source_offset = source_time.utcoffset() or timedelta() 
        target_offset = target_time.utcoffset() or timedelta()
        hours_difference = (target_offset - source_offset).total_seconds() / 3600 

        if hours_difference.is_integer():
            time_diff_str = f"{hours_difference:+.1f}h"
        else:
            time_diff_str = f"{hours_difference:+.2f}".rstrip("0").rstrip(".") + "h"

        return TimeConversionResult(
            source=TimeResult(
                timezone=source_tz,
                datetime=source_time.isoformat(timespec="seconds"),
                is_dst=bool(source_time.dst()),
            ),
            target=TimeResult(
                timezone=target_tz,
                datetime=target_time.isoformat(timespec="seconds"),
                is_dst=bool(target_time.dst()),
            ),
            time_difference=time_diff_str,
        )

async def serve(local_timezone: str | None = None) -> None:
    server = Server("mcp-time")
    time_server = TimeServer() 
    local_tz = str(get_local_tz(local_timezone))

    @server.list_tools() 
    async def list_tools() -> list[Tool]:
        """List available time tools."""
        return [
            Tool(
                name=TimeTools.GET_CURRENT_TIME.value,
                description="Get current time in a specific timezones", 
                inputSchema={
                    "type": "object", 
                    "properties": {
                        "timezone": {
                            "type": "string",
                            "description": f"IANA timezone name (e.g., 'America/New_York', 'Europe/London'). Use '{local_tz}' as local timezone if no timezone provided by the user.",
                        }
                    },
                    "required": ["timezone"],
                },
            ),
             Tool(
                name=TimeTools.CONVERT_TIME.value,
                description="Convert time between timezones",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "source_timezone": {
                            "type": "string",
                            "description": f"Source IANA timezone name (e.g., 'America/New_York', 'Europe/London'). Use '{local_tz}' as local timezone if no source timezone provided by the user.",
                        },
                        "time": {
                            "type": "string",
                            "description": "Time to convert in 24-hour format (HH:MM)",
                        },
                        "target_timezone": {
                            "type": "string",
                            "description": f"Target IANA timezone name (e.g., 'Asia/Tokyo', 'America/San_Francisco'). Use '{local_tz}' as local timezone if no target timezone provided by the user.",
                        },
                    },
                    "required": ["source_timezone", "time", "target_timezone"],
                },
            ),
        ]
        
    @server.call_tool() 
    async def call_tool(
        name: str, arguments: dict 
    ) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """Handle tool calls for time queries"""
        try:
            match name:
                case TimeTools.GET_CURRENT_TIME.value:
                    timezone = arguments.get("timezone")
                    if not timezone:
                        raise ValueError("Missing required argument: timezone")

                    result = time_server.get_current_time(timezone)

                case TimeTools.CONVERT_TIME.value:
                    if not all(
                        k in arguments for k in ['source_timezone', 'time', 'target_timezone']
                    ):
                        raise ValueError("Missing required arguments: source_timezone, time, target_timezone")

                    result = time_server.convert_time(
                        arguments["source_timezone"],
                        arguments["time"],
                        arguments["target_timezone"],
                    )
                case _:
                    raise ValueError(f"Unknown tool: {name}")
                
            return [
                TextContent(type="text", text=json.dumps(result.model_dump(), indent=2))
            ]
        
        except Exception as e:
            raise ValueError(f"Error processing mcp-server-time query: {str(e)}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options) 
