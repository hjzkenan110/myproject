import json
from datetime import datetime

from django.http import HttpResponse
from django.shortcuts import render
from sqlalchemy import asc, func

from .test02 import session, timelion


def query_timelion(request):
    try:
        start = request.GET['start']
        end = request.GET['end']
    except:
        end = datetime.timestamp(datetime.now())
        start = datetime.timestamp(datetime.now()) - 86400

    time = request.GET['time']

    start_time = datetime.fromtimestamp(start)
    end_time = datetime.fromtimestamp(end)

    # 虎扑浏览总量, 按时间排序
    # results = session.query(timelion.fid, func.sum(timelion.unum)).filter(timelion.updatetime<now_time, timelion.updatetime>yes_time).group_by(timelion.fid).order_by(desc(func.sum(timelion.unum))).limit(50)	


    # results = session.query(timelion.fid, func.sum(timelion.unum)).filter(timelion.updatetime<now_time, timelion.updatetime>yes_time).group_by(timelion.fid).order_by(desc(func.sum(timelion.unum))).limit(50)	
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
