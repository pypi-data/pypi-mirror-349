#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'wrc'

import pytest


class LanguageUtil(object):
    language_key = {
        "US": "en",  # 美国
        "SA": "ar",  # 沙特
        "IL": "he",  # 以色列
        "MA": "fr",  # 摩洛哥
        "ES": "es",  # 西班牙
        "QA": "ar",  # 卡塔尔
        "AE": "ar",  # 阿联酋
        "KW": "ar",  # 科威特
        "OM": "ar",  # 阿曼
        "BH": "ar",  # 巴林
        "FR": "fr",  # 法国
        "AO": "pt-pt",  # 安哥拉(国际站葡语)
        "EG": "en",  # 埃及(国际站英语)
        "UK": "en",  # 英国
        "LI": "de",  # 列支敦士登(国际站英语)
        "BE": "nl",  # 比利时(欧洲站荷兰语)
        "LU": "de",  # 卢森堡(德国站德语)
        "AT": "de",  # 奥地利(德国站德语)
        "JP": "ja",  # 日本
        "MY": "en",  # 马来西亚
        "CH": "de",  # 瑞士
        "GR": "el-gr",  # 希腊
        "CZ": "en",  # 捷克共和国
        "RO": "ro",  # 罗马尼亚(罗马尼亚语言)
        "LB": "en",  # 黎巴嫩(国际站英语)
        "TW": "zh-tw",  # 中国台湾
        "HK": "zh-hk",  # 中国香港
        "PL": "pl",  # 波兰
        "RU": "ru",  # 俄罗斯
        "NZ": "en",  # 新西兰
        "ZA": "en",  # 南非
        "SG": "en",  # 新加坡
        "BR": "pt-br",  # 巴西
        "CL": "es",  # 智利
        "VN": "en",  # 越南
        "TH": "th",  # 泰国
        "BG": "en",  # 保加利亚
        "SE": "sv",  # 瑞典
        "CA": "en",  # 加拿大
        "AU": "en",  # 澳大利亚
        "NL": "nl",  # 荷兰
        "IT": "it",  # 意大利
        "DE": "de",  # 德国
        "MX": "es-mx",  # 墨西哥
        "DK": "en",  # 丹麦
        "EE": "en",  # 爱沙尼亚
        "FI": "en",  # 芬兰
        "HU": "en",  # 匈牙利
        "LV": "en",  # 拉脱维亚
        "LT": "en",  # 立陶宛
        "PT": "pt-pt",  # 葡萄牙
        "SK": "en",  # 斯洛伐克
        "SI": "en",  # 斯洛文尼亚
        "IE": "en",  # 爱尔兰
        "KR": "ko",  # 韩国(亚洲站韩语)
        "PH": "en",  # 菲律宾
        "NO": "en",  # 挪威
        "ROE": "en",  # 挪威
        "EC": "es",  # 厄瓜多尔(国际站西语)
        "JO": "en",  # 约旦
        "CO": "es-mx",  # 哥伦比亚
        "MA_AR": "ar",  # 摩洛哥(阿语）
        "LU_EN": "en",  # 卢森堡(欧洲站英语)
        "TH_EN": "en",  # 泰国(英语)
        "IL_EN": "en",  # 以色列(英语)
        "AT_FR": "fr",  # 奥地利(欧洲站法语)
        "BH_EN": "en",  # 巴林(英语)
        "KW_EN": "en",  # 科威特(英语)
        "AE_EN": "en",  # 阿联酋(英语)
        "QA_EN": "en",  # 卡塔尔(英语)
        "OM_EN": "en",  # 阿曼(英语)
        "SA_EN": "en",  # 沙特(英语)
        "KR_EN": "en",  # 韩国(英语)
        "CA_FR": "fr",  # 加拿大(法语)
        "SE_EN": "en",  # 瑞典(英语)
        "JP_EN": "en",  # 日本（英语)
        "FR_EN": "en",  # 法国（英语） # https://wiki.dotfashion.cn/pages/viewpage.action?pageId=1385048900
        "DE_EN": "en",  # 德国（英语）
        "IT_EN": "en",  # 意大利（英语）
        "ES_EN": "en",  # 西班牙（英语）
        "CA_EN": "en",  # 加拿大（英语）
        "MX_EN": "en",  # 墨西哥（英语）
        "BE_EN": "en",  # 比利时（英语）
        "BE_FR": "fr",  # 比利时（法语）
        "BE_RO": "ro",  # 比利时（罗马语）
        "BE_NL": "nl",  # 比利时（荷兰语）
        "BE_EL": "el-gr",  # 比利时（希腊语）
        "BE_CS": "cs",  # 比利时（捷克语）
        "GR_CS": "cs",  # 希腊（捷克语）
        "GR_EN": "en",  # 希腊（英语）
        "GR_FR": "fr",  # 希腊（法语）
        "GR_NL": "nl",  # 希腊（荷兰语）
        "US_ES": "es",  # 美国(西语)
        "CH_FR": "fr",  # 法语
        "ID": "en",  # 印度尼西亚
        "TR": "en",  # 土尔其
        "PE": "es-mx",  # 秘鲁
        "AR": "es-mx",  # 阿根廷
    }

    def language_info(self, site):
        site_type = site
        if LanguageUtil.language_key.get(site_type):
            return LanguageUtil.language_key[site_type]
        else:
            pytest.assume(False), f"该国家不支持{site_type}"

    country_key = {
        "US": "US",  # 美国
        "SA": "SA",  # 沙特
        "IL": "IL",  # 以色列
        "MA": "MA",  # 摩洛哥
        "ES": "ES",  # 西班牙
        "QA": "QA",  # 卡塔尔
        "AE": "AE",  # 阿联酋
        "KW": "KW",  # 科威特
        "OM": "OM",  # 阿曼
        "BH": "BH",  # 巴林
        "FR": "FR",  # 法国
        "AO": "AO",  # 安哥拉(国际站葡语)
        "EG": "EG",  # 埃及(国际站英语)
        "UK": "UK",  # 英国
        "LI": "LI",  # 列支敦士登(国际站英语)
        "BE": "BE",  # 比利时(欧洲站荷兰语)
        "LU": "LU",  # 卢森堡(德国站德语)
        "AT": "AT",  # 奥地利(德国站德语)
        "JP": "JP",  # 日本
        "MY": "MY",  # 马来西亚
        "CH": "CH",  # 瑞士
        "GR": "GR",  # 希腊
        "CZ": "CZ",  # 捷克共和国
        "RO": "RO",  # 罗马尼亚
        "LB": "LB",  # 黎巴嫩(国际站英语)
        "TW": "TW",  # 中国台湾
        "HK": "HK",  # 中国香港
        "PL": "PL",  # 波兰
        "RU": "RU",  # 俄罗斯
        "NZ": "NZ",  # 新西兰
        "ZA": "ZA",  # 南非
        "SG": "SG",  # 新加坡
        "BR": "BR",  # 巴西
        "CL": "CL",  # 智利
        "VN": "VN",  # 越南
        "TH": "TH",  # 泰国
        "BG": "BG",  # 保加利亚
        "SE": "SE",  # 瑞典
        "CA": "CA",  # 加拿大
        "AU": "AU",  # 澳大利亚
        "NL": "NL",  # 荷兰
        "IT": "IT",  # 意大利
        "DE": "DE",  # 德国
        "MX": "MX",  # 墨西哥
        "DK": "DK",  # 丹麦
        "EE": "EE",  # 爱沙尼亚
        "FI": "FI",  # 芬兰
        "HU": "HU",  # 匈牙利
        "LV": "LV",  # 拉脱维亚
        "LT": "LT",  # 立陶宛
        "PT": "PT",  # 葡萄牙
        "SK": "en",  # 斯洛伐克
        "SI": "SI",  # 斯洛文尼亚
        "IE": "IE",  # 爱尔兰
        "KR": "KR",  # 韩国(亚洲站韩语)
        "PH": "PH",  # 菲律宾
        "NO": "NO",  # 挪威
        "EC": "EC",  # 厄瓜多尔(国际站西语)
        "JO": "JO",  # 约旦
        "CO": "CO",  # 哥伦比亚
        "ID": "ID",  # 印度尼西亚
        "TR": "TR",  # 土尔其
        "AR": "AR",  # 阿根廷
        "MA_AR": "MA",  # 摩洛哥(阿语）
        "LU_EN": "LU",  # 卢森堡(欧洲站英语)
        "TH_EN": "TH",  # 泰国(英语)
        "IL_EN": "IL",  # 以色列(英语)
        "AT_FR": "AT",  # 奥地利(欧洲站法语)
        "BH_EN": "BH",  # 巴林(英语)
        "KW_EN": "KW",  # 科威特(英语)
        "AE_EN": "AE",  # 阿联酋(英语)
        "QA_EN": "QA",  # 卡塔尔(英语)
        "OM_EN": "OM",  # 阿曼(英语)
        "SA_EN": "SA",  # 沙特(英语)
        "CA_FR": "CA",  # 加拿大(法语)
        "SE_EN": "SE",  # 瑞典(英语)
        "JP_EN": "JP",  # 日本（英语)
        "US_ES": "US",  # 美国(西语)
        "BE_FR": "BE",  # 比利时(法语)
        "CH_FR": "CH",  # 瑞士(法语)
    }

    def country_info(self, site):
        site_type = site
        if LanguageUtil.country_key.get(site_type):
            return LanguageUtil.country_key[site_type]
        # else:
        #     pytest.assume(False), f"该国家不支持{site_type}"
