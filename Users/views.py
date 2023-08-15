from django.shortcuts import render
from .serializer import UserSerializer
from .models import *
from django.http import JsonResponse, HttpResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache

from rest_framework import viewsets ,status
from rest_framework.response import Response
import redis




class UserViewset(viewsets.ViewSet):

    def get(self,request):
        if cache.get("all_user"):
            serializer=cache.get("all_user")
        else:
            all_user=UserInfo.objects.all()
            serializer=UserSerializer(all_user,many=True)
            cache.set("all_user",serializer.data,24*60*60)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

    def update(self,request,id=None):
        if cache.get(id):
            return Response("Record Currently Updated by other user")
        else:
            cache.set(id,request.user,30)
            user=UserInfo.objects.get(id=id)
            serializer=UserSerializer(instance=user,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            value=cache.get(id)
            if value==request.user:
                cache.delete(id)
        return Response(serializer.data)
    

    def remove(self,request,id=None):
        if cache.get(id):
            return Response("Record Currently deleted by other user")
        else:
            cache.set(id,request.user,30)
            user=UserInfo.objects.get(id=id)
            user.delete()
            value=cache.get(id)
            if value==request.user:
                cache.delete(id)
        return Response("Delete Successfully")
    
    def search_user(self,request,email=None):
        schema = (
        TextField("$.firstname", as_name="firstname"),
        TextField("$.lastname", as_name="lastname"),
        TextField("$.email", as_name="email"),
        TextField("$.phone", as_name="phone"),
        )
        index=cache.ft("idx:user")
        index.create_index(schema,definition=IndexDefinition(prefix=["user:"],index_type=IndexType.JSON),)
        all_users=UserInfo.objects.all()
        for idx,user in enumerate(all_users):
            cache.set(f"user:{idx}",user)

        res=index.search(Query("*"))
        print("Users Founds :", res.total)





# Create your views here.


# @csrf_exempt
# def list_users(request):
#     if request.method == "GET":
#         items={}
#         for key in cache.keys("*"):
#             items[key.decode("utf-8")]=cache.get(key)
#         users = UserInfo.objects.all()
#         users_serilizers = UserSerializer(users, many=True)
#         return JsonResponse(users_serilizers.data, safe=False)

#     elif request.method == "POST":
#         print(request)
#         data = JSONParser().parse(request)
#         serializer = UserSerializer(data=data)
#         if serializer.is_valid():
#             serializer.save()
#             cache.set(serializer.id,serializer,24*60*60)
#             return JsonResponse(serializer.data, status=201)
#         return JsonResponse(serializer.errors, data=400)


# @csrf_exempt
# def retrieve_user(request, pk):
#     if cache.get(pk):
#         user_serializer=cache.get(pk)
#     else:
#         try:
#             user = UserInfo.objects.get(pk=pk)
#             user_serializer = UserSerializer(user)
#             cache.set(user_serializer.id,user_serializer,24*60*60)
#         except UserInfo.DoesNotExist:
#             return HttpResponse("User Doesn't exist",status=404)

#     if request.method == "GET":
#         return JsonResponse(user_serializer.data)
#     elif request.method == "PUT":
#         data = JSONParser().parse(request)
#         serializer = UserSerializer(user, data=data)
#         if serializer.is_valid():
#             serializer.save()
#             cache.set(serializer.id,serializer,24*60*60)
#             return JsonResponse(serializer.data)
#         return JsonResponse(serializer.errors, status=400)

#     elif request.method == "DELETE":
#         cache.delete(pk)
#         user = UserInfo.objects.get(pk=pk)
#         user.delete()
#         return HttpResponse("Item Delete Successfully",status=204)
