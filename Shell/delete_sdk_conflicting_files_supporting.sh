#!/bin/sh

readonly FILE_PATH=$1

echo "删除${FILE_PATH}文件"

# 需要删除的文件
rm -f $FILE_PATH/SXMTestViewController.o
rm -f $FILE_PATH/SXMTest2ViewController.o

echo "删除文件完成"