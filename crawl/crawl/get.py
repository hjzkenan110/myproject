import asyncio
import aiohttp
import json
from urllib.parse import urlencode, urljoin
import requests
import time
import redis
import celery

KEY_WORD = "佳能 50"
URL = "https://s.2.taobao.com/list/waterfall/waterfall.htm"
params = {
    "q" : KEY_WORD,
    "_input_charset" : "utf8"
}

def count_page(url):
    res = requests.get(url)
    body = res.text
    body = body[4:-2]
    j = json.loads(body)
    return j['totalPage']

# 获取列表页的json
async def get_liebiao(url):
    print(url)
    async with aiohttp.ClientSession() as client:
        async with client.get(url) as response:
            body = await response.text()
            body = body[4:-2]
            parser(body)

def parser(html):
    try:
        j = json.loads(html)
        get_url(j["idle"])
    except Exception as e:
        print(html)
        print(e)
    

def get_url(items_list):
    for item in items_list:
        j = item['item']['itemUrl']
        pass
    
def main():
    # start_time = time.time()
    testurl = URL + "?{}".format(urlencode(params))
    count = int(count_page(testurl))

    # 从json里最多只能拿100页
    count = 100 if count > 100 else count

    # tasks = [get_]
    #loop = asyncio.get_event_loop()
    url_list = []
    for i in range(1, count + 1):
        params["wp"] = i
        url_list.append(URL + "?{}".format(urlencode(params)))
    
    return url_list
    # tasks = [get_liebiao(url) for url in url_list]
    # loop.run_until_complete(asyncio.wait(tasks))