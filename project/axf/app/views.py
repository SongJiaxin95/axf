from datetime import datetime, timedelta

from django.core import serializers
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password, check_password
from django.core.urlresolvers import reverse
# Create your views here.
# from rest_framework import mixins, viewsets

from app.models import MainWheel, MainNav, MainHotGoods, MainShop, Goods, MainShow, UserModel, FoodType, \
    UserTicketModel, CarModel, OrderModel,OrderGoodsModel
from utils.functions import get_ticket


def Home(request):
    # shops = MainShop.objects.all()
    date = {'wheels': MainWheel.objects.all(),
            'navs': MainNav.objects.all(),
            'hotgoods': MainHotGoods.objects.all(),
            'shops': MainShop.objects.all(),
            # 'shop1': shops[0],
            # 'shop2to3': shops[1:3],
            # 'shop4to7': shops[3:7],
            # 'shop8to11': shops[7:11],
            'mainshows': MainShow.objects.all()}
    return render(request, 'home/home.html',date)

def MarketType(request):
    if request.method == 'GET':
        typeid = request.GET.get('typeid')
        goods = Goods.objects.filter(categoryid=typeid)
        goods = serializers.serialize('json',goods)
        foodtype_id = FoodType.objects.get(typeid=typeid).id
        childtypenames = FoodType.objects.get(id=foodtype_id).childtypenames
        childtypelist = childtypenames.split('#')
        childtypenamelist = []
        for val in childtypelist:
            mylist = val.split(':')
            childtypenamelist.append(mylist)
        data = {
            'childtypenames': childtypenamelist,
            'goods': goods,
        }
        return JsonResponse(data)

def Market_ChildType_Order(request):
    if request.method == 'GET':
        typeid = request.GET.get('typeid')
        childcid = request.GET.get('childcid')
        order = request.GET.get('order')
        goods = Goods.objects.filter(categoryid=typeid)
        if childcid and childcid != '0':
            goods = goods.filter(childcid=childcid)
        if order == '1':
            goods = goods.order_by('id')
        elif order == '2':
            goods = goods.order_by('productnum')
        elif order == '3':
            goods = goods.order_by('-price')
        elif order == '4':
            goods = goods.order_by('price')
        goods = serializers.serialize('json', goods)
        data = {
            'goods': goods
        }
        return JsonResponse(data)

# 闪购
def Market(request):
    goods = Goods.objects.filter(categoryid=104749)
    childtypenamelist = ['全部分类','0']
    date = {
        'foodtypes': FoodType.objects.all(),
        'goods': goods,
        'childtypenames': childtypenamelist,
    }
    return render(request, 'market/market.html', date)

# 购物车
def Cart(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            cars = CarModel.objects.filter(user=user)
            total = calcTotal(user)
            return render(request, 'cart/cart.html', {'cars':cars, 'total':total})
        else:
            return HttpResponseRedirect(reverse('axf:login'))

# 用户选中与取消选中
def user_chang_select(request):
    if request.method == 'POST':
        goods_id = request.POST.get('goods_id')
        user = request.user
        data = {
            'msg': '请求成功',
            'code': '200'
        }
        if user and user.id:
            cart = CarModel.objects.filter(goods_id=goods_id,user=user).first()
            if cart.is_select:
                cart.is_select = False
            else:
                cart.is_select = True
            cart.save()
            data['is_select'] = cart.is_select
            data['total'] = calcTotal(user)
        return JsonResponse(data)


# 我的
def Mine(request):
    if request.method == 'GET':
        user = request.user
        data = {}
        if user and user.id:
            orders = user.ordermodel_set.all()
            wait_pay, payed = 0, 0
            for order in orders:
                if order.o_status == 0:
                    wait_pay += 1
                elif order.o_status == 1:
                    payed += 1
            data['wait_pay'] = wait_pay
            data['payed'] = payed
        return render(request, 'mine/mine.html',data)


def Login(request):
    if request.method == 'GET':
        return render(request, 'user/user_login.html')
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        if UserModel.objects.filter(username=name).exists():
            user = UserModel.objects.get(username=name)
            if check_password(password, user.password):
                response = HttpResponseRedirect('/axf/home/')
                ticket = get_ticket()
                out_time = datetime.now() + timedelta(days=1)
                response.set_cookie('ticket', ticket, expires=out_time)
                UserTicketModel.objects.create(
                    user=user,
                    ticket=ticket,
                    out_time=out_time
                )
                # user.ticket = ticket
                # user.save()
                return response
            else:
                return render(request, 'user/user_login.html', {'password': '用户名或密码错误'})
        else:
            return render(request, 'user/user_login.html', {'name': '用户不存在'})


def Logout(request):
    if request.method == 'GET':
        response = HttpResponseRedirect('/axf/home/')
        response.delete_cookie('ticket')
        ticket = request.COOKIES.get('ticket')
        userticket = UserTicketModel.objects.filter(ticket=ticket)
        userticket.delete()
        return response


def Register(request):
    if request.method == 'GET':
        return render(request, 'user/user_register.html')
    if request.method == 'POST':
        name = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        icon = request.FILES.get('icon')
        password = make_password(password)
        UserModel.objects.create(username=name, password=password,
                                 email=email, icon=icon
                                 )
        return HttpResponseRedirect('/axf/login/')

# class CartEdit(mixins.ListModelMixin,
#                   mixins.RetrieveModelMixin,
#                   mixins.UpdateModelMixin,
#                   mixins.DestroyModelMixin,
#                   mixins.CreateModelMixin,
#                   viewsets.GenericViewSet):
#
#     # 查询所有信息
#     queryset = CarModel.objects.all()
#     # 序列化
#     serializer_class = CarSerializer
#     # 过滤
#     filter_class = CarFilter

#
#  总计
def calcTotal(user):
    cars = CarModel.objects.filter(user=user)
    total = 0
    for val in cars:
        if val.is_select:
            total += (val.goods.price * val.c_num)
    total = float('%.2f' % total)
    return total

# 添加商品到购物车
def add_goods(request):
    if request.method == 'POST':
        data = {
            'msg': '请求成功',
            'code': '200'
        }
        user = request.user
        if user and user.id:
            goods_id = request.POST.get('goods_id')
            # 获取购物车信息
            user_carts = CarModel.objects.filter(user=user, goods_id=goods_id).first()
            if user_carts:
                user_carts.c_num += 1
                user_carts.save()
                data['c_num'] = user_carts.c_num
            else:
                CarModel.objects.create(goods_id=goods_id, user=user,c_num=1)
                data['c_num'] = 1
            data['total'] = calcTotal(user)
        return JsonResponse(data)

# 从购物车中删除商品
def sub_goods(request):
    if request.method == 'POST':
        data = {
            'msg':'请求成功',
            'code':'200'
        }
        user = request.user
        goods_id = request.POST.get('goods_id')
        if user and user.id:
            # 获取购物车信息
            user_carts = CarModel.objects.filter(user=user, goods_id=goods_id).first()
            if user_carts:
                if user_carts.c_num == 1:
                    user_carts.delete()
                    data['c_num'] = 0
                else:
                    user_carts.c_num -= 1
                    user_carts.save()
                    data['c_num'] = user_carts.c_num
            data['total'] = calcTotal(user)
        return JsonResponse(data)

def user_chang_selectAll(request):
    if request.method == 'POST':
        user = request.user
        data = {
            'msg': '请求成功',
            'code': '200'
        }
        if user and user.id:
            carts = CarModel.objects.filter(user=user)
            if request.POST.get('is_selectall')=='√':
                for i in carts:
                    i.is_select = False
                    i.save()
            else:
                for j in carts:
                    j.is_select = True
                    j.save()
            data['total'] = calcTotal(user)
        return JsonResponse(data)

def user_generate_order(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            carts_goods = CarModel.objects.filter(is_select=True,user=user)
            order = OrderModel.objects.create(user=user,o_status=0)
            for carts in carts_goods:
                OrderGoodsModel.objects.create(
                    goods=carts.goods,order=order,good_num=carts.c_num)
                carts.delete()
            # carts_goods.delete()
            return HttpResponseRedirect(reverse('axf:user_pay_order',args=(order.id,)))


def user_pay_order(request, order_id):
    if request.method == 'GET':
        orders = OrderModel.objects.filter(pk=order_id).first()
        data = {
            'order_id': order_id,
            'orders': orders
        }
        return render(request,'order/order_info.html',data)

def order_pay(request,order_id):
    if request.method == 'GET':
        OrderModel.objects.filter(pk=order_id).update(o_status=1)
        return HttpResponseRedirect(reverse('axf:mine'))

def order_wait_pay(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            orders = OrderModel.objects.filter(user=user,o_status=0)

            return render(request,'order/order_list_wait_pay.html',{'orders':orders})

def order_wait_shouhuo(request):
    if request.method == 'GET':
        user = request.user
        if user and user.id:
            orders = OrderModel.objects.filter(user=user,o_status=1)

            return render(request, 'order/order_list_payed.html', {'orders': orders})