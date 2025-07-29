from mcp.server.fastmcp import FastMCP
import requests


def setup_mcp(token: str, host: str) -> FastMCP:
    mcp = FastMCP("weather")

    @mcp.tool()
    def get_iso3166() -> str:
        """
        获取ISO 3166国家代码列表

        :return: ISO 3166国家代码列表
        :rtype: str

    """
        return """
        Afghanistan	AF
        Aland Islands	AX
        Albania	AL
        Algeria	DZ
        American Samoa	AS
        Andorra	AD
        Angola	AO
        Anguilla	AI
        Antarctica	AQ
        Antigua and Barbuda	AG
        Argentina	AR
        Armenia	AM
        Aruba	AW
        Australia	AU
        Austria	AT
        Azerbaijan	AZ
        Bahamas	BS
        Bahrain	BH
        Bangladesh	BD
        Barbados	BB
        Belarus	BY
        Belgium	BE
        Belize	BZ
        Benin	BJ
        Bermuda	BM
        Bhutan	BT
        Bolivia (Plurinational State of)	BO
        Bonaire, Sint Eustatius and Saba	BQ
        Bosnia and Herzegovina	BA
        Botswana	BW
        Bouvet Island	BV
        Brazil	BR
        British Indian Ocean Territory	IO
        Brunei Darussalam	BN
        Bulgaria	BG
        Burkina Faso	BF
        Burundi	BI
        Cabo Verde	CV
        Cambodia	KH
        Cameroon	CM
        Canada	CA
        Cayman Islands	KY
        Central African Republic	CF
        Chad	TD
        Chile	CL
        China	CN
        Christmas Island	CX
        Cocos (Keeling) Islands	CC
        Colombia	CO
        Comoros	KM
        Congo	CG
        Congo (Democratic Republic of the)	CD
        Cook Islands	CK
        Costa Rica	CR
        Côte d'Ivoire	CI
        Croatia	HR
        Cuba	CU
        Curaçao	CW
        Cyprus	CY
        Czechia	CZ
        Denmark	DK
        Djibouti	DJ
        Dominica	DM
        Dominican Republic	DO
        Ecuador	EC
        Egypt	EG
        El Salvador	SV
        Equatorial Guinea	GQ
        Eritrea	ER
        Estonia	EE
        Ethiopia	ET
        Falkland Islands (Malvinas)	FK
        Faroe Islands	FO
        Fiji	FJ
        Finland	FI
        France	FR
        French Guiana	GF
        French Polynesia	PF
        French Southern Territories	TF
        Gabon	GA
        Gambia	GM
        Georgia	GE
        Germany	DE
        Ghana	GH
        Gibraltar	GI
        Greece	GR
        Greenland	GL
        Grenada	GD
        Guadeloupe	GP
        Guam	GU
        Guatemala	GT
        Guernsey	GG
        Guinea	GN
        Guinea-Bissau	GW
        Guyana	GY
        Haiti	HT
        Heard Island and McDonald Islands	HM
        Holy See	VA
        Honduras	HN
        Hong Kong	HK
        Hungary	HU
        Iceland	IS
        India	IN
        Indonesia	ID
        Iran (Islamic Republic of)	IR
        Iraq	IQ
        Ireland	IE
        Isle of Man	IM
        Israel	IL
        Italy	IT
        Jamaica	JM
        Japan	JP
        Jersey	JE
        Jordan	JO
        Kazakhstan	KZ
        Kenya	KE
        Kiribati	KI
        Korea (Democratic People's Republic of)	KP
        Korea (Republic of)	KR
        Kuwait	KW
        Kyrgyzstan	KG
        Lao People's Democratic Republic	LA
        Latvia	LV
        Lebanon	LB
        Lesotho	LS
        Liberia	LR
        Libya	LY
        Liechtenstein	LI
        Lithuania	LT
        Luxembourg	LU
        Macao	MO
        Macedonia (the former Yugoslav Republic of)	MK
        Madagascar	MG
        Malawi	MW
        Malaysia	MY
        Maldives	MV
        Mali	ML
        Malta	MT
        Marshall Islands	MH
        Martinique	MQ
        Mauritania	MR
        Mauritius	MU
        Mayotte	YT
        Mexico	MX
        Micronesia (Federated States of)	FM
        Moldova (Republic of)	MD
        Monaco	MC
        Mongolia	MN
        Montenegro	ME
        Montserrat	MS
        Morocco	MA
        Mozambique	MZ
        Myanmar	MM
        Namibia	NA
        Nauru	NR
        Nepal	NP
        Netherlands	NL
        New Caledonia	NC
        New Zealand	NZ
        Nicaragua	NI
        Niger	NE
        Nigeria	NG
        Niue	NU
        Norfolk Island	NF
        Northern Mariana Islands	MP
        Norway	NO
        Oman	OM
        Pakistan	PK
        Palau	PW
        Palestine, State of	PS
        Panama	PA
        Papua New Guinea	PG
        Paraguay	PY
        Peru	PE
        Philippines	PH
        Pitcairn	PN
        Poland	PL
        Portugal	PT
        Puerto Rico	PR
        Qatar	QA
        Réunion	RE
        Romania	RO
        Russian Federation	RU
        Rwanda	RW
        Saint Barthélemy	BL
        Saint Helena, Ascension and Tristan da Cunha	SH
        Saint Kitts and Nevis	KN
        Saint Lucia	LC
        Saint Martin (French part)	MF
        Saint Pierre and Miquelon	PM
        Saint Vincent and the Grenadines	VC
        Samoa	WS
        San Marino	SM
        Sao Tome and Principe	ST
        Saudi Arabia	SA
        Senegal	SN
        Serbia	RS
        Seychelles	SC
        Sierra Leone	SL
        Singapore	SG
        Sint Maarten (Dutch part)	SX
        Slovakia	SK
        Slovenia	SI
        Solomon Islands	SB
        Somalia	SO
        South Africa	ZA
        South Georgia and the South Sandwich Islands	GS
        South Sudan	SS
        Spain	ES
        Sri Lanka	LK
        Sudan	SD
        Suriname	SR
        Svalbard and Jan Mayen	SJ
        Swaziland	SZ
        Sweden	SE
        Switzerland	CH
        Syrian Arab Republic	SY
        Taiwan, Province of China	TW
        Tajikistan	TJ
        Tanzania, United Republic of	TZ
        Thailand	TH
        Timor-Leste	TL
        Togo	TG
        Tokelau	TK
        Tonga	TO
        Trinidad and Tobago	TT
        Tunisia	TN
        Turkey	TR
        Turkmenistan	TM
        Turks and Caicos Islands	TC
        Tuvalu	TV
        Uganda	UG
        Ukraine	UA
        United Arab Emirates	AE
        United Kingdom of Great Britain and Northern Ireland	GB
        United States of America	US
        United States Minor Outlying Islands	UM
        Uruguay	UY
        Uzbekistan	UZ
        Vanuatu	VU
        Venezuela (Bolivarian Republic of)	VE
        Viet Nam	VN
        Virgin Islands (British)	VG
        Virgin Islands (U.S.)	VI
        Wallis and Futuna	WF
        Western Sahara	EH
        Yemen	YE
        Zambia	ZM
        Zimbabwe	ZW

        """

    @mcp.tool()
    def lookup_city(location: str, number: int = 1, range: str = 'cn') -> str:
        """
        没有城市位置代码或坐标时,要根据城市名称查询城市位置代码

        :param location: 需要查询地区的名称，支持文字、以英文逗号分隔的经度,纬度坐标（十进制，最多支持小数点后两位）、LocationID或Adcode（仅限中国城市）。例如 location=北京 或 location=116.41,39.92
        :param number: 返回结果数量，最大返回20条，默认返回1条
        :param range: 国家和地区名称需使用ISO 3166 所定义的国家代码，中国为 "cn"，默认为 "cn"
        :return: 天气信息
        :rtype: str

        name 地区/城市名称
        id 地区/城市ID
        lat 地区/城市纬度
        lon 地区/城市经度
        adm2 地区/城市的上级行政区划名称
        adm1 地区/城市所属一级行政区域
        country 地区/城市所属国家名称
        tz 地区/城市所在时区
        utcOffset 地区/城市目前与UTC时间偏移的小时数，参考详细说明
        isDst 地区/城市是否当前处于夏令时。1 表示当前处于夏令时，0 表示当前不是夏令时。
        type 地区/城市的属性
        rank 地区评分
        fxLink 该地区的天气预报网页链接，便于嵌入你的网站或应用
        """
        headers = {"Authorization": f"Bearer {token}",
                   "Accept-Encoding": "gzip"}
        response = requests.get(
            f"https://{host}/geo/v2/city/lookup",
            params={"location": location},
            headers=headers
        )
        return response.json() if response.status_code == 200 else response.text

    @mcp.tool()
    def weather_now(location: str = '101010100') -> str:
        """
        实时天气信息

        :param location: 位置，例如 '101010100','116.41,39.92' 表示北京
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
        headers = {"Authorization": f"Bearer {token}",
                   "Accept-Encoding": "gzip"}
        response = requests.get(
            f"https://{host}/v7/weather/now",
            params={"location": location},
            headers=headers
        )
        return response.json() if response.status_code == 200 else response.text

    @mcp.tool()
    def weather_furture(location: str = '101010100', furture: str = '3d') -> str:
        """
        未来一段时间的天气

        :param location: 位置，例如 '101010100','116.41,39.92' 表示北京
        :param furture: 未来时间. '3d' 未来三天,24h 未来24小时, options: '3d', '7d', '10d', '15d', '30d','24h','72h','168h'
        :return: 天气信息
        :rtype: str

        updateTime 当前API的最近更新时间
        fxLink 当前数据的响应式页面，便于嵌入网站或应用
        fxTime 预报时间
        fxDate 预报日期
        sunrise 日出时间，在高纬度地区可能为空
        sunset 日落时间，在高纬度地区可能为空
        moonrise 当天月升时间，可能为空
        moonset 当天月落时间，可能为空
        moonPhase 月相名称
        tempMax 预报当天最高温度
        tempMin 预报当天最低温度
        text 天气状况的文字描述，包括阴晴雨雪等天气状态的描述
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
        pop 逐小时预报降水概率，百分比数值，可能为空
        precip 当前小时累计降水量，默认单位：毫米
        """
        response = requests.get(
            f"https://{host}/v7/weather/{furture}",
            params={"location": location},
            headers={"Authorization": f"Bearer {token}",
                     "Accept-Encoding": "gzip"}
        )
        return response.json() if response.status_code == 200 else response.text

    return mcp
