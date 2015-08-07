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
if __name__ == '__main__':
    group,labels = createDataSet()
    print classify0([1.5,0],group,labels,3)
