# coding:gbk
# @author: Loid
# @GitHub:
# @Blog: loid.online
import requests
from urllib.parse import quote
import re

def keyword(kw,page=1):
    kw = quote(kw)
    header = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36"}
    url = 'https://www.baidu.com/s?wd=%s&pn=%s0'%(kw,page-1)
    req = requests.get(url,headers=header)
    res = re.findall(r'<a target="_blank" href="(\S+)" class="c-showurl"',req.text)
    return list(set(res))

def location(baiduLink):
    return requests.get(baiduLink,allow_redirects=False).headers.get('Location')

def Write_file(filename,data):
    with open(filename,'a') as f:
        f.write("{data}\n".format(data=data))

# def main(kw,page,filename = None):
#     print "Crawling: {}".format(kw)
#     for pageNum in range(1,page+1):
#         realUrl = map(location,keyword(kw,page=pageNum))
#         if filename:
#             for f in set(realUrl):
#                 Write_file(filename,f)
#             print "[Baidu-Page: {page}] Write {m} Url to the {filename}.".format(page=pageNum,m=len(realUrl),filename=filename)
#         else:
#             for f in set(realUrl):
#                 print f
