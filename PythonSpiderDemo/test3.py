# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup

html = '''
<div class="panel">
    <div class="panel-heading">
        <h4>Hello</h4>
    </div>
    <div class="panel-body">
        <ul class="list" id="list-1">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
            <li class="element">Jay</li>
        </ul>
        <ul class="list list-small" id="list-2">
            <li class="element">Foo</li>
            <li class="element">Bar</li>
        </ul>
    </div>
</div>
'''

soup = BeautifulSoup(html, 'lxml')

# 查找所有的ul标签内容
print(soup.find_all('ul'))

# 针对结果再次find_all,从而获取所有的li标签信息
for ul in soup.find_all('ul'):
    print(ul.find_all('li'))

# 查找id为list-1的内容
print(soup.find_all(attrs={'id': 'list-1'}))

# 查找class为element的内容
print(soup.find_all(attrs={'class': 'element'}))

# 查找所有的text='Foo'的文本
print(soup.find_all(text='Foo'))
