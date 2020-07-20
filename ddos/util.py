ddos = open('ddos.py', 'r')
content = ddos.readlines()

target = open('/var/www/html/ddos.py', 'w')
for item in content:
    target.write(item)
