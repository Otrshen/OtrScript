#!/bin/bash

# author: Otrshen - https://github.com/Otrshen/OtrScript
# usage: 选项说明

        # 语法: sh delete_sdk_conflicting_files.sh <-p <path>>

        # OPTIONS:
        #   -p path     SDK路径
#
# 删除SDK中冲突(重复)的文件
# 1.将SDK中的armv7和arm64文件拆分出来
# 2.分别解压armv7和arm64文件
# 3.删除冲突文件
# 4.重新合并armv7和arm64文件

# 当前文件路径
readonly CURRENT_PATH=$(cd "$(dirname "$0")";pwd)

# SDK名称
SDK_PATH="SDK_PATH"

usage() {
    cat <<- EOF

        ** FAILED **

        # usage: 选项说明

        # 语法:  sh delete_sdk_conflicting_files.sh <-p <path>>
        # 例:    sh delete_sdk_conflicting_files.sh -p /Desktop/libTestSDK.a     

        # OPTIONS:
        #   -p path     SDK路径

EOF
}

# 打印
my_log() {
    echo ''
    echo '///-----------'
    echo '///' $1
    echo '///-----------'
    echo ''
}

# =================== 判断选项值 =================== #

# echo "输入参数：${*}"
# echo "参数下标：${OPTIND}"
while getopts ":p:" opt
do
    case $opt in
        p)
            SDK_PATH=${OPTARG}
            # echo "参数v的值：${OPTARG}, 参数v的下标：${OPTIND}"
            ;;
        :)
            # echo "参数${OPTARG}无值"
            usage
            exit 1
            ;;
        \?)
            # echo "无效的参数名${OPTARG}"
            usage
            exit 1
            ;; 
    esac
done

# 判断path是否有值
if [ $SDK_PATH == 'SDK_PATH' ];then
    usage
    exit 1
fi

# 判断文件是否存在
if [ ! -e $SDK_PATH ];then
    my_log '文件不存在'
    exit 1
fi

# 获取SDK名称
readonly SDK_NAME=`basename ${SDK_PATH} | awk -F "." '{print $1}'`
# 获取文件后缀
readonly SDK_SUFFIX=`basename ${SDK_PATH} | awk -F "." '{print $NF}'`

# 判断是否是.a静态库
if [ ${SDK_SUFFIX} != 'a' ];then
    my_log '文件不是.a静态库'
    exit 1
fi

# 文件输出路径
readonly SDK_TEMP_PATH=~/Desktop/OtrScriptTempFiles/${SDK_NAME}/delete_sdk_conflicting_files
readonly SDK_TEMP_PATH_ARMV7=${SDK_TEMP_PATH}/armv7
readonly SDK_TEMP_PATH_ARM64=${SDK_TEMP_PATH}/arm64

# 创建临时路径
mkdir -p ${SDK_TEMP_PATH_ARMV7}
mkdir -p ${SDK_TEMP_PATH_ARM64}

# 分离静态库
lipo ${SDK_PATH} -thin armv7 -output ${SDK_TEMP_PATH_ARMV7}/armv7_${SDK_NAME}.a
lipo ${SDK_PATH} -thin arm64 -output ${SDK_TEMP_PATH_ARM64}/arm64_${SDK_NAME}.a

# 解压.a 
cd ${SDK_TEMP_PATH_ARMV7}
ar -x armv7_${SDK_NAME}.a
cd ..

# 删除文件
sh ${CURRENT_PATH}/delete_sdk_conflicting_files_supporting.sh ${SDK_TEMP_PATH_ARMV7}

# 打包.a
cd ${SDK_TEMP_PATH_ARMV7}
ar rcs new_armv7_${SDK_NAME}.a *.o
cd ..

cd ${SDK_TEMP_PATH_ARM64}
ar -x arm64_${SDK_NAME}.a
cd ..

sh ${CURRENT_PATH}/delete_sdk_conflicting_files_supporting.sh ${SDK_TEMP_PATH_ARM64}

cd ${SDK_TEMP_PATH_ARM64}
ar rcs new_arm64_${SDK_NAME}.a *.o
cd ..

# 合并.a
lipo -create armv7/new_armv7_${SDK_NAME}.a arm64/new_arm64_${SDK_NAME}.a -output ${SDK_NAME}.a

my_log "完成: ${SDK_TEMP_PATH}"