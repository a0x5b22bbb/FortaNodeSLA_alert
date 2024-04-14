import datetime
import json
import time
from threading import Thread
import sys
from queue import Queue
import requests

from test import getScanNodesByPoolCode, send_email

concurrent = 200

def doWork():

    querySLAbyUrl(q.get())
    q.task_done()

def querySLAbyUrl(scanner_info):
    url = scanner_info['url']
    resp = json.loads(requests.get(url).text)
    sla = -1
    if resp is not None or resp != '':
        temp_a = resp['statistics']
        if temp_a is not None:
            sla = temp_a['avg']
        else:
            sla = -1
    # print("这是SLA: ",sla)
    scanner_info['sla'] = sla
    pass


while True:

    q = Queue(concurrent * 2)
    for i in range(concurrent):
        t = Thread(target=doWork)
        t.daemon = True
        t.start()

    try:
        # 首先通过pool_code 获取 所有scanner_id
        # 数据结构, [{id: xxx, poo: xxx , url: xxx, sla: 0.9}]
        # 然后for 循环 获取每个item的url 把sla 输入进去, 小于0.9的 加入 warning list
        time1 = datetime.datetime.now()
        pools_code = [ '1907']
        all_scanner_nodes = []
        for pool_code in pools_code:
            for i in getScanNodesByPoolCode(pool_code):
                all_scanner_nodes.append(i)
        for scanner_info in all_scanner_nodes:
            q.put(scanner_info)
        q.join()
    except KeyboardInterrupt:
        sys.exit(1)
    except Exception as e:
        print(e)
    time2 = datetime.datetime.now()

    print("用时:", (time2-time1).seconds, "秒 时间:", time2)
    warning_list = []
    for i in all_scanner_nodes:
        if i['sla'] < 0.8:
            i.pop('url')
            warning_list.append(i)

    for i in warning_list:
        print(i)
    print(len(warning_list))
    #发送邮件
    if len(warning_list) > 0:
        body = str(len(warning_list)) + '个节点 低SLA分数 ' + str(time2)
        for i in warning_list:
            body += "\n" + str(i)
        send_email('a0x5b22bbb@163.com', 'PERTIWYAGRVKVXAV', 'a0x5b22bbb@163.com', 'Forta Node SLA Alert ' + str(len(warning_list)) , body)
        pass
    #等待30分钟
    time.sleep(60 * 60)