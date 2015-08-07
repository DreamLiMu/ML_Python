#-*-coding:utf-8-*-
###################
# 该代码是解决输出是中文的问题
# UnicodeEncodeError: 'ascii' codec can't encode characters in position 32-34: ordinal not in range(128
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
#####################
from numpy import *
import operator
#引进matplotlib
import matplotlib
import matplotlib.pyplot as plt

# 创建数据集
def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
    labels = ['A','A','B','B']
    return group,labels

# 分类算法
def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    #距离计算
    diffMat = tile(inX, (dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()
    classCount = {}
    #选择距离最小的k个点
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.iteritems(),
        key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]
#读取文件数据生成矩阵
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
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat,classLabelVector

if __name__ == '__main__':
    path = u'tools\\Ch02\\'
    datingDataMat,datingLabels = file2matrix(path + 'datingTestSet2.txt')
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(datingDataMat[:,0],datingDataMat[:,1],15.0*array(datingLabels),15.0*array(datingLabels))
    plt.show()
    