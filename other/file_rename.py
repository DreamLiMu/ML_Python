#-*-coding:utf-8-*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import os
import png

path = u'G:\\迅雷下载\\Screen1\\'
print 'Hello world'
files = os.listdir(path)
count = 30
for old_file in files:
    old_file = path + old_file
    print old_file
    r = png.Reader(file=open(old_file,'rb'))
    pic = r.read()
    w,h = pic[0],pic[1]
    f = open(old_file, 'wb')
    writer = png.Writer(w,h,greyscale=True,bitdepth=8)
    writer.write(f, m)
    f.close()