import ddddocr
import requests
import base64
import json
import time

# 工时系统

BASE_URL = "http://10.3.47.112"
GET_IMG_URL = f"{BASE_URL}/api/captchaImage"
LOGIN_URL = f"{BASE_URL}/api/login"
REPORT_URL = f"{BASE_URL}/api/worktime/user/report"

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


# 提交日报
def commit_daily(content):
    # 获取当前日期
    t = time.localtime()
    ymd = time.strftime("%Y-%m-%d", t)
    arr = [{'projectId': 118, 'projectName': '【亿信通】产品研发', 'workingDesc': content, 'workingHours': 8, 'workingDay': ymd}]
    print('🕔 报告日期:' + ymd)
    response = s.post(url=REPORT_URL, json=arr, headers={'Authorization': f'Bearer {token}'})
    result_data = json.loads(response.text)
    if result_data['code'] == 200:
        print('🟢 日报提交成功')
    else:
        print('🔴 日报提交失败：' + response.text)


def login_and_commit(content):
    if login():
        time.sleep(1)
        commit_daily(content)
