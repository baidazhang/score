from django import http
from django.shortcuts import render

# Create your views here.
from django.views import View
import redis

#redis配置
host = '192.168.1.102'
password = '123456'

class Score(View):
    def post(self,request):
        name = request.POST.get('name','')
        score = request.POST.get('score','')
        if not (name or score):
            return http.JsonResponse({'msg':'参数有误','code':400})
        redis_conn = redis.Redis(host=host,password=password,port=6379,db=0,decode_responses=True)
        redis_conn.lpush(name,score)
        redis_conn.sadd('names',name)
        return http.JsonResponse({'msg':'OK','code':200})

    def get(self,request):
        name = request.GET.get('name','')
        redis_conn = redis.Redis(host=host,password=password,port=6379, db=0, decode_responses=True)
        names = redis_conn.smembers('names')
        rank_dict = {}
        for i in names:
            score = redis_conn.lindex(i,0)
            rank_dict[i]=score
        rank_list = sorted(rank_dict.items(), key=lambda x: x[1], reverse=True)
        result_list = []
        for index,i in enumerate(rank_list):
            if i[0]== name:
                i_dict = {'排名':int(index)+1,'客户端':i[0],'分数':i[1],'target':True}
            else:
                i_dict ={'排名':i+1,'客户端':i[0],'分数':i[1]}
            result_list.append(i_dict)
        return http.JsonResponse({'msg':'OK','content':result_list})



