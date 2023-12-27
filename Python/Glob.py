import YamlTool

# YAML文件路径，将敏感信息放入配置文件
# 用户需将配置文件路径修改为真实使用的路径
YAML_FILE_PATH = "./weekly.yaml"

# GIT API
GIT_BASE_URL = YamlTool.get_yaml_value("company_git", "base_url")
GIT_LOGIN_URL = f"{GIT_BASE_URL}/user/login"

# 工时 API
MHS_BASE_URL = YamlTool.get_yaml_value("man_hour_system", "base_url")
MHS_GET_IMG_URL = f"{MHS_BASE_URL}/api/captchaImage"
MHS_LOGIN_URL = f"{MHS_BASE_URL}/api/login"
MHS_REPORT_URL = f"{MHS_BASE_URL}/api/worktime/user/report"
MHS_DAILY_INFO_URL = f'{MHS_BASE_URL}/api/worktime/user/selectPersonal'