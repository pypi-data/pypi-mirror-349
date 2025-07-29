from mcp.server.fastmcp import FastMCP
import requests


def setup_mcp(jwt_token: str) -> FastMCP:
    mcp = FastMCP("weather")

    @mcp.tool()
    def weather_now(location: str = '101010100') -> str:
        """
        实时天气信息

        :param location: 位置代码，例如 '101010100' 表示北京
        :return: 天气信息
        :rtype: str

        updateTime 当前API的最近更新时间
        fxLink 当前数据的响应式页面，便于嵌入网站或应用
        obsTime 数据观测时间
        temp 温度，默认单位：摄氏度
        feelsLike 体感温度，默认单位：摄氏度
        text 天气状况的文字描述，包括阴晴雨雪等天气状态的描述
        wind360 风向360角度
        windDir 风向
        windScale 风力等级
        windSpeed 风速，公里/小时
        humidity 相对湿度，百分比数值
        precip 过去1小时降水量，默认单位：毫米
        pressure 大气压强，默认单位：百帕
        vis 能见度，默认单位：公里
        cloud 云量，百分比数值。可能为空
        dew 露点温度。可能为空
        """
        headers = {"Authorization": f"Bearer {jwt_token}",
                   "Accept-Encoding": "gzip"}
        response = requests.get(
            "https://nf78kxjx8h.re.qweatherapi.com/v7/weather/now",
            params={"location": location},
            headers=headers
        )
        return response.json() if response.status_code == 200 else response.text

    @mcp.tool()
    def weather_day(location: str = '101010100', day: str = '3d') -> str:
        """
        未来几天的天气

        :param location: 位置代码，例如 '101010100' 表示北京
        :param day: 天数，例如 '3d' 表示未来三天, options: '3d', '7d', '10d', '15d', '30d'
        :return: 天气信息
        :rtype: str

        updateTime 当前API的最近更新时间
        fxLink 当前数据的响应式页面，便于嵌入网站或应用
        fxDate 预报日期
        sunrise 日出时间，在高纬度地区可能为空
        sunset 日落时间，在高纬度地区可能为空
        moonrise 当天月升时间，可能为空
        moonset 当天月落时间，可能为空
        moonPhase 月相名称
        tempMax 预报当天最高温度
        tempMin 预报当天最低温度
        textDay 预报白天天气状况文字描述，包括阴晴雨雪等天气状态的描述
        textNight 预报晚间天气状况文字描述，包括阴晴雨雪等天气状态的描述
        wind360Day 预报白天风向360角度
        windDirDay 预报白天风向
        windScaleDay 预报白天风力等级
        windSpeedDay 预报白天风速，公里/小时
        wind360Night 预报夜间风向360角度
        windDirNight 预报夜间当天风向
        windScaleNight 预报夜间风力等级
        windSpeedNight 预报夜间风速，公里/小时
        precip 预报当天总降水量，默认单位：毫米
        uvIndex 紫外线强度指数
        humidity 相对湿度，百分比数值
        pressure 大气压强，默认单位：百帕
        vis 能见度，默认单位：公里
        cloud 云量，百分比数值。可能为空
        """
        response = requests.get(
            f"https://nf78kxjx8h.re.qweatherapi.com/v7/weather/{day}",
            params={"location": location},
            headers={"Authorization": f"Bearer {jwt_token}",
                     "Accept-Encoding": "gzip"}
        )
        return response.json() if response.status_code == 200 else response.text

    return mcp
