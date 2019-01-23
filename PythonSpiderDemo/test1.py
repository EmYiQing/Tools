# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup

html = '''
<html>
<head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>
<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>
<p class="story">...</p>
</body>
</html>
'''
soup = BeautifulSoup(html, 'lxml')

# BeautifulSoup中有内置的方法来实现格式化输出
print(soup.prettify())

# title标签内容
print(soup.title.string)

# title标签的父节点名
print(soup.title.parent.name)

# 标签名为p的内容
print(soup.p)

# 标签名为p的class内容
print(soup.p["class"])

# 标签名为a的内容
print(soup.a)

# 查找所有的字符a
print(soup.find_all('a'))

# 查找id='link3'的内容
print(soup.find(id='link3'))



