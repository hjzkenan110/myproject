import json
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from sqlalchemy import asc, desc, func
from sqlalchemy.orm import aliased

from .table import info, timelion
from .db import get_session

BASE_URL = "https://bbs.hupu.com"
# 查询总量
def increase_timelion(request):
    
    try:
        start = request.GET['start']
        end = request.GET['end']
    except:
        end = datetime.timestamp(datetime.now())
        start = datetime.timestamp(datetime.now()) - 86400

    start_time = datetime.fromtimestamp(start)
    end_time = datetime.fromtimestamp(end)

    sum = func.sum(timelion.tpostnum)

    session = get_session()
    results = session.query(
        timelion.updatetime, sum
    ).filter(
        #timelion.updatetime<end_time, 
        #timelion.updatetime>start_time,
    ).group_by(timelion.updatetime).order_by(desc(timelion.updatetime)).all()

    session.close()

    response = {}
    response["data"] = []

    for result in results:
        tmp = {"tpostnum": int(result[1]), 'updatetime': str(result[0])}
        response["data"].append(tmp)

    # 队列翻转
    response["data"].reverse()
    return HttpResponse(json.dumps(response), content_type="application/json")

def process_time(time, choice):
    if choice == "seconde":
        zero = -9
        pattern = "%Y-%m-%d %H:%M"
    elif choice == "minute":
        zero = -12
        pattern = "%Y-%m-%d %H"
    elif choice == "hour":
        zero = -15
        pattern = "%Y-%m-%d "

    time = str(time)
    time = time[:zero]
    time = datetime.strptime(time, pattern)
    return time

# 查询当天帖量排名
def tpostnum_rank(request):
    try:
        ty = request.GET['type']
    except:
        ty = "top8"

    if ty == "others":
        limit = ".limit(10)"
    elif ty == "all":
        limit = ".all()"
    elif ty == "top8":
        limit = ".limit(8)"

    millis = datetime.now()
    millis = process_time(millis, choice="hour")
    
    start_time = millis
    end_time = datetime.now()

    maxtpostnum = func.max(timelion.tpostnum) 

    session = get_session()
    results_str = "session.query(\
        info.fname, timelion.url, maxtpostnum\
    ).filter(\
        info.url==timelion.url,\
    ).group_by(timelion.url).order_by(desc(maxtpostnum))" + limit
    #timelion.updatetime<end_time, \
    #timelion.updatetime>start_time,\



    results = eval(results_str)
    session.close()

    response = {}
    response["data"] = []

    he = 0
    for result in results:
        tmp = {"fname": result[0], "url": BASE_URL + result[1], "tpostnum": int(result[2])}
        he = int(result[2]) + he
        response["data"].append(tmp)

    if ty == "others":
        session = get_session()
        all_tpostnum = session.query(
            func.sum(timelion.tpostnum)
        ).group_by(timelion.updatetime).order_by(desc(timelion.updatetime)).limit(1)
        session.close()
        others = int(all_tpostnum[0][0])
        others = others - he
        response["data"].append({"fname": "others", "tpostnum": others})

    return HttpResponse(json.dumps(response), content_type="application/json")

# SELECT 
# fname, info.url, max(tpostnum),updatetime 
# from 
# timelion ,info
# WHERE
# info.url = timelion.url
# GROUP BY 
# timelion.url
# ORDER BY 
# max(tpostnum) desc

def series_timelion(request):
    try:
        start = request.GET['start']
        end = request.GET['end']
        url = request.GET['url']
    except:
        end = datetime.timestamp(datetime.now())
        start = datetime.timestamp(datetime.now()) - 86400

    start_time = datetime.fromtimestamp(start)
    end_time = datetime.fromtimestamp(end)

    # sum = func.sum(timelion.unum)
    # session = get_session()
    # results = session.query(
    #     info.fname, timelion.url, sum, timelion.updatetime
    # ).filter(
    #     #timelion.updatetime<end_time, 
    #     #timelion.updatetime>start_time,
    #     timelion.url==url,
    #     info.url==url
    # ).group_by(timelion.fid).order_by(asc(func.sum(timelion.updatetime))).limit(50)	

    # ---------------------------------------------------------

    month = func.extract('month', timelion.updatetime).label('month')
    day = func.extract('day', timelion.updatetime).label('day')
    hour = func.extract('hour', timelion.updatetime).label('hour')
    unum = func.sum(timelion.unum)

    #c按小时来分类
    session = get_session()
    results = session.query(
            timelion.url, 
            timelion.updatetime, 
            month, 
            day, 
            hour, 
            unum
        ).group_by('hour', 'day').filter(
            timelion.url == "/2",
            #timelion.updatetime<end_time, 
            #timelion.updatetime>start_time
        ).order_by(asc(timelion.updatetime)).limit(50)

    # response = {}
    # response["data"] = []

    # for result in results:
    #     time = str(result[1])[:-6]+":00:00"
    #     tmp = {"fid": result[0], 'updatetime': time, "unum": int(result[5])}
    #     response["data"].append(tmp)


    # 取出所有数据
    # results = session.query(
    #         timelion.updatetime, 
    #         timelion.unum
    #     ).filter(
    #         timelion.fid == "1048", 
    #     ).order_by(asc(timelion.updatetime)).limit(50)	
    session.close()
    response = {}
    response["data"] = []

    for result in results:
        tmp = {'updatetime': str(result[1]), "unum": int(result[5])}
        response["data"].append(tmp)

    return HttpResponse(json.dumps(response), content_type="application/json")
