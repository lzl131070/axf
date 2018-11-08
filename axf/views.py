import hashlib
import os
import random
import time
import uuid

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import _md5
# Create your views here.
from AXF import settings
from axf.models import Goods, Wheel, Mainshow, Mustbuy, Foodtypes, Nav, Shop, User, Cart


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


def market(request,categoryid,childid,sort):    # 闪购超市

    token = request.COOKIES.get('token')
    user = User.objects.filter(token=token).first()
    cart = Cart.objects.filter(userid=user)




    foodtypes = Foodtypes.objects.all()
    # typeid=foodtypes.filter(typeid=categoryid).first()
    # categoryid = foodtypes[int(categoryid)].typeid
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
    # childid = listbounce[int(childid)]['childnum']
    if childid=='0':
        goods=Goods.objects.filter(categoryid=categoryid)
    else:
        goods=Goods.objects.filter(categoryid=categoryid).filter(childcid=childid)

    if sort == '0':
        pass
    elif sort == '1':

        goods = goods.order_by('-productnum')
    elif sort == '2':
        goods = goods.order_by('price')
    elif sort == '3':
        goods = goods.order_by('-price')

    data={
        'foodtypes': foodtypes,
        'goods':goods,
        'listbounce':listbounce,
        'categoryid':categoryid,
        'childid':childid,
        'sort':sort,
        'cart':cart
    }
    # response = redirect('axf:market')
    # response.delete_cookie('cartext')
    # catsort = request.COOKIES.get('cartext')

    return render(request, 'market/market.html',context=data)


def cart(request):  # 购物车
    token = request.COOKIES.get('token')
    if token:
        user = User.objects.get(token=token)
        carts = Cart.objects.filter(userid=user).exclude(num=0)

        return render(request,'cart/cart.html',context={'carts':carts})
    else:
        return render(request,'mine/login.html')

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



def addcart(request):
    token = request.COOKIES.get('token')
    goodid = request.GET.get('goodid')
    print(goodid)
    print('test+++++')
    Jsondata={
        'goodid':goodid,
    }
    if token:
        Jsondata['status']=1
        user = User.objects.get(token=token)
        good = Goods.objects.get(pk=goodid)
        cart = Cart.objects.filter(userid=user).filter(goodid=good)
        if cart.exists():
            cart = cart.first()
            cart.num += 1
            Jsondata['num'] = cart.num
            cart.save()
        else:
            cart = Cart()
            cart.userid = user
            cart.goodid = good
            cart.num = 1
            Jsondata['num'] = cart.num
            cart.save()

    else:
        Jsondata['status']=-1

    return JsonResponse(Jsondata)


def reduce(request):
    token = request.COOKIES.get('token')
    user = User.objects.get(token=token)
    goodid = request.GET.get('goodid')
    cart = Cart.objects.get(goodid=goodid,userid=user)
    cart.num-=1
    cart.save()
    print('test-----')
    Jsondata = {
        'goodid':goodid,
        'num':cart.num
    }

    return JsonResponse(Jsondata)

def checkone(request):
    token = request.COOKIES.get('token')
    user = User.objects.get(token=token)
    cartid = request.GET.get('isid')
    cart = Cart.objects.get(pk=cartid,userid=user)
    print(cart.isselect)
    cart.isselect = not cart.isselect
    cart.save()
    data={
        'isselect':cart.isselect,
        'status':1,

    }

    return JsonResponse(data)


def checkall(request):
    token = request.COOKIES.get('token')
    user = User.objects.get(token=token)
    isselect = request.GET.get('isall')
    if isselect=='true':
        isselect = True
    else:
        isselect=False
    print(isselect)
    carts = Cart.objects.filter(userid=user)
    for cart in carts:
        cart.isselect = isselect
        cart.save()
    data={
        'isselect':isselect,
        'status':1,

    }
    return JsonResponse(data)

