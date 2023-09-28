import weekly
import ManHourSystem


# 爬取日志后，再上报工时系统
def report():
    content = weekly.get_daily_content()

    if len(content) <= 0:
        print('🟠 日报内容为空\n')
        return

    print('🟢 日报内容：')
    print(content + '\n')
    ManHourSystem.login_and_commit(content)
    print('')
    ManHourSystem.query_daily_info()
    print('')


if __name__ == "__main__":
    report()

