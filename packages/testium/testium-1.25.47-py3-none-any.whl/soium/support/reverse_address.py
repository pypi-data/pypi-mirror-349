# import math
# import random
# import re
# import time
# from contextlib import suppress
#
# import requests
# import sre_yield
# from selenium import webdriver
# from selenium.webdriver import DesiredCapabilities
#

# url = "https://pc-test22.wrc.com"
#
#
# def get_cookie():
#     """
#     登录获取Cookie
#     """
#     login_page_url = f"{url}/user/auth/login"
#     options = webdriver.ChromeOptions()
#     # options.headless = True
#     prefs = {"profile.managed_default_content_settings.images": 2}
#     options.add_experimental_option("prefs", prefs)
#     with webdriver.Remote(command_executor="http://10.102.32.12:4444/wd/hub",
#                           desired_capabilities=DesiredCapabilities.CHROME,
#                           options=options) as driver:
#         driver.get(login_page_url)
#         driver.find_element_by_css_selector('[name="email"]').send_keys('maoba_us@test.com')
#         driver.find_element_by_css_selector('[name="password"').send_keys('123456qwe')
#         time.sleep(1)
#         cookie = driver.execute_script("return document.cookie")
#         driver.find_element_by_css_selector('.sign-in-btn-wrapper > button').click()
#         while 1:
#             if (current_cookie := driver.execute_script("return document.cookie")) != cookie:
#                 return current_cookie
#             time.sleep(1)
#
#
# def generate_regex(regex: str) -> str:
#     """
#     生成数据
#     """
#     items = sre_yield.AllStrings(regex)
#     while 1:
#         with suppress(ValueError):
#             item = items[random.randrange(0, items.length)]
#             isinstance(item, str)
#             # 替换不可见的字符
#             item = re.sub(re.compile('[\u0000-\u001F\u007F-\u00A0]'), 'a', item)
#             return item
#
#
# def generate_reverse_regex(regex: str) -> list:
#     """
#     生成反正则及数据
#     return: [{reg, value}, ]
#     """
#     regex_list = []
#     pattern_list = []
#     pattern = regex.replace('\\\\', '\\')
#     pattern_list += [_ for _ in re.split(re.compile(r'(\(\^.+?\$\))'), pattern) if _ not in ['|', '']]
#     for pattern in pattern_list:
#         for index, regular in {
#             '1': r'\[(.+?)\]',
#             '2': r'\{([\d]+)\}',
#             '3': r'\{([\d]+),\}',
#             '4': r'\{([\d]+),([\d]+)\}',
#             '5': r'^(\d+?)\D',
#             '6': r'\(([\d\|]+)\)',
#             '7': r'(\[[\\s\\S]+?\]\+)',
#         }.items():
#             results = re.finditer(re.compile(regular), pattern)
#             if index == '1':
#                 """
#                 例子: xx[0-9]xx  需要提取的内容: 0-9
#                 结果: xx[^0-9]xx
#                 """
#                 for result in results:
#                     """
#                     正则匹配结果: [0-9]
#                     start: "[" 的位置
#                     end: "]" 的位置
#                     match: 0-9
#                     """
#                     start, end = result.span()
#                     match = result.groups()[0]
#                     if match not in ['\\s\\S', '\\S\\s']:
#                         # 排除match不限制的正则
#                         # 结果 = 原正则[:start] + [^match] + 原正则[end:]
#                         regex_list.append(f'{pattern[:start]}[^{match}]{pattern[end:]}')
#             if index == '2':
#                 """
#                 例子: xxx{3}xxx 需要提取的内容: 3
#                 结果: [xxx{2}xxx, xxx{4}xxx]
#                 """
#                 for result in results:
#                     """
#                     正则匹配结果:{3}
#                     start: "{" 的位置
#                     end: "}" 的位置
#                     match: 3
#                     replacements: 取match±1, 即2, 4
#                     """
#                     start, end = result.span()
#                     match = int(result.groups()[0])
#                     replacements = [match - 1, match + 1]
#                     """
#                     循环replacements,即需要替换的个数, 以下以value表示
#                     结果 = 原正则[:start] + {value} + 原正则[end:]
#                     """
#                     [regex_list.append(f'{pattern[:start]}{{{replacement}}}{pattern[end:]}') for replacement in
#                      replacements if replacement > 0]
#             if index == '3':
#                 """
#                 例子: xxx{3,}xxx 需要提取的内容: 3
#                 结果: xxx{2}xxx
#                 """
#                 for result in results:
#                     """
#                     正则匹配结果:{3,}
#                     start: "{" 的位置
#                     end: "}" 的位置
#                     match: 3
#                     replacements: 取match-1, 即2
#                     """
#                     start, end = result.span()
#                     replacement = int(result.groups()[0]) - 1
#                     # 结果 = 原正则[:start] + {replacements} + 原正则[end:]
#                     if replacement <= 0:
#                         continue
#                     regex_list.append(f'{pattern[:start]}{{{replacement}}}{pattern[end:]}')
#             if index == '4':
#                 """
#                 例子: xxx{3,5}xxx 需要提取的内容: 3,5
#                 结果: [xxx{2}xxx, xxx{6}xxx]
#                 """
#                 for result in results:
#                     """
#                     正则匹配结果:{3,5}
#                     start: "{" 的位置
#                     end: "}" 的位置
#                     minimum(最小值): 3
#                     maximum(最大值): 5
#                     replacements: 取最小值-1, 取最大值+1
#                     """
#                     start, end = result.span()
#                     minimum, maximum = result.groups()
#                     replacements = [int(minimum) - 1, int(maximum) + 1]
#                     """
#                     循环replacements,即需要替换的个数, 以下以value表示
#                     结果 = 原正则[:start] + {value} + 原正则[end:]
#                     """
#                     [regex_list.append(f'{pattern[:start]}{{{replacement}}}{pattern[end:]}') for replacement in
#                      replacements if replacement > 0]
#             if index in ['5', '6']:
#                 """
#                 例子: 场景5: 09xxx, 场景6: (30|31|33)xxx  例如电话的校验
#                 结果: 非09开头的两位数xxx, 非(30|31|33)开头的两位数xxx  匹配的长度按照匹配出来的数字长度生成,例如09生成2位,911生成3位
#                 """
#                 for result in results:
#                     """
#                     正则匹配结果: 场景5: 09    场景6: (30|31|33)
#                     start: 场景5的起点为"0" 场景6的起点为"("
#                     end: 场景5的结束为"9" 场景6的结束为")"
#                     zone_descriptions: 以"|"分割多个区号, 返回[30, 31, 33]
#                     items: 过滤所有区号的长度, 过滤后结果为[2,]
#                     """
#                     start, end = result.span()
#                     match = result.groups()[0]
#                     zone_descriptions = match.split('|')
#                     items = set([len(num) for num in match.split('|')])
#                     for item in items:
#                         while True:
#                             """
#                             随机生成刚刚过滤后的区号长度的数字, 与正确的区号匹配是否一样, 如果一样重新生成
#                             """
#                             num = ''.join(map(str, random.choices(list(range(10)), k=item)))
#                             if num not in zone_descriptions:
#                                 break
#                         if index == '5':
#                             regex_list.append(f'{pattern[:start]}{num}{pattern[end - 1:]}')
#                         else:
#                             regex_list.append(f'{pattern[:start]}({num}){pattern[end:]}')
#             if index == '7':
#                 """
#                 场景7不做限制, 无反正则跳过
#                 """
#                 break
#     return [{"reg": regex, "value": generate_regex(regex)} for regex in regex_list]
#
#
# def get_all_country(lang) -> list:
#     """
#     获取全部国家
#     """
#     return requests.get("https://www.wrc.com/getWholeCountryList",
#                         params={
#                             '_lang': lang
#                         }).json()
#
#
# def get_country_id(name, lang):
#     """
#     获取国家ID
#     """
#     all_country = get_all_country(lang)
#     country_id = next(country['id'] for country in all_country if name == country['country'])
#     return country_id
#
#
# def get_address_rules(country_id, distribution_type, lang) -> dict:
#     """
#     获取地址规则
#     """
#     cookie = get_cookie()
#     # cookie = "_ga=GA1.3.795224321.1624242389; _gid=GA1.3.2050626483.1624242389; scarab.visitor=%2277387BBA0155217F%22; cookieId=22D80917_3503_3E44_6DD6_141851591AE1; cdn_key=mlang%3Den; G_ENABLED_IDPS=google; pwa_user_email=maoba_us%40test.com; pwa_user_memberid=1000003098; memberId=1000003098; origin_type=; originId=; sessionID_wrc_m_pwa=s%3AdODFPZOvXDlQpPdicLz0L_7mnOGAF1RP.A3aHFwXMNX9N3pbcBK8uvQ0hg197lqLHhdjAuAymyt8; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221000003098%22%2C%22first_id%22%3A%2217a2c63fca02cd-05db046cdef08b-4373266-2073600-17a2c63fca138c%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%2217a2c63fca02cd-05db046cdef08b-4373266-2073600-17a2c63fca138c%22%7D; user_levelOpen=; OptanonAlertBoxClosed=2021-06-21T07:56:24.992Z; OptanonConsent=isIABGlobal=false&datestamp=Mon+Jun+21+2021+15%3A56%3A25+GMT%2B0800+(%E4%B8%AD%E5%9C%8B%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=6.13.0&hosts=&consentId=a4df03e355e09f0fe49983cec066edbf&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1&AwaitingReconsent=false&geolocation=SG%3B; bi_session_id=bi_1624329442839_10432; pwa_default_currency_expire_ar=1; pwa_currency_ar=SAR; _csrf=XJ2pvwKl0zZ7ZMfmTbDrKo8w; language=ru; pwa_default_currency_expire_ru=1; pwa_currency_ru=RUB; pwa_default_currency=RUB"
#     headers = {
#         "x-requested-with": "XMLHttpRequest",
#         "cookie": cookie
#     }
#     field_list = requests.post(f"{url}/user/addressbook/getAddressCheckRule", data={
#         "distribution_type": distribution_type,
#         "country_id": country_id
#     }, params={
#         '_lang': lang
#     }, headers=headers).json()['info']['result']['field_rule_check']
#     return {field['field_name']: {"is_require": field['is_require'], "regex_list": field['regex_list'],
#                                   "require_copywrite": field['require_copywrite'],
#                                   "reverse_regex_list": field['reverse_regex_list']} for field in
#             field_list if field['field_name'] != "country"}
#
#
# def get_field(name: str, data: dict, union_name: str = None) -> str:
#     """
#     获取正向的字段值
#     union_name: 联合校验字段名
#     """
#     field = data.get(union_name) if union_name else data.get(name)
#     while 1:
#         result = ''
#         for regex in field['regex_list']:
#             replace_string = generate_regex(regex['reg'])
#             result = f"{result[:-len(replace_string)]}{replace_string}"
#         for reverse_regex in field['reverse_regex_list']:
#             result = re.sub(re.compile(reverse_regex['reg']), '', result)
#         if all([re.search(re.compile(regex['reg']), result) for regex in field['regex_list']]):
#             if not union_name:
#                 return result
#             else:
#                 field = data.get(name)
#                 for regex in field['regex_list']:
#                     if not re.search(re.compile(regex['reg']), result):
#                         replace_string = generate_regex(regex['reg'])
#                         result = f"{result[:-len(replace_string)]}{replace_string}"
#                 if all([re.search(re.compile(regex['reg']), result) for regex in
#                         (field['regex_list'] + data.get(union_name)['regex_list'])]):
#                     return result
#
#
# def get_reverse_field(name: str, data: dict) -> list:
#     """
#     获取反向的字段值
#     """
#     field = data.get(name)
#     union_field_name = {"last_name": "first_name", "address2": "address1"}.get(name)
#     reverse_regex_list = []
#     filter_regex_list = []
#     # 判断是否必填项
#     if field['is_require'] == "1":
#         reverse_regex_list.append({
#             "group": None,
#             "value": '',
#             "reg": None,
#             "copywrite": field['require_copywrite'],
#             "is_union_check": None
#         })
#     for index, regex in enumerate(field['regex_list']):
#         if index:
#             # 判断是否联合校验
#             if regex['is_union_check']:
#                 # 走联合校验
#                 while 1:
#                     correct_result = get_field(union_field_name, data)
#                     wrong_result = re.sub(re.compile(regex['reg']), '', correct_result)
#                     for _ in ([_['reg'] for _ in data[union_field_name]['regex_list']] + filter_regex_list):
#                         if not re.search(re.compile(_), wrong_result):
#                             break
#                     else:
#                         reverse_regex_list.append({
#                             "group": {
#                                 union_field_name: wrong_result[:math.ceil(len(wrong_result) / 2)],
#                                 name: wrong_result[math.ceil(len(wrong_result) / 2):]
#                             },
#                             "value": "",
#                             "reg": f"剔除正则: {regex['reg']}",
#                             "copywrite": regex['copywrite'],
#                             "is_union_check": True
#                         })
#                         break
#             else:
#                 # 不走联合校验
#                 while 1:
#                     correct_result = get_field(name, data)
#                     wrong_result = re.sub(re.compile(regex['reg']), '', correct_result)
#                     for filter_regex in filter_regex_list:
#                         if not re.search(re.compile(filter_regex), wrong_result):
#                             break
#                     else:
#                         reverse_regex_list.append({
#                             "group": None,
#                             "value": wrong_result,
#                             "reg": f"剔除正则: {regex['reg']}",
#                             "copywrite": regex['copywrite'],
#                             "is_union_check": False
#                         })
#                         break
#         else:
#             # 判断是否联合校验
#             if regex['is_union_check']:
#                 # 走联合校验
#                 while 1:
#                     for reverse_regex in generate_reverse_regex(regex['reg']):
#                         status = False
#                         for _ in data[union_field_name]['regex_list']:
#                             if not re.search(re.compile(_['reg']), reverse_regex['reg']):
#                                 break
#                         else:
#                             reverse_regex_list.append({
#                                 "group": {
#                                     union_field_name: reverse_regex['value'][:math.ceil(
#                                         len(reverse_regex['value']) / 2)],
#                                     name: reverse_regex['value'][
#                                           math.ceil(len(reverse_regex['value']) / 2):]
#                                 },
#                                 "value": "",
#                                 "reg": reverse_regex['reg'],
#                                 "copywrite": regex['copywrite'],
#                                 "is_union_check": True
#                             })
#                             status = True
#                         if not status:
#                             break
#                     else:
#                         break
#             else:
#                 # 不走联合校验
#                 for reverse_regex in generate_reverse_regex(regex['reg']):
#                     reverse_regex_list.append({
#                         "group": None,
#                         "value": reverse_regex['value'],
#                         "reg": reverse_regex['reg'],
#                         "copywrite": regex['copywrite'],
#                         "is_union_check": False
#                     })
#         filter_regex_list.append(regex['reg'])
#
#     # 生成反正则的数据
#     for reverse_regex in field['reverse_regex_list']:
#         while 1:
#             status = False
#             if is_union_check := field['regex_list'][0]['is_union_check']:
#                 correct_result = get_field(name, data, union_field_name)
#             else:
#                 correct_result = get_field(name, data)
#             replace_string = generate_regex(reverse_regex['reg'])
#             wrong_result = f"{correct_result[:-len(replace_string)]}{replace_string}"
#             regex_list = field['regex_list']
#             if is_union_check:
#                 regex_list += data.get(union_field_name)['regex_list']
#             for _ in regex_list:
#                 if not re.search(re.compile(_['reg']), wrong_result):
#                     break
#             else:
#                 if is_union_check:
#                     reverse_regex_list.append({
#                         "group": {
#                             union_field_name: wrong_result[:math.ceil(len(wrong_result) / 2)],
#                             name: wrong_result[math.ceil(len(wrong_result) / 2):]
#                         },
#                         "value": "",
#                         "reg": f"插入反正则: {reverse_regex['reg']}",
#                         "copywrite": reverse_regex['copywrite'],
#                         "is_union_check": True
#                     })
#                 else:
#                     reverse_regex_list.append({
#                         "group": None,
#                         "value": wrong_result,
#                         "reg": f"插入反正则: {reverse_regex['reg']}",
#                         "copywrite": reverse_regex['copywrite'],
#                         "is_union_check": False
#                     })
#                 status = True
#             if status:
#                 break
#     return reverse_regex_list
#
#
# def get_reverse_address(country_name, distribution_type="1", lang='en') -> dict:
#     """
#     获取反向地址
#     {
#         "field_name":[
#             {
#                 "group":null,
#                 "value":"",
#                 "reg":null,
#                 "copywrite":"First Name should contain 2-35 characters",
#                 "is_union_check":null
#             }
#         ]
#     }
#     当is_union_check为True时,需要填写group里面的字段值,反之填写value的值,错误提示为copywrite
#     """
#     country_id = get_country_id(country_name, lang)
#     address_rules = get_address_rules(country_id, distribution_type, lang)
#     address = {}
#     for name in address_rules:
#         address.update(
#             {name: get_reverse_field(name, address_rules)}
#         )
#     return address
