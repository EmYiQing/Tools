import hashlib
import ipaddress
import multiprocessing
import time

from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import sr1

SUCCESS = 10001
FAILURE = 10002


def random_str_byte():
    temp = hashlib.md5()
    temp.update(bytes(str(time.time()), encoding='utf-8'))
    result = temp.hexdigest()
    return bytes(result, encoding='utf-8')


def ping(target_ip):
    package = IP(dst=target_ip) / ICMP() / random_str_byte()
    result = sr1(package, timeout=3, verbose=False)
    if result:
        return target_ip, SUCCESS
    else:
        return target_ip, FAILURE


def get_ip_list(ip):
    temp = ipaddress.ip_network(ip, False).hosts()
    ip_list = []
    for item in temp:
        ip_list.append(str(item))
    return ip_list


def do_scan(target_ip, thread_num):
    print("Please Wait......")
    ip_list = get_ip_list(target_ip)
    pool = multiprocessing.Pool(processes=int(thread_num))
    result = pool.map(ping, ip_list)
    pool.close()
    pool.join()
    for ip, res in result:
        if res == SUCCESS:
            print('%-20s%-20s' % (ip, "Success"))


if __name__ == '__main__':
    do_scan('172.16.12.1/24', 64)
