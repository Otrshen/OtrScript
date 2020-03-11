import re
import yaml
import argparse
import requests

from enum import Enum
from datetime import datetime
from bs4 import BeautifulSoup

# ================== 命令行输入参数，默认值：1 ======================== #

parser = argparse.ArgumentParser(usage='参数说明')
parser.add_argument('-p', dest='page', type=int, help='共查询几页提交记录', default=2)
args = parser.parse_args()

# ================== 可修改数据 ======================== #

# 总共显示几页数据
SHOW_PAGE_TOTAL = args.page
# push记录包含此字符串则不打印 (DRD : Don't record)
NO_RECORD_TAG = "DRD"
# 时间格式，每次爬完Git记录时间，以免下次爬取重复内容
GMT_FORMAT = '%a, %d %b %Y %H:%M:%S CST'
# YAML文件路径，将敏感信息放入配置文件
YAML_FILE_PAHTH = "/Users/a1/Documents/GitHub/otr-config/weekly.yaml"
# Git URL
BASE_URL = "http://10.3.40.239:3000"
LOGIN_URL = f"{BASE_URL}/user/login"

# ====================================================== #

# 全局变量

# 更多路径，用于点击更多按钮
more_path = ""
# 最大的推送时间
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
    dict_arr = []
    # print(new_divs)

    for new_divs_str in new_divs:
        soup = BeautifulSoup(str(new_divs_str), "html.parser")
        a_arr = soup.p.find_all("a")
        pro_name = a_arr[-1].string

        # 核对时间,如提交时间小于记录时间则break
        time_flag = False
        push_time_spans = soup.find_all(attrs={'class': 'time-since'})
        for span in push_time_spans:
            push_time = span.attrs["title"]
            old_push_time = get_yaml_value("push_time")

            # 记录最大的时间
            if last_push_time == "":
            	last_push_time = push_time

            if datetime.strptime(push_time, GMT_FORMAT) < datetime.strptime(old_push_time, GMT_FORMAT):
	            time_flag = True

        if time_flag:
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

                # 如是Merge或包含特定字符串则不记录到dict
                if not ("Merge branch" in content or NO_RECORD_TAG in content):
                    push_dict[pro_name] = content

            dict_arr.append(push_dict)

    return dict_arr


# 显示push内容
def show_push_content():
    dict_arr = []

    for index in range(0, SHOW_PAGE_TOTAL):
        # 第一个请求用于登录并获取第一页数据
        if index == 0:
        	# 登录数据
        	username = get_yaml_value("username")
        	password = get_yaml_value("password")
        	login_data = { "user_name": username, "password": password }

        	arr = get_push_content(LOGIN_URL, login_data)
        else:
            arr = get_push_content(get_more_url(more_path), "", True)

        dict_arr = dict_arr + arr

	# 获取项目中文名与项目工程名的键值对
    pro_type = get_yaml_value("pro_type")

    # 合并多次请求结果
    final_dict = build_dict(pro_type)
    for dict in dict_arr:
        for k, v in dict.items():
            if k in final_dict:
                final_dict[k].append(v)

    # 输出
    for k, v in final_dict.items():
        for prok, prov in pro_type.items():
            if k == prov:
                if len(v) > 0:
                    print()
                    print(prok + ":")
                    for index, content in enumerate(v):
                        print(f"{index + 1}. {content}")

    # 有输出时，则记录最后的推送时间，下去爬取日志时取此时间之后的推送内容
    if len(dict_arr) > 0:
    	print("时间：" + last_push_time)
    	set_push_time(last_push_time)


# 获取yaml文件的value (暂无考虑出现异常的情况)
def get_yaml_value(the_key):
    # 读取文件内容
    with open(YAML_FILE_PAHTH, encoding='utf-8') as f:
        doc = yaml.safe_load(f)
        if "company_git" in doc and the_key in doc["company_git"]:
            return doc["company_git"][the_key]

    # 如无时间则返回 2020-03-08 17:47:32
    # return "Mon, 24 Feb 2020 15:47:04 CST"
    return "Sun, 08 Mar 2020 17:47:32 CST"


def set_push_time(time):
    with open(YAML_FILE_PAHTH, encoding='utf-8') as f:
        doc = yaml.safe_load(f)

    # 修改值
    doc['company_git']['push_time'] = time

    # 保存修改
    with open(YAML_FILE_PAHTH, 'w', encoding='utf-8') as f:
        yaml.safe_dump(doc, f, default_flow_style=False)
        # print(doc)

# 项目类型
# PRO_TYPE = get_yaml_value("pro_type")
# print(build_dict())
show_push_content()
# print(type(get_yaml_value("pro_type")))