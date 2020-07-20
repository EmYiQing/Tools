from scapy.layers.inet import IP, TCP
from scapy.sendrecv import sr


def tcp_scan(target_ip, start_port, end_port):
    temp = sr(IP(dst=target_ip) /
              TCP(dport=(int(start_port), int(end_port)), flags='S'),
              timeout=3, verbose=False)
    result = temp[0].res
    for i in range(len(result)):
        if result[i][1].haslayer(TCP):
            tcp_pack = result[i][1].getlayer(TCP).fields
            if tcp_pack['flags'] == 18:
                print('%-18s%-12sOpen' %
                      (target_ip, 'Port:'+str(tcp_pack['sport'])))


if __name__ == '__main__':
    tcp_scan("172.16.12.135", "1", "100")
