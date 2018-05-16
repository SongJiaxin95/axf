from django.conf.urls import url
from app import views
from rest_framework.routers import SimpleRouter

# router = SimpleRouter()
# router.register(r'^cart', views.CartEdit)
urlpatterns = [
    url(r'home/',views.Home,name='home'),
    url(r'market/',views.Market,name='market'),
    # 闪购分类
    url(r'markettype/',views.MarketType,name='markettype'),
    url(r'market_childtype_order/',views.Market_ChildType_Order,name='market_childtype_order'),
    # 购物车
    url(r'cart/',views.Cart,name='cart'),
    # 个人中心
    url(r'mine/',views.Mine,name='mine'),
    # 登录
    url(r'login/',views.Login,name='login'),
    # 退出
    url(r'logout/',views.Logout,name='logout'),
    # 注册
    url(r'register/',views.Register,name='register'),
    # 添加商品到购物车
    url(r'addgoods/',views.add_goods,name='addgoods'),
    url(r'subgoods/',views.sub_goods,name='subgoods'),
    # 修改购物车商品的选择
    url(r'changecartselect/',views.user_chang_select,name='change_select'),
    url(r'changecartselectall/',views.user_chang_selectAll,name='change_selectall'),
    # 下单
    url(r'generateorder/',views.user_generate_order,name='user_generate_order'),
    # 付款
    url(r'payorder/(\d+)/',views.user_pay_order,name='user_pay_order'),
    url(r'orderpayed/(\d+)/',views.order_pay,name='order_pay'),
    url(r'orderWaitPay/',views.order_wait_pay,name='order_wait_pay'),
    url(r'orderlistpayed/',views.order_wait_shouhuo,name='order_wait_shouhuo'),
]
# urlpatterns += router.urls