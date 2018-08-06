from django.shortcuts import render
import json
from .test02 import timelion, session

from django.http import HttpResponse
import datetime
from sqlalchemy import func, desc


def index(request):
    return HttpResponse(u"欢迎光临 自强学堂!")

def query_timelion(request):
    now_time = datetime.datetime.now()
    yes_time = now_time + datetime.timedelta(days=-1)

    # start = request.GET['start']
    # end = request.GET['end']
    results = session.query(timelion.fid, func.sum(timelion.unum)).filter(timelion.updatetime<now_time, timelion.updatetime>yes_time).group_by(timelion.fid).order_by(desc(func.sum(timelion.unum))).limit(50)	
    response = {}
    response["data"] = []

    for result in results:
        response["data"].append({"fid": result[0], "unum": str(result[1])})
    
    return HttpResponse(json.dumps(response), content_type="application/json")