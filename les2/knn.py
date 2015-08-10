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
#归一化
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals,(m,1))
    #特征值相除
    normDataSet = normDataSet/tile(ranges,(m,1))
    return normDataSet,ranges,minVals

##测试
def datingClassTest(hoRatio,f):
    datingDataMat,datingLabels = file2matrix(f)
    normMat,ranges,minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRatio)
    errorCount = 0.0
    for i in range(numTestVecs):
        classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
        print "the classifier came back with:%d,the real answer is :%d "%(classifierResult,datingLabels[i])
        if(classifierResult != datingLabels[i]):
            errorCount += 1.0
        print "the total error rate is: %f"%(errorCount/float(numTestVecs))

def classifyPerson(f):
    resultList = ['not at all','in small doses','in large doses']
    percentTats = float(raw_input("percenttage of time spent playing video games?"))
    ffMiles = float(raw_input("frequent flier miles earned per year?"))
    iceCream = float(raw_input("liters of ice cream consumed per year?"))
    datingDataMat,datingLabels = file2matrix(f)
    normMat,ranges,minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles,percentTats,iceCream])
    classifierResult = classify0((inArr-minVals)/ranges,normMat,datingLabels,3)
    print "You will probably like this person: ",resultList[classifierResult - 1]

def img2Vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect

if __name__ == '__main__':
    #画图
    path = u'../tools/Ch02/'
    #fig = plt.figure()
    #ax = fig.add_subplot(111)
    #ax.scatter(datingDataMat[:,0],datingDataMat[:,1],15.0*array(datingLabels),15.0*array(datingLabels))
    #plt.show()
    testVect = img2Vector(path + 'testDigits/0_13.txt')
    print testVect[0,32:63]