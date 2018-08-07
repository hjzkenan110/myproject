import logging
import time

import requests
import sqlalchemy as sa
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import datetime
from test02 import session, timelion, info

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

url_list = [
    "https://bbs.hupu.com/get_nav?fup=1",
    "https://bbs.hupu.com/get_nav?fup=232",
    "https://bbs.hupu.com/get_nav?fup=198",
    "https://bbs.hupu.com/get_nav?fup=4596",
    "https://bbs.hupu.com/get_nav?fup=234",
    "https://bbs.hupu.com/get_nav?fup=174",
    "https://bbs.hupu.com/get_nav?fup=238",
    "https://bbs.hupu.com/get_nav?fup=233",
    "https://bbs.hupu.com/get_nav?fup=41",
    "https://bbs.hupu.com/get_nav?fup=42",
    "https://bbs.hupu.com/get_nav?fup=114",
    "https://bbs.hupu.com/get_nav?fup=7"
]

def fetch(url):
    r = requests.get(url)

    if r.status_code == 200:
        # 获得13位时间戳
        millis = datetime.datetime.now()
        datas = r.json()["data"]
        for data in datas:
            data["updatetime"] = millis
            data["tpostnum"] = int(data["tpostnum"])
        return datas
    else:
        print("error" + r.text)
        return None


def main():
    for url in url_list:
        datas = fetch(url)
        if datas:
            for data in datas:
                # 上一次查询结果
                last_data = session.query(timelion).filter(timelion.fid==data["fid"]).order_by(sa.desc(timelion.updatetime)).first()
                if last_data:
                    minus = int(data['tpostnum']) - last_data.tpostnum
                    if minus < 0:
                        minus = int(data['tpostnum'])
                    data['unum'] = minus
                else:
                    data['unum'] = 0
                
                a = timelion(fid=data['fid'], tpostnum=data['tpostnum'], tid=data['tid'], updatetime=data['updatetime'], unum = data['unum'])
                session.add(a)
                session.commit()

# 获取原来的数据
def fetch_info():
    for url in url_list:
        datas = fetch(url)
        if datas:
            for data in datas:
                a = data
                a = info(fid=data['fid'], fname=data['fname'], url=data['url'])
                session.add(a)
                session.commit()


if __name__ == "__main__":
    main()