#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import yaml
import argparse
import requests
import pyperclip

from datetime import datetime
from bs4 import BeautifulSoup

# ================== 命令行输入参数，默认值：0 ======================== #

parser = argparse.ArgumentParser(usage='参数说明')
parser.add_argument('-p', dest='page', type=int, help='共查询几页提交记录, page > 0 以page数为准, page <= 0 以YAML文件中的最近推送时间为准', default=0)
parser.add_argument('-d', dest='daily', type=int, help='日报参数，如传此参数则以YAML文件中日报的最近推送时间为准', default=0)
args = parser.parse_args()

# ================== 可修改数据 ======================== #

# 总共显示几页数据
SHOW_PAGE_TOTAL = args.page
# 是否是日报
IS_DAILY_PAPER = args.daily
# push记录包含此字符串则不打印 (DRD : Don't record)
NO_RECORD_TAG = "DRD"
# 时间格式，每次爬完Git记录时间，以免下次爬取重复内容
GMT_FORMAT = '%a, %d %b %Y %H:%M:%S CST'
# YAML文件路径，将敏感信息放入配置文件
YAML_FILE_PAHTH = "/Users/shenming/Desktop/Code/GitHub/otr-config/weekly.yaml"
# Git URL
BASE_URL = "http://10.3.40.239:3000"
LOGIN_URL = f"{BASE_URL}/user/login"

# ====================================================== #

# 全局变量

# 更多路径，用于点击更多按钮
more_path = ""
# 最近推送时间
last_push_time = ""

s = requests.Session()

# 获取push内容
def get_push_content(url, params, is_get=False):
    global more_path
    html = ""

    if is_get:
        response = s.get(url)
        html = response.text
    else:
        response = s.post(url, data=params)
        html = response.text

    # More按钮
    more_reg = r'<button class="ui fluid basic button center ajax-load-button" data-url="(.*?)">More</button>'
    more_reg = re.compile(more_reg, re.I)
    more_btns = re.findall(more_reg, html)

    for more_path_str in more_btns:
        more_path = more_path_str

    # 获得所有 push news 的内容
    soup = BeautifulSoup(html, "html.parser")
    new_divs = soup.find_all(attrs={'class': 'push news'})

    return grouped_data(new_divs)


# 获取More地址
def get_more_url(path):
    return f"{BASE_URL}/{path}"


# 构建字典
def build_dict(pro_type):
    dict = {}

    for v in pro_type.values():
        dict[v] = []

    return dict


# 根据项目分组数据
def grouped_data(new_divs):
    # 最近推送时间
    global last_push_time
    # 结果集
    dict_arr = []
    # 是否停止,当推送内容的时间小于上次记录的推送时间则停止
    stop_flag = False

    for new_divs_str in new_divs:
        # 获取工程名称
        soup = BeautifulSoup(str(new_divs_str), "html.parser")
        a_arr = soup.p.find_all("a")
        push_user_name = a_arr[0].string

        # 如果推送者不是自己，则跳过此次循环
        if push_user_name != get_yaml_value("name"):
            continue

        # 项目名
        pro_name = a_arr[-1].string

        # 命令行未设置配置参数则以yaml文件记录的时间为准
        if SHOW_PAGE_TOTAL == 0:
            # 核对时间,如提交时间小于记录时间则break
            ps = soup.find_all("p")
            span_attrs = ps[-1].span.attrs
            push_time = ''
            if 'title' in span_attrs:
                push_time = ps[-1].span.attrs["title"]
            else:
                push_time = ps[-1].span.attrs["data-content"]

            # 获取之前的提交时间
            if IS_DAILY_PAPER != 0:
                old_push_time = get_yaml_value("daily_push_time")
            else:
                old_push_time = get_yaml_value("push_time")

            # 记录最大的时间
            if last_push_time == "":
                last_push_time = push_time

            if datetime.strptime(push_time, GMT_FORMAT) <= datetime.strptime(old_push_time, GMT_FORMAT):
                stop_flag = True
                break

        # 找出用户push的内容
        push_lis = soup.find_all("li")
        for li in push_lis:
            push_dict = {}
            li_soup = BeautifulSoup(str(li), "html.parser")

            user_tag = ""
            # 使用find_all确保有img元素
            imgs = li_soup.find_all("img")
            for img in imgs:
                user_tag = li_soup.img.get("src")
                # 只取第一个img的值
                break

            # 不是登录用户则continue (由于网页的布局的特殊性，只能用user_tag来标识用户)
            if user_tag != get_yaml_value("user_tag"):
                continue

            # 使用find_all确保有span元素
            spans = li_soup.find_all("span")
            for span in spans:
                content = li_soup.span.string.replace("\n", "")

                if need_record_content(content):
                    push_dict[pro_name] = content

            dict_arr.append(push_dict)

    return dict_arr, stop_flag


# 显示push内容
def show_push_content():
    dict_arr = []

    # SHOW_PAGE_TOTAL == 0时 ，默认5页，以最近推送时间为准
    page = 5
    if SHOW_PAGE_TOTAL > 0:
        page = SHOW_PAGE_TOTAL

    for index in range(0, page):
        # 第一个请求用于登录并获取第一页数据
        if index == 0:
            # 登录数据
            username = get_yaml_value("username")
            password = get_yaml_value("password")
            login_data = { "user_name": username, "password": password }

            r_tuple = get_push_content(LOGIN_URL, login_data)
        else:
            r_tuple = get_push_content(get_more_url(more_path), "", True)

        dict_arr = dict_arr + r_tuple[0]

        if r_tuple[1]:
            break

    # 获取项目中文名与项目工程名的键值对
    pro_type = get_yaml_value("pro_type")

    # 合并多次请求结果
    final_dict = build_dict(pro_type)
    for dict in dict_arr:
        for k, v in dict.items():
            if k in final_dict:
                final_dict[k].append(v)

    # 输出，拼接字符串，并将字符串复制到系统剪贴板
    result = ""
    for k, v in final_dict.items():
        for prok, prov in pro_type.items():
            if k == prov:
                if len(v) > 0:
                    result = result + "\n" + prok + ":" + "\n"
                    for index, content in enumerate(v):
                        result = result + f"{content}" + "\n"
                        # result = result + f"{index + 1}. {content}" + "\n"

    # 将结果复制到系统剪贴板
    pyperclip.copy(result)
    print(result)

    # 有输出且命令行未设置page参数，则记录最后的推送时间，下去爬取日志时取此时间之后的推送内容
    if len(dict_arr) > 0 and SHOW_PAGE_TOTAL == 0:
        set_push_time(last_push_time)


# 获取yaml文件的value (暂无考虑出现异常的情况)
def get_yaml_value(the_key):
    # 读取文件内容
    with open(YAML_FILE_PAHTH, encoding='utf-8') as f:
        doc = yaml.safe_load(f)
        if "company_git" in doc and the_key in doc["company_git"]:
            return doc["company_git"][the_key]

    # 如无时间则返回 2020-03-08 17:47:32
    return "Sun, 08 Mar 2020 17:47:32 CST"


# 设置最近推送时间
def set_push_time(time):
    with open(YAML_FILE_PAHTH, encoding='utf-8') as f:
        doc = yaml.safe_load(f)

    # 修改值
    if IS_DAILY_PAPER != 0:
        doc['company_git']['daily_push_time'] = time
    else:
        doc['company_git']['push_time'] = time

    # 保存修改
    with open(YAML_FILE_PAHTH, 'w', encoding='utf-8') as f:
        yaml.safe_dump(doc, f, default_flow_style=False)


# 判断是否记录此内容 （两个判断一样）
# 周报模式: 如是Merge 或 包含特定字符串 则不记录到dict
# 日报模式: 如是Merge 或 包含特定字符串 则不记录到dict
def need_record_content(content):
    if IS_DAILY_PAPER != 0:
        if not ("Merge branch" in content or NO_RECORD_TAG in content):
            return True
        else:
            return False
    else:
        if not ("Merge branch" in content or NO_RECORD_TAG in content):
            return True
        else:
            return False


show_push_content()
