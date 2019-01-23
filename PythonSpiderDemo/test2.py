# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup

html = '''
<html>
<head><title>The Dormouse's story</title></head>
<body>
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

# 将p标签下的所有子标签存入到了一个列表中
print (soup.p.contents)
