#!/bin/bash

# author: otrshen
# usage: 选项说明

        # 语法: sh SeeSDKIncludedFiles.sh <-p <path>>

        # OPTIONS:
        #   -p path     SDK路径
#
# 查看SDK所包含文件
# 1.将SDK中的arm64文件拆分出来
# 2.显示SDK中包含的文件
# 3.可解压arm64SDK的文件

# SDK名称
SDK_PATH="SDK_PATH"

usage() {
    cat <<- EOF

        ** FAILED **

        # usage: 选项说明

        # 语法:  sh SeeSDKIncludedFiles.sh <-p <path>>
        # 例:    sh SeeSDKIncludedFiles.sh -p /Desktop/libTestSDK.a     

        # OPTIONS:
        #   -p path     SDK路径

EOF
}

# 打印
myLog() {
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
    myLog '文件不存在'
    exit 1
fi

# 获取SDK名称
SDK_NAME=`basename ${SDK_PATH} | awk -F "." '{print $1}'`
# 获取文件后缀
SDK_SUFFIX=`basename ${SDK_PATH} | awk -F "." '{print $NF}'`

# 判断是否是.a静态库
if [ ${SDK_SUFFIX} != 'a' ];then
    myLog '文件不是.a静态库'
    exit 1
fi

# 文件输出路径
SDK_TEMP_PATH=~/Desktop/OtrScriptTempFiles/${SDK_NAME}/arm64
# arm64文件输出路径
SDK_OUTPUT_PATH=${SDK_TEMP_PATH}/${SDK_NAME}_arm64.a

# 创建临时路径
mkdir -p ${SDK_TEMP_PATH}

# 拆分出arm64的SDK
lipo ${SDK_PATH} -thin arm64 -output ${SDK_OUTPUT_PATH}

echo ''
# 查看arm64SDK包含哪些文件
ar -t ${SDK_OUTPUT_PATH}

myLog "临时文件路径:${SDK_TEMP_PATH}"

echo ''
echo '==============================='
echo ''

echo "是否解压该SDK文件? [y/n]"

read tag
while([[ $tag != y ]] && [[ $tag != n ]])
do
echo "请输入y/n"
read tag
done

if [ $tag == y ];then

mkdir -p ${SDK_TEMP_PATH}/file    # 创建文件夹
cd ${SDK_TEMP_PATH}/file          # 进入file文件夹
ar -x ../${SDK_NAME}_arm64.a      # 解压.a静态库

myLog "解压成功:${SDK_TEMP_PATH}/file"

fi
