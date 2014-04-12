import urllib2, urlparse, re, MySQLdb
#coding: utf-8

class PoemClass:
	def __init__(self, book_info, poem_info, title, author, poem):
		self.book_info = book_info
		self.poem_info = poem_info
		self.title = title
		self.author = author
		self.poem = poem
	def __str__(self):
		return self.book_info + ' ' + self.poem_info + ' ' + self.title + ' ' + self.author + ' ' + self.poem

def getPage(book_num, poem_num):
	book_str = str(book_num).zfill(3)
	poem_str = str(poem_num).zfill(3)
	req = urllib2.Request('http://www16.zzu.edu.cn/qtss/zzjpoem1.dll/viewoneshi?js='+book_str+'&ns='+poem_str, headers={'User-Agent' : "Magic Browser"})
	webpage= urllib2.urlopen(req)
	webcontent = webpage.read()
	print(webcontent)
	info_result = re.search(r'全唐诗第([0-9]+)卷第([0-9]+)首', webcontent)
	if info_result:
		book_info = info_result.group(1)
		poem_info = info_result.group(2)
		print(book_info + ' ' + poem_info)
	title_result = re.search(u'face="([\u4e00-\u9fa5]+)">([\u0020-\u007f_\u4e00-\u9fff_\uff01-\uffee_\u3002_\u3001_\u2026_\u201d_\u201c_\u2019_\u2018_\u300a_\u300b]+)</font>', webcontent.decode("gbk"))
	if title_result:
		title = title_result.group(2)
		print(title)
	author_result = re.search(u'face="([\u4e00-\u9fa5]+)"><u>([\u0020-\u007f_\u4e00-\u9fff_\uff01-\uffee_\u3002_\u3001_\u2026_\u201d_\u201c_\u2019_\u2018_\u300a_\u300b]+)</u>', webcontent.decode("gbk"))
	if author_result:
		author = author_result.group(2)
		print(author)
	poem_results = re.findall(u'([\u4e00-\u9fff_\uff01-\uffee_\u3002_\u3001_\u2026_\u201d_\u201c_\u2019_\u2018_\u300a_\u300b]+)<br>', webcontent.decode("gbk"))
	poem=''
	for poem_result in poem_results:
		poem  = poem + poem_result
	print(poem)
	
	newPoem = PoemClass(book_info, poem_info, title, author, poem)
	'''
	if poem_num > 2 or info_result == None:
		return
	else:
		getPage(book_num, poem_num+1)
	'''
	preservePage(newPoem)
def preservePage(poemClass):
	try:
		conn = MySQLdb.connect(host='localhost',user='root',passwd='123',db='poem', charset='utf8')
	except Exception, e:
		print e
		sys.exit()
	cursor = conn.cursor()
	sql = "insert into poem(poem_book_num, poem_poem_num, poem_title, poem_author, poem_content) values ('%s', '%s', '%s', '%s', '%s')" % (poemClass.book_info, poemClass.poem_info, poemClass.title, poemClass.author, poemClass.poem)
	try:
		cursor.execute(sql)
	except Exception, e:
		print e
	conn.commit()
	cursor.close()
	conn.close()
	'''
	# 连接数据库　
	try:
		conn = MySQLdb.connect(host='localhost',user='root',passwd='xxxx',db='test1')
	except Exception, e:
		print e
		sys.exit()

	# 获取cursor对象来进行操作

	cursor = conn.cursor()
	# 创建表
	sql = "create table if not exists test1(name varchar(128) primary key, age int(4))"
	cursor.execute(sql)
	# 插入数据
	sql = "insert into test1(name, age) values ('%s', %d)" % ("zhaowei", 23)
	try:
		cursor.execute(sql)
	except Exception, e:
		print e

	sql = "insert into test1(name, age) values ('%s', %d)" % ("张三", 21)
	try:
		cursor.execute(sql)
	except Exception, e:
		print e
	# 插入多条

	sql = "insert into test1(name, age) values (%s, %s)" 
	val = (("李四", 24), ("王五", 25), ("洪六", 26))
	try:
		cursor.executemany(sql, val)
	except Exception, e:
		print e

	#查询出数据
	sql = "select * from test1"
	cursor.execute(sql)
	alldata = cursor.fetchall()
	# 如果有数据返回，就循环输出, alldata是有个二维的列表
	if alldata:
		for rec in alldata:
			print rec[0], rec[1]


	cursor.close()

	conn.close()
	'''

if __name__ == '__main__':
	print('Hello World!')
	#for i in rage(900):
	getPage(1,2)