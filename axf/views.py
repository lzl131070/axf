import hashlib
import os
import random
import time
import uuid

from django.http import HttpResponse
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


def market(request,categoryid):    # 闪购超市
    foodtypes = Foodtypes.objects.all()
    # typeid=foodtypes.filter(typeid=categoryid).first()
    foodtype = foodtypes.filter(typeid=categoryid)[0]
    strid = foodtype.childtypenames
    listname = strid.split('#')
    listbounce = []
    for i in listname:
        iList=i.split(":")
        dirt={
            'childname':iList[0],
            'childnum':iList[1]
        }
        listbounce.append(dirt)
    goods=Goods.objects.filter(categoryid=categoryid)
    data={
        'foodtypes': foodtypes,
        'goods':goods,
        'listbounce':listbounce,
    }
    return render(request, 'market/market.html',context=data)


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
        return render(request, 'mine/register.html')
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
            num = 1
            response = redirect('axf:register')
            return render(request, 'mine/register.html', context={'num':num})
            # return response

def login(request):
    if request.method=='GET':
        return render(request,'mine/login.html')
    elif request.method=='POST':
        account = request.POST.get('account')
        users=User.objects.filter(account=account)
        password = get_pswd(request.POST.get('password'))
        if users.exists():
            users.filter(password=password)
            if users.exists():
                user=users.first()
                response=redirect('axf:mine')
                response.set_cookie('token',user.token)
                return response
            else:
                return HttpResponse('密码错误')
        else:
            return HttpResponse('账号不存在')
def logout(request):
    response = redirect('axf:mine')
    response.delete_cookie('token')
    return response
