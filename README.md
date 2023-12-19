![language](https://img.shields.io/badge/language-Python3%7CShell-brightgreen) ![license](https://img.shields.io/badge/license-MIT-373737)

# OtrScript

> Python脚本，Shell脚本集合。

## 文件说明

### Python

文件名 | 用途 |  详细说明 
-|-|-
weekly.py | 爬取git提交记录，生成周报 | -
ManHourSystem.py | 工时系统接口 | -
ReportDaily.py | 汇报 | -

#### 命令演示

```shell
# 帮助命令
python3 ReportDaily.py --help
# 提交某个项目
python3 ReportDaily.py -d 1
```

#### YAML配置

```yaml
company_git: # 公司git相关配置
  base_url: http://10.3.43.211:9666 # git地址
  daily_push_time: Mon, 18 Dec 2023 16:44:52 CST # 日报时间
  monthly_push_time: Mon, 27 Nov 2023 17:38:33 CST # 周报时间
  password: 123123 # 密码
  pro_type: # 项目类型，用于分类统计
    "ETKit工具类": iOS/ET-Kit
    VPN SDK: iOS/ET-VPN
  push_time: Mon, 18 Dec 2023 16:44:52 CST # 默认时间
  user_tag: /avatars/73 # 头像
  username: shenming # 用户名
man_hour_system: # 工时相关配置
  base_url: http://10.3.47.112 # 工时地址
  password: 123123 # 密码
  username: shenming # 用户名

```

### Shell

文件名 | 用途 |  详细说明 
-|-|-
see_sdk_included_files.sh | 查看.a静态库包含哪些文件 | -
delete_sdk_conflicting_files.sh<br/>delete_sdk_conflicting_files_supporting.sh | 删除.a静态库中冲突文件并重新打包 | -
sqlcipher_decrypt.exp<br/>sqlcipher_encrypt.exp | SQLCipher加解密数据库脚本 | -
confuse.sh | `Objective-C`混淆脚本 | 无

### Terminal

文件名 | 用途 |  详细说明 
-|-|-
.bash_profile_otrshen | 终端`alias`积累 | -
