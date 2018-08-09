import time
from lxml import etree
import requests
import sqlalchemy as sa
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from datetime import datetime

from table import session, timelion, info

URL = "https://bbs.hupu.com/boards.php"

def get():
    r = requests.get(URL)
    if r.status_code == 200:
        return r.text 
    else:
        return None

def process_time(time):
    time = str(time)
    time = time[:-9]
    time = time + "00"
    time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
    return time


def parse(content):
    if content:
        millis = datetime.now()
        millis = process_time(millis)
        html = etree.HTML(content)
        html = html.xpath("//div/ul/li/span/..")
        for l in html:
            # 取url
            url = l.xpath("./a/@href")[0]
            # 今日帖子数量 
            num = l.xpath("./span")[0].text
            num = num.split("日")[1]
            num = num[:-1]

            # 查询数据
            last_data = session.query(
                timelion
            ).filter(
                timelion.url==url
            ).order_by(sa.desc(timelion.updatetime)).first()

            # 初始化设置
            if last_data:
                minus = int(num) - last_data.tpostnum
                if minus < 0:
                    minus = int(num)
                unum = minus 
            else:
                unum = 0

            # 提交到数据库
            a = timelion(url=url, tpostnum=num, unum=unum, updatetime=millis)
            session.add(a)
            session.commit()


def parse_info(content):
    if content:
        html = etree.HTML(content)
        html = html.xpath("//div/ul/li/span/..")
        for l in html:
            fname = l.xpath("./a")[0].text
            url = l.xpath("./a/@href")[0]
            infomation = info(url=url, fname=fname)
            session.add(infomation)
            session.commit()


if __name__ == "__main__":
    text = get()
    parse(text)