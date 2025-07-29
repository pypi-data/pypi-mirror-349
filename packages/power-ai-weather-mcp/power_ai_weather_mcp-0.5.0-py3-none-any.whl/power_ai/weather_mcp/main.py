import json
import logging
import os
import uuid
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from power_ai.common.sign import make_payload

# 加载配置
load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

mcp = FastMCP(
    name="Weather Service",
    host=os.getenv("MCP_SERVER_HOST", "0.0.0.0"),
    port=int(os.getenv("MCP_SERVER_PORT", "8000")),
)

# 创建会话，设置重试机制
session = requests.session()
retry = Retry(connect=3, backoff_factor=0.5)
adapter = HTTPAdapter(max_retries=retry)
session.mount("http://", adapter)
session.mount("https://", adapter)


class Location(BaseModel):
    """位置信息模型"""

    id: Optional[str] = None
    name: Optional[str] = None
    country: Optional[str] = None
    path: Optional[str] = None
    timezone: Optional[str] = None
    timezone_offset: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None

    class Config:
        extra = "ignore"  # 忽略额外的字段


class WeatherNow(BaseModel):
    """实时天气模型"""

    text: Optional[str] = Field(None, description="天气状况")
    code: Optional[str] = Field(None, description="天气状况代码")
    temperature: Optional[str] = Field(None, description="实时温度")
    feels_like: Optional[str] = Field(None, description="体感温度")
    pressure: Optional[str] = Field(None, description="气压(百帕)")
    humidity: Optional[str] = Field(None, description="相对湿度(%)")
    visibility: Optional[str] = Field(None, description="能见度(公里)")
    wind_direction: Optional[str] = Field(None, description="风向")
    wind_direction_degree: Optional[str] = Field(None, description="风向角度(度)")
    wind_speed: Optional[str] = Field(None, description="风速(公里/小时)")
    wind_scale: Optional[str] = Field(None, description="风力等级")
    clouds: Optional[str] = Field(None, description="云量(%)")
    dew_point: Optional[str] = Field(None, description="露点温度(摄氏度)")
    ultraviolet: Optional[str] = Field(None, description="紫外线指数")

    class Config:
        extra = "ignore"  # 忽略额外的字段


class WeatherForecast(BaseModel):
    """天气预报模型"""

    date: Optional[str] = Field(None, description="预报日期")
    text_day: Optional[str] = Field(None, description="白天天气状况")
    code_day: Optional[str] = Field(None, description="白天天气代码")
    text_night: Optional[str] = Field(None, description="夜间天气状况")
    code_night: Optional[str] = Field(None, description="夜间天气代码")
    high: Optional[str] = Field(None, description="最高温度(摄氏度)")
    low: Optional[str] = Field(None, description="最低温度(摄氏度)")
    rainfall: Optional[str] = Field(None, description="降水量(毫米)")
    precip: Optional[str] = Field(None, description="降水概率(%)")
    wind_direction: Optional[str] = Field(None, description="风向")
    wind_direction_degree: Optional[str] = Field(None, description="风向角度(度)")
    wind_speed: Optional[str] = Field(None, description="风速(公里/小时)")
    wind_scale: Optional[str] = Field(None, description="风力等级")
    sun_rise: Optional[str] = Field(None, description="日出时间")
    sun_set: Optional[str] = Field(None, description="日落时间")
    moon_rise: Optional[str] = Field(None, description="月升时间")
    moon_set: Optional[str] = Field(None, description="月落时间")

    class Config:
        extra = "ignore"  # 忽略额外的字段


class AirQuality(BaseModel):
    """空气质量模型"""

    aqi: Optional[str] = Field(None, description="空气质量指数")
    pm25: Optional[str] = Field(None, description="PM2.5浓度(微克/立方米)")
    pm10: Optional[str] = Field(None, description="PM10浓度(微克/立方米)")
    so2: Optional[str] = Field(None, description="二氧化硫浓度(微克/立方米)")
    no2: Optional[str] = Field(None, description="二氧化氮浓度(微克/立方米)")
    o3: Optional[str] = Field(None, description="臭氧浓度(微克/立方米)")
    co: Optional[str] = Field(None, description="一氧化碳浓度(毫克/立方米)")
    quality: Optional[str] = Field(None, description="空气质量等级")
    qualityCode: Optional[str] = Field(None, description="空气质量代码")

    class Config:
        extra = "ignore"  # 忽略额外的字段


class LifeSuggestion(BaseModel):
    """生活指数模型"""

    brief: Optional[str] = Field(None, description="指数简述")
    details: Optional[str] = Field(None, description="详细建议")

    class Config:
        extra = "ignore"  # 忽略额外的字段


class WeatherAlarm(BaseModel):
    """天气预警模型"""

    type: Optional[str] = Field(None, description="预警类型")
    level: Optional[str] = Field(None, description="预警等级")
    title: Optional[str] = Field(None, description="预警标题")
    text: Optional[str] = Field(None, description="预警内容")
    pub_time: Optional[str] = Field(None, description="发布时间")

    class Config:
        extra = "ignore"  # 忽略额外的字段


class Typhoon(BaseModel):
    """台风信息模型"""

    id: Optional[str] = Field(None, description="台风编号")
    name: Optional[str] = Field(None, description="台风名称")
    en_name: Optional[str] = Field(None, description="英文名称")
    level: Optional[str] = Field(None, description="台风等级")
    pressure: Optional[float] = Field(None, description="气压(百帕)")
    wind_speed: Optional[float] = Field(None, description="风速(公里/小时)")
    move_speed: Optional[float] = Field(None, description="移动速度(公里/小时)")
    move_direction: Optional[str] = Field(None, description="移动方向")
    lat: Optional[float] = Field(None, description="纬度")
    lon: Optional[float] = Field(None, description="经度")

    class Config:
        extra = "ignore"  # 忽略额外的字段


class Precipitation(BaseModel):
    """降水预报模型"""

    precipitation: Optional[List[float]] = Field(None, description="降水量(毫米)")
    probability: Optional[List[float]] = Field(None, description="降水概率(%)")
    description: Optional[str] = Field(None, description="降水描述")

    class Config:
        extra = "ignore"  # 忽略额外的字段


class WeatherService:
    """天气服务实现类"""

    def __init__(self):
        # app_id 和 app_secret 从环境变量中获取
        self.app_id = os.getenv("APP_ID")
        self.app_secret = os.getenv("APP_SECRET")
        assert self.app_id and self.app_secret, "APP_ID 和 APP_SECRET 不能为空"
        # 设置请求头
        self.headers = {"content-type": "application/json"}
        # 请求相关
        self.endpoint = os.getenv("WEATHER_ENDPOINT")
        self.device_id = os.getenv("WEATHER_DEVICE_ID", str(uuid.uuid4()))
        self.lang = os.getenv("WEATHER_LANGUAGE", "zh-cn")
        self.unit = os.getenv("WEATHER_UNIT", "c")  # 默认的温度单位
        self.timeout = int(os.getenv("WEATHER_REQUEST_TIMEOUT", "10"))

        # 路径相关
        self.path_weather_now = "/api/2/infotainment/weather/now"
        self.path_weather_daily = "/api/2/infotainment/weather/daily"
        self.path_weather_hourly = "/api/2/infotainment/weather/hourly"
        self.path_weather_yesterday = "/api/2/infotainment/weather/daily/history"  # 新
        self.path_weather_alarm = "/api/2/infotainment/weather/alarm"
        self.path_air_quality_now = "/api/2/infotainment/weather/air/now"
        self.path_location_search = "/api/2/infotainment/weather/location/search"
        self.path_info_now = "/api/2/infotainment/weather/info/now"
        self.path_sunrise_sunset = "/api/2/infotainment/weather/geo/sun"
        self.path_life_suggestion = "/api/2/infotainment/weather/life/suggestion"
        self.path_precipitation = "/api/2/infotainment/weather/precipitation"  # 新
        self.path_typhoon = "/api/2/infotainment/weather/typhoon"  # 新

    async def get_weather_now(self, location: str) -> Optional[WeatherNow]:
        """获取实时天气"""
        # 构造请求
        path = self.path_weather_now
        data = {
            "location": json.dumps({"area": location}),
            "device_id": self.device_id,
            "lang": self.lang,
            "unit": self.unit,
        }
        payload = make_payload(
            path=path,
            method="GET",
            app_id=self.app_id,
            app_secret=self.app_secret,
            data=data,
            content_type="json",
        )

        # 发送请求
        url = self.endpoint + path
        response = session.get(
            url, params=payload, headers=self.headers, timeout=self.timeout
        ).json()
        if response.get("result_code") != "success" or "data" not in response:
            logging.error(f"获取实时天气失败: {response}")
            return None

        # 处理返回结果
        weather_data = response["data"][0].get("now", {})
        if not weather_data:
            logging.error("返回的实时天气数据为空")
            return None

        return WeatherNow(**weather_data)

    async def get_weather_forecast_hourly(
        self, location: str, start: int = 1, hours: int = 24
    ) -> List[WeatherForecast]:
        """获取小时级天气预报"""
        # 构造请求
        path = self.path_weather_hourly
        data = {
            "location": json.dumps({"area": location}),
            "device_id": self.device_id,
            "lang": self.lang,
            "unit": self.unit,
            "start": start,
            "hours": hours,
        }
        payload = make_payload(
            path=path,
            method="GET",
            app_id=self.app_id,
            app_secret=self.app_secret,
            data=data,
            content_type="json",
        )

        # 发送请求
        url = self.endpoint + path
        response = session.get(
            url, params=payload, headers=self.headers, timeout=self.timeout
        ).json()
        if response.get("result_code") != "success" or "data" not in response:
            logging.error(f"获取小时级天气预报失败: {response}")
            return []

        # 处理返回结果
        hourly_data = response["data"][0].get("hourly", [])
        if not hourly_data:
            logging.error("返回的小时级天气预报数据为空")
            return []

        return [WeatherForecast(**item) for item in hourly_data]

    async def get_weather_forecast_daily(
        self, location: str, start: int = 0, days: int = 7
    ) -> List[WeatherForecast]:
        """获取天级天气预报"""
        # 构造请求
        path = self.path_weather_daily
        data = {
            "location": json.dumps({"area": location}),
            "device_id": self.device_id,
            "lang": self.lang,
            "unit": self.unit,
            "start": start,
            "days": days,
        }
        payload = make_payload(
            path=path,
            method="GET",
            app_id=self.app_id,
            app_secret=self.app_secret,
            data=data,
            content_type="json",
        )

        # 发送请求
        url = self.endpoint + path
        response = session.get(
            url, params=payload, headers=self.headers, timeout=self.timeout
        ).json()
        if response.get("result_code") != "success" or "data" not in response:
            logging.error(f"获取天级天气预报失败: {response}")
            return []

        # 处理返回结果
        daily_data = response["data"][0].get("daily", [])
        if not daily_data:
            logging.error("返回的天级天气预报数据为空")
            return []

        return [WeatherForecast(**item) for item in daily_data]

    async def get_air_quality(self, location: str) -> Optional[AirQuality]:
        """获取空气质量"""
        # 构造请求
        path = self.path_air_quality_now
        data = {
            "location": json.dumps({"area": location}),
            "device_id": self.device_id,
            "lang": self.lang,
        }
        payload = make_payload(
            path=path,
            method="GET",
            app_id=self.app_id,
            app_secret=self.app_secret,
            data=data,
            content_type="json",
        )

        # 发送请求
        url = self.endpoint + path
        response = session.get(
            url, params=payload, headers=self.headers, timeout=self.timeout
        ).json()
        if response.get("result_code") != "success" or "data" not in response:
            logging.error(f"获取空气质量失败: {response}")
            return None

        # 处理返回结果
        air_data = response["data"][0].get("air", {}).get("city", {})
        if not air_data:
            logging.error("返回的空气质量数据为空")
            return None

        return AirQuality(**air_data)

    async def get_life_suggestion(self, location: str) -> Dict[str, LifeSuggestion]:
        """获取生活指数"""
        # 构造请求
        path = self.path_life_suggestion
        data = {
            "location": json.dumps({"area": location}),
            "device_id": self.device_id,
            "lang": self.lang,
        }
        payload = make_payload(
            path=path,
            method="GET",
            app_id=self.app_id,
            app_secret=self.app_secret,
            data=data,
            content_type="json",
        )

        # 发送请求
        url = self.endpoint + path
        response = session.get(
            url, params=payload, headers=self.headers, timeout=self.timeout
        ).json()
        if response.get("result_code") != "success" or "data" not in response:
            logging.error(f"获取生活指数失败: {response}")
            return {}

        # 处理返回结果
        suggestion_data = response["data"][0].get("suggestion", {})
        if not suggestion_data:
            logging.error("返回的生活指数数据为空")
            return {}

        return {
            k: LifeSuggestion(**v)
            for k, v in suggestion_data.items()
            if isinstance(v, dict) and "brief" in v and "details" in v
        }

    async def get_weather_alarm(
        self, location: str, distinct: bool = True
    ) -> List[WeatherAlarm]:
        """获取天气预警"""
        # 构造请求
        path = self.path_weather_alarm
        data = {
            "location": json.dumps({"area": location}),
            "device_id": self.device_id,
            "lang": self.lang,
            "distinct": distinct,
        }
        payload = make_payload(
            path=path,
            method="GET",
            app_id=self.app_id,
            app_secret=self.app_secret,
            data=data,
            content_type="json",
        )

        # 发送请求
        url = self.endpoint + path
        response = session.get(
            url, params=payload, headers=self.headers, timeout=self.timeout
        ).json()
        if response.get("result_code") != "success" or "data" not in response:
            logging.error(f"获取天气预警失败: {response}")
            return []

        # 处理返回结果
        alarm_data = response["data"][0].get("alarms", [])
        if not alarm_data:
            logging.info("当前没有天气预警信息")
            return []

        # 检查天气预警数据是否满足模型要求的字段
        valid_alarms = []
        for alarm in alarm_data:
            if not all(
                field in alarm
                for field in ["type", "level", "title", "text", "pub_time"]
            ):
                logging.warning(f"跳过不完整的天气预警数据: {alarm}")
                continue
            valid_alarms.append(WeatherAlarm(**alarm))

        return valid_alarms

    async def get_typhoon(self) -> List[Typhoon]:
        """获取台风信息"""

        # 构造请求
        path = self.path_typhoon
        data = {"device_id": self.device_id}
        payload = make_payload(
            path=path,
            method="GET",
            app_id=self.app_id,
            app_secret=self.app_secret,
            data=data,
            content_type="json",
        )

        # 发送请求
        url = self.endpoint + path
        response = session.get(
            url, params=payload, headers=self.headers, timeout=self.timeout
        ).json()
        if response.get("result_code") != "success" or "data" not in response:
            logging.error(f"获取台风信息失败: {response}")
            return []

        # 处理返回结果
        typhoon_data = response.get("data", [])
        if not typhoon_data:
            logging.info("当前没有台风信息")
            return []

        # 检查台风数据是否满足模型要求的字段
        valid_typhoons = []
        required_fields = [
            "id",
            "name",
            "en_name",
            "level",
            "pressure",
            "wind_speed",
            "move_speed",
            "move_direction",
            "lat",
            "lon",
        ]

        for typhoon in typhoon_data:
            if not all(field in typhoon for field in required_fields):
                logging.warning(f"跳过不完整的台风数据: {typhoon}")
                continue
            valid_typhoons.append(Typhoon(**typhoon))

        return valid_typhoons

    async def get_precipitation(self, location: str) -> Optional[Precipitation]:
        """获取降水预报"""
        # 构造请求
        path = self.path_precipitation
        data = {
            "location": json.dumps({"area": location}),
            "device_id": self.device_id,
            "lang": self.lang,
        }
        payload = make_payload(
            path=path,
            method="GET",
            app_id=self.app_id,
            app_secret=self.app_secret,
            data=data,
            content_type="json",
        )

        # 发送请求
        url = self.endpoint + path
        response = session.get(
            url, params=payload, headers=self.headers, timeout=self.timeout
        ).json()
        if response.get("result_code") != "success" or "data" not in response:
            logging.error(f"获取降水预报失败: {response}")
            # 即使接口失败，也返回空的降水预报对象
            return Precipitation()

        # 处理返回结果
        precip_data = response.get("data", {})
        if not precip_data:
            logging.error("返回的降水预报数据为空")
            return Precipitation()

        return Precipitation(**precip_data)


@mcp.tool()
async def get_weather_now(location: str) -> dict:
    """
    获取指定位置的实时天气

    参数:
    - location: 位置名称，如城市名称（例如：北京、上海）

    返回:
    - 实时天气信息
    """
    weather_service = WeatherService()  # 创建服务实例
    weather = await weather_service.get_weather_now(location)
    if not weather:
        return {"error": "无法获取天气信息"}

    # 将结果转换为以description为key的字典
    fields_info = {
        field.description: getattr(weather, field_name)
        for field_name, field in weather.__fields__.items()
    }
    return fields_info


@mcp.tool()
async def get_weather_forecast_hourly(
    location: str, start: int = 1, hours: int = 24
) -> List[dict]:
    """
    获取指定位置的小时级天气预报

    参数:
    - location: 位置名称，如城市名称（例如：北京、上海）
    - start: 开始小时(1-23)，默认为1
    - hours: 预报小时数(1-24)，默认为24

    返回:
    - 小时级天气预报列表
    """
    weather_service = WeatherService()  # 创建服务实例
    forecasts = await weather_service.get_weather_forecast_hourly(
        location, start, hours
    )

    # 将结果转换为以description为key的字典列表
    result = []
    for forecast in forecasts:
        fields_info = {
            field.description: getattr(forecast, field_name)
            for field_name, field in forecast.__fields__.items()
        }
        result.append(fields_info)
    return result


@mcp.tool()
async def get_weather_forecast_daily(
    location: str, start: int = 0, days: int = 7
) -> List[dict]:
    """
    获取指定位置的天级天气预报

    参数:
    - location: 位置名称，如城市名称（例如：北京、上海）
    - start: 开始日期(0-7)，默认为0(今天)
    - days: 预报天数(1-7)，默认为7

    返回:
    - 天级天气预报列表
    """
    weather_service = WeatherService()  # 创建服务实例
    forecasts = await weather_service.get_weather_forecast_daily(location, start, days)

    # 将结果转换为以description为key的字典列表
    result = []
    for forecast in forecasts:
        fields_info = {
            field.description: getattr(forecast, field_name)
            for field_name, field in forecast.__fields__.items()
        }
        result.append(fields_info)
    return result


@mcp.tool()
async def get_air_quality(location: str) -> dict:
    """
    获取指定位置的空气质量

    参数:
    - location: 位置名称，如城市名称（例如：北京、上海）

    返回:
    - 空气质量信息
    """
    weather_service = WeatherService()  # 创建服务实例
    air_quality = await weather_service.get_air_quality(location)
    if not air_quality:
        return {"error": "无法获取空气质量信息"}

    # 将结果转换为以description为key的字典
    fields_info = {
        field.description: getattr(air_quality, field_name)
        for field_name, field in air_quality.__fields__.items()
    }
    return fields_info


@mcp.tool()
async def get_life_suggestion(location: str) -> Dict[str, dict]:
    """
    获取指定位置的生活指数

    参数:
    - location: 位置名称，如城市名称（例如：北京、上海）

    返回:
    - 生活指数信息
    """
    weather_service = WeatherService()  # 创建服务实例
    suggestions = await weather_service.get_life_suggestion(location)
    if not suggestions:
        return {"error": "无法获取生活指数信息"}

    # 将结果转换为以description为key的字典
    result = {}
    for key, suggestion in suggestions.items():
        fields_info = {
            field.description: getattr(suggestion, field_name)
            for field_name, field in suggestion.__fields__.items()
        }
        result[key] = fields_info
    return result


@mcp.tool()
async def get_weather_alarm(location: str, distinct: bool = True) -> List[dict]:
    """
    获取指定位置的天气预警

    参数:
    - location: 位置名称，如城市名称（例如：北京、上海）
    - distinct: 是否去重同标题预警，默认为True

    返回:
    - 天气预警列表
    """
    weather_service = WeatherService()  # 创建服务实例
    alarms = await weather_service.get_weather_alarm(location, distinct)

    # 将结果转换为以description为key的字典列表
    result = []
    for alarm in alarms:
        fields_info = {
            field.description: getattr(alarm, field_name)
            for field_name, field in alarm.__fields__.items()
        }
        result.append(fields_info)
    return result


@mcp.tool()
async def get_typhoon() -> List[dict]:
    """
    获取台风信息

    返回:
    - 台风信息列表
    """
    weather_service = WeatherService()  # 创建服务实例
    typhoons = await weather_service.get_typhoon()

    # 将结果转换为以description为key的字典列表
    result = []
    for typhoon in typhoons:
        fields_info = {
            field.description: getattr(typhoon, field_name)
            for field_name, field in typhoon.__fields__.items()
        }
        result.append(fields_info)
    return result


@mcp.tool()
async def get_precipitation(location: str) -> dict:
    """
    获取指定位置的降水预报

    参数:
    - location: 位置名称，如城市名称（例如：北京、上海）

    返回:
    - 降水预报信息
    """
    weather_service = WeatherService()  # 创建服务实例
    precipitation = await weather_service.get_precipitation(location)
    if not precipitation:
        return {"error": "无法获取降水预报信息"}

    # 将结果转换为以description为key的字典
    fields_info = {
        field.description: getattr(precipitation, field_name)
        for field_name, field in precipitation.__fields__.items()
    }
    return fields_info


def main():
    """启动MCP服务器"""
    mcp.run(transport=os.getenv("MCP_SERVER_TRANSPORT", "streamable-http"))


if __name__ == "__main__":
    main()
