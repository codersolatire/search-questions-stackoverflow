from django.shortcuts import render
import json
import datetime
from datetime import date
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .utils import StackExchange
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

# Create your views here.

def index(request):

    # a = datetime.datetime.strptime(request.COOKIES['start_date'],'%Y-%m-%d %H:%M:%S')
    # b = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),'%Y-%m-%d %H:%M:%S')

    # difference_dates = abs(b-a).days
    
    # if difference_dates > 1 and difference_dates < 2 and int(request.COOKIES['load_count_per_day']) > 100:
    #     print('One Day Complete')
    #     return render(request,"dashboard.html",{"error":"MAX_LIMIT"})
    # elif int(request.COOKIES['load_count_per_min']) > 5 and (datetime.datetime.now().minute - int(request.COOKIES['start_time'])) == 1:
    #     print("Limit Exceed")
    #     return render(request,"dashboard.html",{"error":"TIME_EXCEED"})
    # else:
    
    obj = {}

    response = render(request,"dashboard.html",obj)

    response.set_cookie('load_count_per_min', 0)
    response.set_cookie('start_time', datetime.datetime.now().minute)
    response.set_cookie('load_count_per_day', 0)
    response.set_cookie('start_date',datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

    # return HttpResponse(json_list, "application/javascript")
    # return render(request,"dashboard.html",obj)
    return response

# def submit(request):
    question_keyword = request.POST.copy().get('questions_keyword')
    question_keyword = question_keyword.replace(',','+')

    result_json = StackExchange().fetchresults(question_keyword)
    
    # json_list = json.dumps(result_json)

    # obj = {}
    obj = json.loads(result_json)

    return render(request,"dashboard.html",obj)

    # return HttpResponse(final_res["questions"], "application/javascript")

@api_view(['POST'])
def submit(request):
    
    question_keyword = request.POST.copy().get('questions_keyword')
    questions_title = request.POST.copy().get('questions_title')

    load_count_per_min = int(request.COOKIES['load_count_per_min']) + 1
    load_count_per_day = int(request.COOKIES['load_count_per_day']) + 1

    if load_count_per_min > 5 and (datetime.datetime.now().minute - int(request.COOKIES['start_time'])) == 1:
        print("Limit Exceed")
        return render(request,"dashboard.html",{"error":"TIME_EXCEED"})
    else:
        # question_keyword = question_keyword.replace(',','+')

        parameters = {
            "site" : "stackoverflow",
            "order": "desc",
            "sort" : "activity",
            "tagged": question_keyword,
            "intitle": questions_title,
        }

        result_json = StackExchange().fetchResultStackExchange(parameters)
        obj = json.loads(result_json)

        response = render(request,"dashboard.html",obj)

        response.set_cookie('load_count_per_min',load_count_per_min)

        # return render(request,"dashboard.html",obj)
        return response