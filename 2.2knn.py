#-*-coding:utf-8-*-
###################
# 该代码是解决输出是中文的问题
# UnicodeEncodeError: 'ascii' codec can't encode characters in position 32-34: ordinal not in range(128
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
#######################
from numpy import *
import operator

def file2matrix(filename):
    fr = open(filename)
    arrayOlines = fr.readlines()
    #得到文件行数
    numberOfLines = len(arrayOlines)
    #创建返回Numpy的矩阵
    returnMat = zeros((numberOfLines,3))

    classLabelVector = []
    index = 0
    #解析文件数据到列表
    for line in arrayOlines:
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1