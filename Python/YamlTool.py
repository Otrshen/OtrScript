import yaml
import Glob


# 获取yaml文件的value (暂无考虑出现异常的情况)
def get_yaml_value(key1, key2):
    # 读取文件内容
    with open(Glob.YAML_FILE_PATH, encoding='utf-8') as f:
        doc = yaml.safe_load(f)
        if key1 in doc and key2 in doc[key1]:
            return doc[key1][key2]

    return ""


# 设置值
def set_push_time(key1, key2, value):
    path = Glob.YAML_FILE_PATH
    with open(path, encoding='utf-8') as f:
        doc = yaml.safe_load(f)

    doc[key1][key2] = value

    # 保存修改
    with open(path, 'w', encoding='utf-8') as f:
        yaml.safe_dump(doc, f, default_flow_style=False)
