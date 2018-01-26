# coding:utf-8
import os
import sys
import requests
from urllib.parse import urlparse
from optparse import OptionParser
from spider.baiduspider import *
from spider.oshadan import *
sys.path.append(os.getcwd()+'\\plugins')

#   url 数据采集接口
class SpiderEngine():
    def __init__(self):
        self.oshadanapi = oshadan()
        self.oshadanLogin = self.oshadanapi.login()

    #   百度爬虫接口
    def baiduSpider(self,kw,page=1):
        retList = keyword(kw=kw,page=page)
        return map(lambda x:'http://{}'.format(urlparse(x).netloc),map(location,retList))

    #   oshadan数据采集接口
    def oshadanSpider(self,keyword,page):
        if self.oshadanLogin:
            retList = self.oshadanapi.search(keyword,page)
            return map(lambda x: "http://{}".format(urlparse(x).netloc), map(lambda x: x["url"], retList))

class shellFramework():
    plugins = []
    def __init__(self,pluginName,outputFile=None):
        self.pluginName = pluginName
        self.load_plugins()
        self.output = outputFile
        print('Load Plugin : {}'.format(self.pluginName))

    #   加载所有插件
    def load_plugins(self):
        self.plugins = os.listdir(os.getcwd()+'/plugins')

    #   判断是否存在插件
    def exist_plugin(self):
        return self.pluginName+'.py' in self.plugins

    #   调用解析插件
    def exec_plugin(self,url):
        if not self.exist_plugin():
            print('The plugin does not exist!')
            exit(0)

        md = __import__(self.pluginName)
        if hasattr(md,'Exploit'):
            exp = getattr(md,'Exploit')()
            ret = exp.attack(url)
            if ret:
                print(ret)
                if self.output:
                    with open(self.output,'a') as f:
                        f.write(ret+'\n')
        else:
            print('Plugin Error!')


#   列出所有插件
def listPluginView(pluginLink=None):

    def load_plugins():
        '''
            'pyc' in x or '__init' in x 返回True或者False
            [True] 等于 [1]
            [False] 等于 [0]
            filter返回结果为True的参数值
            :return:
        '''
        plugins = os.listdir(os.getcwd()+'/plugins')
        return filter(lambda x: (True,False)['pyc' in x or '__init' in x],plugins)

    plugins = load_plugins()
    if pluginLink:
        plugins = filter(lambda x: re.search(pluginLink,x),plugins)
    return plugins

#   解析命令参数
def cmdparse(keyword,page,engine,plugin,list=None,output=None):
    retSpider = []
    if list:                                                                    #设置list=None，是默认不执行该代码，-l不能和其它命令参数共同执行
        plugins = listPluginView() if list == 'all' else listPluginView(list)
        print('List Plugins:')
        for p in plugins:
            print(p[:-3])
        exit(0)

    if keyword and page and engine and plugin:
        print('Spider Engine : {}'.format(engine))
        page = str(page).split('-')
        pageIntStart = 1 if len(page)==1 else int(page[0])
        pageIntEnd = int(page[-1])

        print('Spider from page {} to page {}'.format(pageIntStart,pageIntEnd))
        # 判断采集接口并返回数据
        engineApi = SpiderEngine()
        if engine == 'baidu':
            for p in range(pageIntStart,pageIntEnd+1):
                ret = engineApi.baiduSpider(keyword,p)
                for x in ret:
                    retSpider.append(x)
                #map(lambda x:retSpider.append(x),engineApi.baiduSpider(keyword,p))
        elif engine == 'oshadan':
            for p in range(pageIntStart,pageIntEnd+1):
                map(lambda x:retSpider.append(x),engineApi.oshadanSpider(keyword,p))
        else:
            print('Error Engine! Retry!')
        #print(retSpider)
        print('Data total : {}'.format(len(retSpider)))
        pg = shellFramework(plugin,output)
        for url in set(retSpider):
            try:
                pg.exec_plugin(url)
            except requests.ConnectionError:
                continue
            except requests.TooManyRedirects:
                continue

if __name__ == '__main__':

    usage = 'usage : %prog -k "inurl:/alone/alone.php?id=" -p 30 -e baidu -l beecms_sql_40 -o beecms_down.txt'
    parse = OptionParser(usage=usage)
    parse.add_option('-k','--keyword',dest='keyword',type='string',help='Waiting for collection\'s command.',default=None)
    parse.add_option('-p','--page',dest='page',type='string',help='Collected pages.',default=10)
    parse.add_option('-e','--engine',dest='engine',type='string',help='Spidder engine',default=None)
    parse.add_option('-l','--load',dest='load',type='string',help='Load Plugin Script Name',default=None)
    parse.add_option('-s','--scripts',dest='scripts',type='string',help='List Plugin',default=None)
    parse.add_option('-o','--output',dest='output',type='string',help='Output File',default=None)
    options ,args = parse.parse_args()
    cmdparse(options.keyword,options.page,options.engine,options.load,options.scripts,options.output)
