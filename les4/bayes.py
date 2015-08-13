#-*-coding:utf-8-*-
#该代码是解决输出是中文的问题
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
####################
from numpy import *

def loadDataSet():
    postingList = [['my','dog','has','flea','problems','help','please'],
                    ['maybe','not','take','him','to','dog','park','stupid'],
                    ['my','dalmation','is','so','cute','I','love','him'],
                    ['stop','posting','stupid','worthless','garbage'],
                    ['mr','licks','ate','my','steak','how','to','stop','him'],
                    ['quit','buying','worthless','dog','food','stupid']]
    classVec = [0,1,0,1,0,1] #1代表侮辱性文字，0代表正常言论
    return postingList,classVec

def createVocabList(dataSet):
    #创建一个空集
    vocabSet = set([])
    for document in dataSet:
        #创建两个集合的并集
        vocabSet = vocabSet | set(document)
    return list(vocabSet)

##词集模型
def setOfWords2Vec(vocabList, inputSet):
    ## 创建一个其中所含元素都为0的向量
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print "the word : %s is not in my Vocabulary!"%word
    return returnVec

##词袋模型
def bagOfWords2Vec(vocabList, inputSet):
    ## 创建一个其中所含元素都为0的向量
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
        else:
            print "the word : %s is not in my Vocabulary!"%word
    return returnVec

def trainNB0(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    ##初始化概率
    p0Num = ones(numWords); p1Num = ones(numWords)
    p0Denom = 2.0; p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            ##向量相加
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    print p1Num
    print p1Denom
    print p1Num/p1Denom
    p1Vec = log(p1Num/p1Denom) #change to log()
    ##对每个元素做除法
    p0Vec = log(p0Num/p0Denom) #change to log()
    return p0Vec,p1Vec,pAbusive    

def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
    ##元素相乘
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0
##测试贝叶斯分类器
def testingNB():
    listOPosts,listClasses = loadDataSet()
    myVocabList = createVocabList(listOPosts)
    trainMat = []
    for postinDoc in listOPosts:
        trainMat.append(bagOfWords2Vec(myVocabList,postinDoc))
    p0V,p1V,pAb = trainNB0(array(trainMat),array(listClasses))
    testEntry = ['love','stupid','dalmation']
    thisDoc = array(bagOfWords2Vec(myVocabList,testEntry))
    print testEntry,'classified as :',classifyNB(thisDoc,p0V,p1V,pAb)
    testEntry = ['my','love','garbage']
    thisDoc = array(bagOfWords2Vec(myVocabList,testEntry))
    print testEntry,'classified as :',classifyNB(thisDoc,p0V,p1V,pAb)

def textParse(bigString):
    import re
    listOfTokens = re.split(r'\\W*',bigString)
    return [tok.lower() for tok in listOfTokens if len(tok) > 2]

##垃圾邮件过滤
def spamTest():
    docList = []; classList = []; fullText = []
    for i in range(1,26):
        ##导入并解析文本文件
        wordList = textParse(open('email/spam/%d.txt' %i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(1)
        wordList = textParse(open('email/ham/%d.txt' %i).read())
        docList.append(wordList)
        fullText.extend(wordList)
        classList.append(0)
    vocabList = createVocabList(docList)
    trainingSet = range(50); testSet = []
    ##随机构建训练集
    for i in range(10):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del(trainingSet[randIndex])
    trainMat = []; trainClasses = []
    for docIndex in trainingSet:
        trainMat.append(setOfWords2Vec(vocabList,docList[docIndex]))
        trainClasses.append(classList[docIndex])
    p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
    errorCount = 0
    ##对测试集分类
    for docIndex in testSet:
        wordVector = setOfWords2Vec(vocabList,docList[docIndex])
        if classifyNB(array(wordVector),p0V,p1V,pSpam) != classList[docIndex]:
            errorCount += 1
    print 'the error rate is : ',float(errorCount)/len(testSet)    


if __name__ == '__main__':
    spamTest()
