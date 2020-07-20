from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sr


def tcp_scan(target_ip, start_port, end_port):
    temp = sr(IP(dst=target_ip) /
              TCP(dport=(int(start_port), int(end_port)), flags=''),
              timeout=3, verbose=False)
    result = temp[0].res
    port_list = [i for i in range(int(start_port), int(end_port) + 1)]
    close_list = []
    for i in range(len(result)):
        if result[i][1].haslayer(TCP):
            tcp_pack = result[i][1].getlayer(TCP).fields
            if tcp_pack['flags'] == 20:
                close_list.append(tcp_pack['sport'])
    open_list = list(set(port_list).difference(set(close_list)))
    for item in sorted(open_list):
        print('%-18s%-12sOpen' %
              (target_ip, 'Port:' + str(item)))


if __name__ == '__main__':
    tcp_scan("172.16.12.135", "1", "100")
