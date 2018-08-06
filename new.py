import requests
import time 
from lxml import etree
import fake_useragent

URL = "http://www.haoweichi.com/Others/yi_da_li_ren_shen_fen_sheng_cheng"
all = set()

def fetch():
    try:
        response = requests.get(URL)
        data = response.text
        html = etree.HTML(data)
        try:
            phone = html.xpath("/html/body/div[1]/div[3]/div[2]/div/div[2]/div[7]/div[4]/input/@value")[0]
            name = html.xpath("/html/body/div[1]/div[3]/div[2]/div/div[2]/div[2]/div[2]/input/@value")[0]
            data = str(phone)+","+str(name)
            if data in all:
                pass
            else:
                all.add(data)
                with open("f.txt", "a+", encoding='utf-8') as f:
                    print(str(phone)+","+str(name))
                    f.write(str(phone)+","+str(name)+"\n")
        except:
            print("wrong!")
    except Exception as e:
        print(e)

for i in range(0, 10000):
    time.sleep(0.5)
    fetch()