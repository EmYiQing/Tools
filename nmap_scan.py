import nmap


def nmap_scan(target_ip):
    temp = nmap.PortScanner()
    result = temp.scan(hosts=target_ip, arguments='-A')
    info = result['scan'][target_ip]
    if info['status']['state'] == 'up':
        mac = info['addresses']['mac']
        os = info['osmatch'][0]['name']
        print("IP : " + target_ip)
        print("MAC : "+mac)
        print("OS : "+os)
        # Port ......
    else:
        print("Target:" + target_ip + " Not Online!")


if __name__ == '__main__':
    nmap_scan('172.16.12.135')
