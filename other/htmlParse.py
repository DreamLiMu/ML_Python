# -*-coding:utf-8-*-
from BeautifulSoup import *
import os
import string
from BeautifulSoup import BeautifulSoup
from lxml import etree
from bookModel import BookModel
import re
import operator
##################
# 该代码是解决输出是中文的问题
# UnicodeEncodeError: 'ascii' codec can't encode characters in position 32-34: ordinal not in range(128
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
#####################

bookStore = u'E:\\BaiduYunDownload\\Work Docs\\文档\\读者需求分析\\Book\\'
bookDetailPath = u'E:\\BaiduYunDownload\\Work Docs\\BookInfo\\'

bookInfos = bookDetailPath + 'bookinfo.txt'
reg_space = re.compile('( )+')
reg_line = re.compile('(\n)+')

def extractInfo(bookStore=bookStore,bookInfos=bookInfos):
    books = []
    paths = os.listdir(bookStore)
    for i in range(0,len(paths)):
        paths2 = os.listdir(bookStore+paths[i])
        for j in range(0,len(paths2)):
            bookPath = bookStore+paths[i]+"\\"+paths2[j]
            if(os.path.isfile(bookPath)):
                book = BookModel()
                file = open(bookPath,'r')
                html = file.read().decode('utf-8')
                tree = etree.HTML(html)
                # 书名
                name = tree.xpath('//span[@id="productTitle"]')
                if len(name) == 0:
                    name = tree.xpath('//span[@id="btAsinTitle"]/span')
                book.bookName = name[0].text.strip()
                #作者
                author = tree.xpath('//span[@class="author notFaded"]/a')
                if len(author) == 0:
                    author = tree.xpath("//div[@class='buying']/span/a")
                str = ''
                for a in range(0,len(author)):
                    str += author[a].text.strip()+";"
                book.bookAuthor = str
                #价格
                priceStr = ''
                price = tree.xpath("//div[@class='cBoxInner']/table/tbody/tr/td/text()")
                if len(price) == 0:
                    price = tree.xpath("//div[@id='tmmSwatches']/ul/li/span/span/span[@class='a-button-inner']/a/span/span[@class='a-color-price']/text()")
                if len(price) > 0:
                    for a in range(0,len(price)):
                        if operator.contains(price[a].strip(),'￥'):
                           priceStr += reg_space.sub('',price[a].strip())+';'
                book.bookPrice = priceStr
                #Rate评分
                rate = tree.xpath("//div[@id='avgRating']/span")
                
                if len(rate) > 0:
                    book.bookRate = getText(rate[0])
                #Rank 排名
                rank = tree.xpath("//li[@id='SalesRank']")
                book.bookRank = getText(rank[0])
                #Comment 评论条数
                comm = tree.xpath("//span[@id='acrCustomerReviewText']")
                if len(comm) == 0:
                    comm = tree.xpath("//div[@class='content']/ul/li/span[@class='crAvgStars']/a")
                if len(comm) == 0:
                    comm = tree.xpath("//span[@class='tiny']/b")
                if len(comm) == 1:
                    book.bookCmmNum = getText(comm[0])
                else:
                    book.bookCmmNum = '还没有评论'
                #Class分类
                
                #Publish出版社
                publish = tree.xpath('//div[@class="content"]/ul/li')
                publishStr = ''
                if len(publish) != 0:
                    for p in range(0,len(publish)):
                        if operator.contains(getText(publish[p]),'出版社:'):
                            publishStr = publishStr + getText(publish[p])+'||'
                book.bookPublish = publishStr
            books.append(book)
    return books


#获取标签内容
def getText(elem):
    rc = []
    if elem.text is not None:
        rc.append(elem.text.strip())
    for node in elem.itertext(tag=['b','a','span','li']):
        rc.append(node.strip())
    return reg_line.sub('',''.join(rc))


if __name__ == '__main__':
    books = extractInfo()
    f = open(u'E:\\bookInfo.txt','w+')
    for book in books:
        f.write(book.toString()+"#$")
        #f.write(book.toString()+"##")
    f.flush()
    f.close()
    print "完成！"
    #print operator.contains('￥20','5')