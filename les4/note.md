#贝叶斯分类
===
##朴素贝叶斯算法
[Baidu](http://www.baidu.com)  
~~this text is surrounded by literal asterisks~~
**this text is surrounded by literal asterisks**

*   这是列表1
*   这是列表2

==这是高亮显示==
```
def setOfWords2Vec(vocabList, inputSet):
    returnVec = [0] * len(vocabList)
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] = 1
        else:
            print the word : %s is not in my Vocabulary!%word
    return returnVec
```
