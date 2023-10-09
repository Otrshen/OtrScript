import string

import ddddocr
import requests
import base64
import json
import time
from enum import Enum


class ProType(Enum):
    # 其他工作
    OTHER = 1
    # 嘟嘟分享项目
    DOSHARE = 118


# 工时系统

BASE_URL = "http://10.3.47.112"
GET_IMG_URL = f"{BASE_URL}/api/captchaImage"
# 登录接口
LOGIN_URL = f"{BASE_URL}/api/login"
# 汇报接口
REPORT_URL = f"{BASE_URL}/api/worktime/user/report"
# 日报详情接口
DAILY_INFO_URL = f'{BASE_URL}/api/worktime/user/selectPersonal'

token = ''
# 登录重试次数
login_retry_times = 5

s = requests.Session()
s.headers = {'Content-Type': 'application/json;charset=UTF-8'}


def get_img():
    response = s.get(GET_IMG_URL)
    json_data = json.loads(response.text)
    # print(response.text)
    return json_data


# 识别验证码
def ocr_img(json_data):
    ocr = ddddocr.DdddOcr(show_ad=False)
    data = base64.b64decode(json_data['img'])
    res = ocr.classification(data)
    print('🟢 验证码：' + res)
    return res


# 获取年月日字符串，如 2023-09-28
def get_time_str():
    # 获取当前日期
    t = time.localtime()
    ymd = time.strftime("%Y-%m-%d", t)
    return ymd


def login():
    global token
    global login_retry_times

    if login_retry_times == 0:
        print('🔴 登录重试次数达上限')
        return False

    json_data = get_img()
    code = ocr_img(json_data)

    dict = {'username': 'shenyn', 'password': 'shen123', 'code': code, 'uuid': json_data['uuid']}
    response = s.post(url=LOGIN_URL, json=dict)
    result_data = json.loads(response.text)
    if result_data['code'] == 200:
        print('🟢 登录成功')
        token = result_data['token']
        return True
    else:
        print('🔴 登录失败：' + response.text)

        if result_data['msg'] == '验证码错误':
            login_retry_times = login_retry_times - 1
            time.sleep(1.5)
            return login()

        return False


def generate_daily_params(content: string, type: ProType):
    ymd = get_time_str()
    print('🕔 报告日期:' + ymd)

    if type == ProType.DOSHARE:
        print('🟢 提交项目：【亿信通】产品研发')
        return [{'projectId': 118, 'projectName': '【亿信通】产品研发', 'workingDesc': content, 'workingHours': 8, 'workingDay': ymd}]
    if type == ProType.OTHER:
        print('🟢 提交项目：其他工作')
        return [{'projectId': 1, 'projectName': '其他工作', 'workingDesc': content, 'workingHours': 8,
                 'workingDay': ymd}]

    return []


# 提交日报
def commit_daily(params):
    if not params:
        print('🔴 未知项目，无法提交')
        return False

    response = s.post(url=REPORT_URL, json=params, headers={'Authorization': f'Bearer {token}'})
    result_data = json.loads(response.text)
    if result_data['code'] == 200:
        print('🟢 日报提交成功')
        return True
    else:
        print('🔴 日报提交失败：' + response.text)
        return False


# 登录并提交日报
def login_and_commit(content, type):
    if login():
        time.sleep(1)
        return commit_daily(generate_daily_params(content, type))


# 查看当天日报详情
def query_daily_info():
    ymd = get_time_str()
    params = {'workingDay': ymd}
    response = s.post(url=DAILY_INFO_URL, json=params, headers={'Authorization': f'Bearer {token}'})
    result_data = json.loads(response.text)
    if result_data['code'] == 200:
        print('🟢 日报查询成功：')
        print(json.dumps(result_data['rows'], indent=4, ensure_ascii=False))
    else:
        print('🔴 日报查询失败：' + response.text)

