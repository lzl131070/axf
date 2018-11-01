import hashlib
import os
import random
import time
import uuid

from django.shortcuts import render, redirect
import _md5
# Create your views here.
from AXF import settings
from axf.models import Goods, Wheel, Mainshow, Mustbuy, Foodtypes, Nav, Shop, User


def home(request):  # 首页
    navs=Nav.objects.all()
    wheels=Wheel.objects.all()
    mustbuys=Mustbuy.objects.all()
    shops=Shop.objects.all()
    mainshows=Mainshow.objects.all()
    data={
        'navs': navs,
        'wheels': wheels,
        'mustbuys':mustbuys,
        'shops':shops,
        'mainshows':mainshows,
    }
    return render(request, 'home/home.html',context=data)


def market(request):    # 闪购超市
    return render(request, 'market/market.html')


def cart(request):  # 购物车
    return render(request,'cart/cart.html')


def mine(request):  # 我的
    token = request.COOKIES.get('token')
    users = User.objects.filter(token=token)
    data = {

    }
    if users.exists():
        user= users.first()
        data['user']=user

    return render(request,'mine/mine.html',context=data)
def get_pswd(pswd):
    sha = hashlib.md5()
    sha.update(pswd.encode('utf-8'))
    return sha.hexdigest()
def get_token():
    token = str(time.time())+str(random.random)
    md5 = hashlib.md5()
    md5.update(token.encode('utf-8'))
    return md5.hexdigest()
def register(request):
    if request.method=='GET':
        return render(request,'register.html')
    elif request.method=='POST':
        user=User()
        user.account = request.POST.get('account')
        user.password = get_pswd(request.POST.get('password'))
        user.token=str(uuid.uuid5(uuid.uuid4(),'register'))
        user.adv = request.POST.get('address')
        user.tel = request.POST.get('tel')
        user.name = request.POST.get('name')
        file = request.FILES.get('file')
        filename = str(random.randrange(100))+ '-' + file.name
        filepath = os.path.join(settings.MEDIA_ROOT,filename)
        with open(filepath,'wb') as fp:
            for i in file.chunks():
                fp.write(i)
        user.img = filepath.split('AXF')[1]
        try:
            user.save()
            response = redirect('axf:mine')
            response.set_cookie('token',user.token)
            return response
        except:
            # num = 1
            response = redirect('axf:register')
            return render(request,'register.html',context={'num':num})
            # return response


def logout(request):
    response = redirect('axf:mine')
    response.delete_cookie('token')
    return response