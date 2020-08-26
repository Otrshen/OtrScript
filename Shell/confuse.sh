#!/bin/bash
# author: Otrshen - https://github.com/Otrshen/OtrScript
#

STRING_SYMBOL_FILE="names.list"
STRING_SYMBOL_FILE_SNN="storyboard_xib_names.list"
HEAD_FILE="$PROJECT_DIR/$PROJECT_NAME/ObConfuseDef.h"

# 加前缀防止产生以数字开头的md5值
function md5(){
    # 其中"$1yan"中的"yan"为md5中的盐，可自行修改。
    md5_str=`echo -n "$1yan" | md5sum | cut -d ' ' -f 1`
    echo "ET_"$md5_str
};

# 删除之前的头文件
rm -f $HEAD_FILE

# 重新建立头文件
touch $HEAD_FILE

# 构建头文件
echo "// 创建于 `date '+%Y-%m-%d %H:%M:%S'`" >> $HEAD_FILE
echo '' >> $HEAD_FILE
echo '#ifndef ObConfuseDef_h' >> $HEAD_FILE
echo '#define ObConfuseDef_h' >> $HEAD_FILE
echo '' >> $HEAD_FILE
echo '/* ---------- 普通类、方法、属性 --------- */' >> $HEAD_FILE
echo '' >> $HEAD_FILE

# 普通类、方法、属性
cat "$STRING_SYMBOL_FILE" | while read -ra line; do
    if [[ ! -z "$line" ]]; then
    	md5_str=$(md5 $line)
        echo "#define $line $md5_str" >> $HEAD_FILE
    fi
done

echo '' >> $HEAD_FILE
echo '/* -------- storyboard或xib中的类名、方法名、属性名 ------- */' >> $HEAD_FILE
echo '' >> $HEAD_FILE

# Debug状态下还原storyboard和nib文件
# Release状态下进行混淆

if [ ${CONFIGURATION} == "Debug" ]; then

	echo "还原storyboard或nib文件中的类名、方法名、属性名";

	# 还原storyboard或nib文件中的类名、方法名、属性名
	cat "$STRING_SYMBOL_FILE_SNN" | while read -ra line; do
	    if [[ ! -z "$line" ]]; then
			md5_str=$(md5 $line)
	     #    echo "#define $line $md5_str" >> $HEAD_FILE

	        # 修改storyboard文件
			ls -R | find $PROJECT_DIR -name "*.storyboard" | while read -ra sb_path; do
				# 还原类名、方法名、属性名
				sed -i '' "s/customClass=\"$md5_str\"/customClass=\"$line\"/g" $sb_path
				sed -i '' "s/property=\"$md5_str\"/property=\"$line\"/g" $sb_path
				sed -i '' "s/selector=\"$md5_str:\"/selector=\"$line:\"/g" $sb_path
			done

			# 修改xib文件
			ls -R | find $PROJECT_DIR -name "*.xib" | while read -ra sb_path; do
				sed -i '' "s/customClass=\"$md5_str\"/customClass=\"$line\"/g" $sb_path
				sed -i '' "s/property=\"$md5_str\"/property=\"$line\"/g" $sb_path
				sed -i '' "s/selector=\"$md5_str:\"/selector=\"$line:\"/g" $sb_path
			done
	    fi
	done

else

	echo "混淆storyboard或nib文件中的类名、方法名、属性名";

	# 混淆storyboard或nib文件中的类名、方法名、属性名
	cat "$STRING_SYMBOL_FILE_SNN" | while read -ra line; do
	    if [[ ! -z "$line" ]]; then
	    	md5_str=$(md5 $line)
	        echo "#define $line $md5_str" >> $HEAD_FILE

	        # 修改storyboard文件
			ls -R | find $PROJECT_DIR -name "*.storyboard" | while read -ra sb_path; do
				# 修改类名、属性名、方法名
				sed -i '' "s/customClass=\"$line\"/customClass=\"$md5_str\"/g" $sb_path
				sed -i '' "s/property=\"$line\"/property=\"$md5_str\"/g" $sb_path
				sed -i '' "s/selector=\"$line:\"/selector=\"$md5_str:\"/g" $sb_path
			done

			# 修改xib文件
			ls -R | find $PROJECT_DIR -name "*.xib" | while read -ra sb_path; do
				sed -i '' "s/customClass=\"$line\"/customClass=\"$md5_str\"/g" $sb_path
				sed -i '' "s/property=\"$line\"/property=\"$md5_str\"/g" $sb_path
				sed -i '' "s/selector=\"$line:\"/selector=\"$md5_str:\"/g" $sb_path
			done
	    fi
	done

fi

echo '' >> $HEAD_FILE
echo '#endif /* ObConfuseDef_h */' >> $HEAD_FILE
