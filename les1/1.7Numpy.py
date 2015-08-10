#/usr/local/bin
#-*-coding:utf-8-*-
from numpy import *

#构造随机数组
ran = random.rand(4,4)
print '随机数组'
print ran

#构造矩阵 mat()
randMat = mat(random.rand(4,4))
print '矩阵'
print randMat
#矩阵求逆
print '矩阵的逆'
print randMat.I
#单位矩阵
print eye(4)