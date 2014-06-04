    # -*- coding: utf-8 -*-
#---------------------------------------
#   程序：stock_assistant
#   版本：0.1 
#   作者：glx
#   日期：2014-06-04 
#   语言：Python 2.7 
#   功能：方便上班时看股票
#---------------------------------------

import sys
import urllib
import urllib2
import re
import time
import string as S
import getopt
import thread

reload(sys)
sys.setdefaultencoding("utf-8")

#----------- 处理页面上的各种标签 -----------
class HTML_Tool:
    # 用非 贪婪模式 匹配 \t 或者 \n 或者 空格 或者 超链接 或者 图片
    BgnCharToNoneRex = re.compile("(\t|\n| |<a.*?>|<img.*?>)")
    
    # 用非 贪婪模式 匹配 任意<>标签
    EndCharToNoneRex = re.compile("<.*?>")

    # 用非 贪婪模式 匹配 任意<p>标签
    BgnPartRex = re.compile("<p.*?>")
    CharToNewLineRex = re.compile("(<br/>|</p>|<tr>|<div>|</div>)")
    CharToNextTabRex = re.compile("<td>")

    # 将一些html的符号实体转变为原始符号
    replaceTab = [("&lt;","<"),("&gt;",">"),("&amp;","&"),("&nbsp;"," ")]
    
    def Replace_Char(self,x):
        x = self.BgnCharToNoneRex.sub("",x)
        x = self.BgnPartRex.sub("\n    ",x)
        x = self.CharToNewLineRex.sub("\n",x)
        x = self.CharToNextTabRex.sub("\t",x)
        x = self.EndCharToNoneRex.sub("",x)

        for t in self.replaceTab:  
            x = x.replace(t[0],t[1])  
        return x  
#----------- 处理页面上的各种标签 ----------- 
class HTML_Model:

	def __init__(self,shortcode,interval = 30):
		self.page = 1
		self.tool = HTML_Tool()
		self.shortcode = shortcode
		self.interval = interval
		self.enable = False

	def GetPage(self):
		user_agent = 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT)'
		headers = {'User-Agent' : user_agent}
		# Tencet API
		myUrl = 'http://qt.gtimg.cn/q=' + self.shortcode
		req = urllib2.Request(myUrl,headers = headers)
		myResponse = urllib2.urlopen(req)
		UnicodePage = myResponse.read()
		# 匹配股票数据
		myItems = re.findall('v_(.*?)="1~(.*?)~\d+~(.*?)~.*?;',UnicodePage,re.S)
		print "--------%s-----------"%(time.asctime(time.localtime()))
		for result in myItems:
			print "###%s###\n  %s\n  %s\n"%(result[0],result[1],result[2])

	def Start(self):
		self.enable = True
		while self.enable == True:
			self.GetPage()
			time.sleep(self.interval)

def help():
	print u"""
#---------------------------------------
#   程序：stock_assistant
#   作者：glx
#   语言：Python 2.7 
#   功能：方便上班时看股票
#---------------------------------------
"""
	print u"usage: python stock_assistant.py sh600000 sh600001"
	print u"-i --interval			set interval,default is 30 sec"
	print u"-f --file				get the stock codes from a file"

def version():
	print 'v0.11 at 2014-6-4'

def main(argv):
	try:
		opts,args = getopt.getopt(argv[1:],"vhf:i:",["version","help","file=","interval="])
	except getopt.GetoptError, e:
		print e
		sys.exit(2)
	interval = None
	# shortcode = S.join(args,',')
	for o,v in opts:
		if o in ('-v','--version'):
			version()
			sys.exit(0)
		if o in ('-h','--help'):
			help()
			sys.exit(0)
		if o in ('-i','--interval'):
			interval = int(v)

		if o in ('-f','--file'):
			args = []
			lines = open(v,'r').readlines()
			for line in lines:				
				args.append(line.replace('\n',''))
	if args == None or args == [] or args == "":
		args = []
		lines = open(sys.path[0]+'/sample','r').readlines()
		for line in lines:
			args.append(line.replace('\n',''))
	shortcode = S.join(args,',')
	if interval is not None:
		myModel = HTML_Model(shortcode,interval)
	else:	
		myModel = HTML_Model(shortcode)
	myModel.Start()
if __name__ == '__main__':
	main(sys.argv)

	