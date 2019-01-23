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

# 获取class名为panel下panel-heading的内容
print(soup.select('.panel .panel-heading'))

# 获取class名为ul和li的内容
print(soup.select('ul li'))

# 获取class名为element，id为list-2的内容
print(soup.select('#list-2 .element'))

# 使用get_text()获取文本内容
for li in soup.select('li'):
    print(li.get_text())

# 获取属性的时候可以通过[属性名]或者attrs[属性名]
for ul in soup.select('ul'):
    print(ul['id'])
    # print(ul.attrs['id'])
