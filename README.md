![language](https://img.shields.io/badge/language-Python3%7CShell-brightgreen) ![license](https://img.shields.io/badge/license-MIT-373737)

# OtrScript

> Python脚本，Shell脚本集合。

## Python

### 文件说明

文件名 | 用途 |  详细说明 
-|-|-
weekly.py | 爬取git提交记录，生成周报 | -
ManHourSystem.py | 工时系统接口 | -
ReportDaily.py | 汇报 | -
Glob.py | 全局常量 | 
weekly.yaml | 配置文件（模版） | 

### 使用说明

1. 复制`weekly.yaml`文件，修改相关参数。
2. 修改`Glob.py`文件中关于`weekly.yaml`的引用路径。

命令演示：

```shell
# 帮助命令
python3 ReportDaily.py --help
# 提交某个项目
python3 ReportDaily.py -d 1
# 获取工时月报
python3 ManHourSystem.py -m 1
```

### 依赖库

```shell
pip3 install pyyaml
pip3 install argparse
pip3 install requests
pip3 install pyperclip
pip3 install bs4
pip3 install chardet
pip3 install chinesecalendar
# 请使用指定版本1.4.8
pip3 install ddddocr
```

## Shell

文件名 | 用途 |  详细说明 
-|-|-
see_sdk_included_files.sh | 查看.a静态库包含哪些文件 | -
delete_sdk_conflicting_files.sh<br/>delete_sdk_conflicting_files_supporting.sh | 删除.a静态库中冲突文件并重新打包 | -
sqlcipher_decrypt.exp<br/>sqlcipher_encrypt.exp | SQLCipher加解密数据库脚本 | -
confuse.sh | `Objective-C`混淆脚本 | 无

## Terminal

文件名 | 用途 |  详细说明 
-|-|-
.bash_profile_otrshen | 终端`alias`积累 | -
