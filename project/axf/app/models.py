from django.db import models

# Create your models here.

class Main(models.Model):
    img = models.CharField(max_length=200)  # 图片
    name = models.CharField(max_length=100)  # 名称
    trackid = models.CharField(max_length=16)  # id

    class Meta:
        abstract = True

class MainWheel(Main):
    class Meta:
        db_table = 'axf_wheel'

class MainNav(Main):
    class Meta:
        db_table = 'axf_nav'

class MainHotGoods(Main):
    class Meta:
        db_table = 'axf_hotgoods'

class MainShop(Main):
    class Meta:
        db_table = 'axf_shop'

class MainShow(Main):
    categoryid = models.CharField(max_length=16,null=True)
    brandname = models.CharField(max_length=100,null=True)
    img1 = models.CharField(max_length=200)
    childcid1 = models.CharField(max_length=16,null=True)
    productid1 = models.CharField(max_length=16,null=True)
    longname1 = models.CharField(max_length=100)
    price1 = models.FloatField(default=0)
    marketprice1 = models.FloatField(default=1)
    img2 = models.CharField(max_length=200)
    childcid2 = models.CharField(max_length=16,null=True)
    productid2 = models.CharField(max_length=16,null=True)
    longname2 = models.CharField(max_length=100)
    price2 = models.FloatField(default=0)
    marketprice2 = models.FloatField(default=1)
    img3 = models.CharField(max_length=200)
    childcid3 = models.CharField(max_length=16,null=True)
    productid3 = models.CharField(max_length=16,null=True)
    longname3 = models.CharField(max_length=100)
    price3 = models.FloatField(default=0)
    marketprice3 = models.FloatField(default=1)

    class Meta:
        db_table = 'axf_mainshow'

# 闪购左侧模型
class FoodType(models.Model):
    typeid = models.CharField(max_length=60)
    typename = models.CharField(max_length=100)
    childtypenames = models.CharField(max_length=200)
    typesort = models.IntegerField(default=1)

    class Meta:
        db_table = 'axf_foodtypes'


class Goods(models.Model):
    productid = models.CharField(max_length=16)  # 商品的id
    productimg = models.CharField(max_length=200)  # 商品的图片
    productname = models.CharField(max_length=100)  # 商品的名称
    productlongname = models.CharField(max_length=200)  # 商品的规格
    isxf = models.IntegerField(default=1)
    pmdesc = models.CharField(max_length=100)
    specifics = models.CharField(max_length=100)  # 规格
    price = models.FloatField(default=0)  # 商品的折后价格
    marketprice = models.FloatField(default=1)  # 商品的原价
    categoryid = models.CharField(max_length=16)  # 分类的id
    childcid = models.CharField(max_length=16)  # 子分类的id
    childcidname = models.CharField(max_length=100)  # 子分类的名称
    dealerid = models.CharField(max_length=16)
    storenums = models.IntegerField(default=1)  # 排序
    productnum = models.IntegerField(default=1)  # 销量排序

    class Meta:
        db_table = 'axf_goods'

class UserModel(models.Model):
    username = models.CharField(max_length=32,unique=True)
    password = models.CharField(max_length=256)
    email = models.CharField(max_length=64, unique=True)
    # Falsh代表女
    sex = models.BooleanField(default=False)
    icon = models.ImageField(upload_to='icon')
    is_delete = models.BooleanField(default=False)
    ticket = models.CharField(max_length=30,null=True)

    class Meta:
        db_table = 'axf_user'

# 购物车
class CarModel(models.Model):
    user = models.ForeignKey(UserModel)  # 关联用户
    goods = models.ForeignKey(Goods)  # 关联商品
    c_num = models.IntegerField(default=1)  # 商品的个数
    is_select = models.BooleanField(default=True)  # 是否选择商品

    class Meta:
        db_table = 'axf_cart'

class OrderModel(models.Model):
    user = models.ForeignKey(UserModel)  # 关联用户
    o_num = models.CharField(max_length=64)  # 数量
    # 0 代表下单，但是未付款 1 代表已付款未发货 2 已付款。已发货
    o_status = models.IntegerField(default=0)  # 状态
    o_create = models.DateTimeField(auto_now_add=True)  # 创建时间

    class Meta:
        db_table = 'axf_order'


class OrderGoodsModel(models.Model):
    goods = models.ForeignKey(Goods)  # 关联的商品
    order = models.ForeignKey(OrderModel)  # 关联的订单
    good_num = models.IntegerField(default=1)  # 商品的个数

    class Meta:
        db_table = 'axf_order_goods'

class UserTicketModel(models.Model):
    user = models.ForeignKey(UserModel)
    ticket = models.CharField(max_length=30,null=True)
    out_time = models.DateTimeField()

    class Meta:
        db_table = 'axf_user_ticket'