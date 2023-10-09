import weekly
import ManHourSystem
import argparse
from ManHourSystem import ProType


# 是否是嘟嘟分享
IS_DOSHARE = 0
# 是否是其他项目
IS_OTHER = 0


# 爬取日志后，再上报工时系统
def report():
    content = weekly.get_daily_content()

    if len(content) <= 0:
        print('🟠 日报内容为空\n')
        return

    print('🟢 日报内容：')
    print(content + '\n')

    type = ProType.DOSHARE
    if IS_OTHER == 1:
        type = ProType.OTHER

    flag = ManHourSystem.login_and_commit(content, type)
    print('')
    if flag:
        ManHourSystem.query_daily_info()
        print('')


if __name__ == "__main__":
    # ================== 命令行输入参数，默认值：0 ======================== #
    parser = argparse.ArgumentParser(usage='参数说明')
    parser.add_argument('-d', dest='doshare', type=int, help='嘟嘟分享项目', default=0)
    parser.add_argument('-o', dest='other', type=int, help='其他项目', default=0)
    args = parser.parse_args()

    IS_DOSHARE = args.doshare
    IS_OTHER = args.other

    report()

