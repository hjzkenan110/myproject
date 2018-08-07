import asyncio
import json
import time
from asyncio import Queue
from urllib.parse import urlencode, urljoin

import aiohttp
import celery
import redis
import requests
from fake_useragent import UserAgent
from lxml import etree
from requests.cookies import RequestsCookieJar
from requests.utils import dict_from_cookiejar

headers = {'Accept': 'text/html, application/xhtml+xml, image/jxr, */*',
            'Accept - Encoding':'gzip, deflate',
           'Accept-Language':'zh-Hans-CN, zh-Hans; q=0.5',
           'Connection':'Keep-Alive',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'}

headers = {
    ":authority": "2.taobao.com",
    ":method": "GET",
    ":path": "/item.htm?id=573553154318&from=list&similarUrl=",
    ":scheme": "https",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "upgrade-insecure-requests": 1,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"
}

# from workers import app
all = set()
KEY_WORD = "七工匠 50"
URL = "https://s.2.taobao.com/list/waterfall/waterfall.htm"
params = {
    "q" : KEY_WORD,
    "_input_charset" : "utf8",
    "start" : 100,
    "end" : 500
}

# 获得页数
def count_page(url):
    res = requests.get(url)
    body = res.text
    body = body[4:-2]
    j = json.loads(body)
    return j['totalPage']


# 获得返回的cookies
def get_cookies(url):
    session = requests.session()
    r = session.get(url, headers=headers)
    print(r.text())
    cookies = dict_from_cookiejar(session.cookies)
    with open("cook.txt", "w") as fp:
        json.dump(cookies, fp)


# 获得每个列表页的url
def get_page_list():
    testurl = URL + "?{}".format(urlencode(params))
    count = int(count_page(testurl))

    # 从json里最多只能拿100页
    count = 100 if count > 100 else count

    liebiao_list = []
    for i in range(1, count + 1):
        params["wp"] = i
        liebiao_list.append(URL + "?{}".format(urlencode(params)))
    
    return liebiao_list


# 获取列表页的json
async def get_liebiao(url):

    global all
    result = []

    body = await fetch(url)
    if body:
        html = body[4:-2]

    try:
        j = json.loads(html)
        item_urls = get_detail_list(j["idle"])

        for item_url in item_urls:
            url = "https:" + item_url
            # 去重
            if url in all:
                pass
            else:
                all.add(url)
                result.append(url)
        
        return result
        
    except Exception as e:
        print(e)

# 从json中加载每一页的item url
def get_detail_list(items_list):
    
    items_urls = set()

    for item in items_list:
        j = item['item']['itemUrl']
        items_urls.add(j)

    return items_urls


async def producer(q, num_workers):
    page_list = get_page_list()
    get_cookies("https://2.taobao.com/item.htm?id=573553154318")
    for url in page_list:
        detail_lists = await get_liebiao(url)
        for i in detail_lists:
            await q.put(i)
            print('producer: added url {} to the queue'.format(i))
        # Add None entries in the queue
        # to signal the consumers to exit
        print('producer: adding stop signals to the queue')
        for i in range(num_workers):
            await q.put(None)
        print('producer: waiting for queue to empty')
        await q.join()
        print('producer: ending')


async def consumer(n, q):
    print('consumer {}: starting'.format(n))
    while True:
        print('consumer {}: waiting for url'.format(n))
        url = await q.get()
        print('consumer {}: has url {}'.format(n, url))
        if url is None:
            # None is the signal to stop.
            q.task_done()
            break
        else:
            html = await fetch(url)
            a = etree.HTML(html)
            title = a.xpath("//*[@id=\"J_Property\"]/h1")[0]
            print(title)
            q.task_done()
    print('consumer {}: ending'.format(n))
 

async def main(loop, num_consumers):
    # Create the queue with a fixed size so the producer
    # will block until the consumers pull some items out.

    print('Crawl: starting')
    q = asyncio.Queue(maxsize=num_consumers)
 
    # Scheduled the consumer tasks.
    consumers = [
        loop.create_task(consumer(i, q))
        for i in range(num_consumers)
    ]
    
    # Schedule the producer task.
    prod = loop.create_task(producer(q, num_consumers))
 
    # Wait for all of the coroutines to finish.
    await asyncio.wait(consumers + [prod])


async def fetch(url, headers=None):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status in [200, 201]:
                data = await response.text()
                return data
            return None
        return None


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main(loop, 10))
    finally:
        loop.close()
