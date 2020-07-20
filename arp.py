import os
import re

from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp

UNKNOWN_MAC = 'ff:ff:ff:ff:ff:ff'
PATTERN = '\w\w:\w\w:\w\w:\w\w:\w\w:\w\w'


def get_mac_address(network):
    temp = os.popen('ifconfig ' + network)
    result = temp.readlines()
    for item in result:
        condition = re.search(PATTERN, item)
        if condition:
            return condition.group(0)


def get_ip_list(ip):
    temp = str(ip).split('.')
    ip_list = []
    for i in range(1, 255):
        ip_list.append(temp[0] + '.' + temp[1] + '.' + temp[2] + '.' + str(i))
    return ip_list


def arp_scan(local_ip, network='ens33'):
    mac = get_mac_address(network)
    ip_list = get_ip_list(local_ip)

    temp = srp(Ether(src=mac, dst=UNKNOWN_MAC) /
               ARP(op=1, hwsrc=mac, hwdst=UNKNOWN_MAC, psrc=local_ip, pdst=ip_list),
               iface=network, timeout=1, verbose=False)

    result = temp[0].res
    result_list = []
    number = len(result)
    for i in range(number):
        result_ip = result[i][1].getlayer(ARP).fields['psrc']
        result_mac = result[i][1].getlayer(ARP).fields['hwsrc']
        result_list.append((result_ip, result_mac))
    return result_list


if __name__ == '__main__':
    # 172.16.12.1
    print("Please Input IP:")
    ip = input()
    print("Please Input Network Interface:")
    network = input()
    result = arp_scan(ip, network)
    for item in result:
        print('%-20s%-20s' % (item[0], item[1]))