import json

import requests


def getScanNodesByPoolCode(pool_code):
    url = "https://api.thegraph.com/subgraphs/name/forta-network/forta-network"
    payload = json.dumps({
        "operationName": "ScannerPoolsQuery",
        "variables": {
            "first": 2,
            "id_in": [pool_code]
        },
        "query": "query ScannerPoolsQuery($orderBy: String = \"id\", $orderDirection: String = \"asc\", $first: Int = 12, $id_gt: String = \"\", $id_in: [String!], $chainId: Int, $skip: Int) {\n  scannerPools(\n    orderBy: $orderBy\n    orderDirection: $orderDirection\n    where: {id_in: $id_in}\n    first: $first\n    skip: $skip\n  ) {\n    id\n    chainId\n    status\n    chainId\n    stakeAllocated\n    stakeDelegated\n    stakeOwned\n    stakeOwnedAllocated\n    apyForLastEpoch\n    oldCommission\n    commission\n    commissionSinceEpoch\n    owner {\n      id\n      __typename\n    }\n    scanNodes {\n      id\n      enabled\n      __typename\n    }\n    __typename\n  }\n}\n"
    })
    headers = {
        'authority': 'api.thegraph.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://app.forta.network',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': '__cf_bm=iRxVZxAX6AJgPGdutMF1tH81GPDPUzL8TqlA9X81oRY-1706090709-1-AXlDjr+U0jKZljdi6UFGuu09ZgdEFQh+3hoM6taX0nHixeHjWqrEjx3+Y+ExlpQ952+odB74MgQim/gxLgG5P6U='
    }

    resp = requests.request("POST", url, headers=headers, data=payload)
    data = json.loads(resp.text)
    scan_nodes = data['data']['scannerPools'][0]['scanNodes']
    url_list = []
    for i in scan_nodes:
        if i['enabled'] == True:
            url_list.append({"id": i['id'], "pool": pool_code, "sla": 0,
                               'url': 'https://api.forta.network/stats/sla/scanner/' + i['id']
                               })
            pass
    return url_list
pass


import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_email(account, password, to_addr, subject, body):
    smtp_server = 'smtp.163.com'
    port = 465  # 163邮箱的SSL端口号

    # 创建一个 MIMEText 对象（包含邮件内容和格式）
    msg = MIMEText(body, 'plain', 'utf-8')
    msg['From'] = Header(account)
    msg['To'] = Header(to_addr)
    msg['Subject'] = Header(subject)

    # 使用 SSL 加密的 SMTP 会话
    with smtplib.SMTP_SSL(smtp_server, port) as server:
        server.login(account, password)  # 登录邮箱
        server.sendmail(account, [to_addr], msg.as_string())  # 发送邮件

# 使用函数示例
# send_email('a0x5b22bbb@163.com', 'PERTIWYAGRVKVXAV', 'a0x5b22bbb@163.com', 'Forta Node SLA Alert ', 'Hello, this is a test email.')