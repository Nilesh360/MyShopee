from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from chatbot.user_services import getUsers,saveUser,toggle_online,cacheDataBackend
import threading
from django.core.cache import cache
import json
import string
import random
from base.views import login

# Create your views here.

def home(request):
    toggle_online(request,'online')
    room_name = None
    connect_request_user = None 
    if request.user.is_authenticated:
        cache_obj = cacheDataBackend()
        cache_data = cache_obj.getter(request.user.id)
        if cache_data:
            room_name = cache_data['room_name']
            connect_request_userid=cache_data['connect_request_userid']
            connect_request_user = User.objects.get(id=connect_request_userid)
    context={'room_name':room_name,'connect_request_user':connect_request_user}
    return render(request,'chatbot/home.html',context)



@login_required(login_url='login')
def sendUserChatRequest(request,pk):
    passed_user = User.objects.get(id=pk)
    room_name=''.join(random.choices(string.ascii_uppercase +string.digits, k=9)) # 9 length room_name
    data = {
    'connect_receiver_userid': str(pk),
    'connect_request_userid': str(request.user.id),
    'room_name':room_name
    }
    cache_obj = cacheDataBackend()
    cache_obj.setter(pk,data)
     
    context={'passed_user':passed_user,'room_name': room_name}
    return render(request,'chatbot/chatroom.html',context)


@login_required(login_url='login')
def getRoom(request):
    cache_obj = cacheDataBackend()
    cache_data = cache_obj.getter(request.user.id)
    passed_user=None
    room_name = None
    if cache_data:
        connect_request_userid=cache_data['connect_request_userid']
        passed_user = User.objects.get(id=connect_request_userid)
        room_name = cache_data['room_name']

    cache_obj.delete(request.user.id)
    context={'passed_user':passed_user,'room_name': room_name}
    return render(request, 'chatbot/chatroom.html', context)



@login_required(login_url='login')
def displayUser(request):
    users = User.objects.all()
    context = {'users':users}
    return render(request,'chatbot/Interest.html',context)

