# -*-coding:utf-8 -*-
import exrex
import sys

# 过滤关键字
web_white = ['com', 'cn', 'org', 'edu', 'gov', 'www']


def host_para(host):
    """
    根据输入网址得到域名等特征信息
    例如输入：https://www.cnblogs.com/xxx
    得到结果：www.cnblogs.com.xxx
    :param host: 输入URL
    :return: 特征字符串
    """
    if '://' in host:
        host = host.split('://')[1]
    if '/' in host:
        host = host.replace('/', '.')
    return host


def dic_create(host):
    """
    生产密码字典
    :param host:经过处理的URL
    :return: None
    """

    # 比如传入www.cnblogs.comxxx
    # 得到[www,cnblogs,comxxx]
    web_dics = host.split('.')

    # 读取正则规则
    f_rule = open('rule.ini', 'r')
    rule = ""
    for i in f_rule:
        if '#' != i[0]:
            rule = i

    # 创建字典文件
    f_dic = open('dic.txt', 'w')
    f_dic.close()

    for web_dic in web_dics:
        if web_dic not in web_white:
            # 读取参考密码进行组合
            f_pass = open('pass.txt', 'r')
            for dic_pass in f_pass:
                dics = list(exrex.generate(rule.format(web_dic=web_dic, dic_pass=dic_pass.strip('\n'))))
                for dic in dics:
                    # 过滤过于简单的密码
                    if len(dic) > 4:
                        f_dic = open('dic.txt', 'a+')
                        f_dic.write(dic + "\n")
                        f_dic.close()
                        print dic.strip('\n')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        dic_create(host_para(sys.argv[1]))
        sys.exit()
    else:
        print "[*]Usage:python create_dic.py [URL]"
