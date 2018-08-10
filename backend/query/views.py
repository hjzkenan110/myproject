import json
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from sqlalchemy import asc, func, desc

from .table import session, timelion, info

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

    results = session.query(
        timelion.updatetime, sum
    ).filter(
        timelion.updatetime<end_time, 
        timelion.updatetime>start_time,
    ).group_by(timelion.updatetime).order_by(timelion.updatetime).all()

    response = {}
    response["data"] = []

    for result in results:
        tmp = {"fid": result[0], 'updatetime': str(result[0])}
        response["data"].append(tmp)


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

    sum = func.sum(timelion.unum)

    results = session.query(
        info.fname, timelion.url, sum, timelion.updatetime
    ).filter(
        timelion.updatetime<end_time, 
        timelion.updatetime>start_time,
        timelion.url==url,
        info.url==url
    ).group_by(timelion.fid).order_by(desc(func.sum(timelion.updatetime))).all(50)	
    # month = func.extract('month', timelion.updatetime).label('month')
    # day = func.extract('day', timelion.updatetime).label('day')
    # hour = func.extract('hour', timelion.updatetime).label('hour')
    # unum = func.sum(timelion.unum)

    #按小时来分类
    # results = session.query(
    #         timelion.fid, 
    #         timelion.updatetime, 
    #         month, 
    #         day, 
    #         hour, 
    #         unum
    #     ).group_by('hour', 'day').filter(timelion.fid == "34",timelion.updatetime<end_time, timelion.updatetime>start_time).all()

    # response = {}
    # response["data"] = []

    # for result in results:
    #     time = str(result[1])[:-6]+":00:00"
    #     tmp = {"fid": result[0], 'updatetime': time, "unum": int(result[5])}
    #     response["data"].append(tmp)


    # 取出所有数据
    results = session.query(
            timelion.updatetime, 
            timelion.unum
        ).filter(
            timelion.fid == "1048", 
        ).order_by(asc(timelion.updatetime)).limit(50)	

    response = {}
    response["data"] = []

    for result in results:
        tmp = {'updatetime': str(result[0]), "unum": int(result[1])}
        response["data"].append(tmp)

    return HttpResponse(json.dumps(response), content_type="application/json")
