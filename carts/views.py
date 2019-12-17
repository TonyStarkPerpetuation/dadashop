from django.views import View
# 继承django的view 重写成类视图函数
import json
from goods.models import *
# Create your views here.
from django.http import JsonResponse
from django_redis import get_redis_connection
from utils.loging_decorator import logging_check

redis_conn = get_redis_connection('cart')

# 购物车
class CartVIew(View):
    def dispatch(self, request, *args, **kwargs):
        if request.method in ("POST","DELETE"):
            cart_dict = json.loads(request.body)
            sku_id = cart_dict.get('sku_id')
            if not sku_id:
                return JsonResponse({'code': 30102, 'error': '没有sku_id参数'})
            try:
                sku = SKU.objects.get(id=sku_id)  # 11: 红袖添香
            except Exception as e:
                print(e)
                return JsonResponse({'code': 30101, 'error': "未找到商品"})
            request.cart_dict = cart_dict
            request.sku_id = sku_id
            request.sku = sku
            return super().dispatch(request, *args, **kwargs)
        return super().dispatch(request, *args, **kwargs)

    def set_select_unselect(self, user_id, sku_id, selected):
        '''
        put 请求的state 状态 select 和  unselect
        :param user_id: 用户id user.id
        :param sku_id: 商品id int sku_id
        :param selected: 状态码（0/1)
        :return: 响应列表 [{"id":"","name":"","count":"","selected":""},{"":""...}]
        '''
        redis_c = redis_conn.hget('cart_%d' % user_id, sku_id)
        if not redis_c:
            return JsonResponse({'code': 30101, 'error': '未找到商品'})
        count = int(json.loads(redis_c)['count'])
        status = json.dumps({'count': count, 'selected': selected})
        redis_conn.hset('cart_%d' % user_id, sku_id, status)
        skus_list = self.get_cart_list(user_id)
        return skus_list

    def set_selectall_unselectall(self, user_id, selected):
        '''
        put 请求的state 状态selectall 和 unselectall
        :param user_id: 用户id user.id
        :param selected: 状态码（0/1)
        :return: 响应列表 [{"id":"","name":"","count":"","selected":""},{"":""...}]
        '''
        cart_all = redis_conn.hgetall('cart_%d' % user_id)
        if not cart_all:
            return JsonResponse({'code': 30101, 'error': '未找到商品'})
        for sku_id in cart_all.keys():
            cart_c = redis_conn.hget('cart_%d' % user_id, sku_id)
            # count = int(json.loads(cart_c)['count'])
            # status = json.dumps({'count': count, 'selected': selected})
            status = json.loads(cart_c)
            status['selected'] = selected
            status = json.dumps(status)
            redis_conn.hset('cart_%d' % user_id, sku_id, status)
        skus_list = self.get_cart_list(user_id)
        return skus_list

    def get_cart_list(self, user_id):
        '''
        :param user_id: 用户的id
        :return: reqsponse 列表 [{"id":"","name":"","count":"","selected":""},{"":""...}]
        '''
        cart_dict = {}
        # print('get cart list')
        # 重新去redis数据
        redis_cart = redis_conn.hgetall('cart_%d' % user_id)
        for sku_id, status in redis_cart.items():
            cart_dict[int(sku_id.decode())] = {
                'state': json.loads(status),
            }
        skus = SKU.objects.filter(id__in=cart_dict.keys())
        skus_list = []
        for sku in skus:
            sku_dict = {}
            sku_dict['id'] = sku.id
            sku_dict['name'] = sku.name
            sku_dict['count'] = int(cart_dict[sku.id]['state']['count'])
            sku_dict['selected'] = int(cart_dict[sku.id]['state']['selected'])
            sku_dict['default_image_url'] = str(sku.default_image_url)
            sku_dict['price'] = sku.price
            sku_sale_attr_name = []
            sku_sale_attr_val = []

            saleattr_vals = SaleAttrValue.objects.filter(sku_id=sku.id)
            for saleattr_val in saleattr_vals:
                #属性值
                sku_sale_attr_val.append(saleattr_val.sale_attr_value_name)
                # 1,通过在 spu类中查询所有
                # saleattrname = SPUSaleAttr.objects.filter(saleattrvalue=saleattr_val)[0]
                # 2,通过外键直接找到
                saleattrname = saleattr_val.sale_attr_id.sale_attr_name
                #属性名称
                sku_sale_attr_name.append(saleattrname)

                # print(sku_sale_attr_name)

            sku_dict['sku_sale_attr_name'] = sku_sale_attr_name
            sku_dict['sku_sale_attr_val'] = sku_sale_attr_val
            skus_list.append(sku_dict)
        return skus_list

    # post方式接收
    @logging_check
    def post(self, request, username):
        """
            1.获取用户传递数据。包括前端传递的数据。sku ID\ count
            2.判断购买数量和库存类比。
            3.判断用户是否合法
            4.实现购物车的增加：
                4.1 如果购物车服务器缓存中已经有，那么累加，存入缓存
                4.2 如果购物车的服务器缓存中没有，那么新增。存入缓存
            5.获取当前登陆用户购物车中的商品，返回前端。
        """
        cart_dict = request.cart_dict
        sku = request.sku
        count = cart_dict.get('count')
        stock = sku.stock
        try:
            count = int(count)
        except Exception:
            return JsonResponse({'code':10112,'error':'count error'})
        if count > stock:
            return JsonResponse({'code':10113,'error':'count > stock'})

        user = request.user
        if username != user.username:
            return JsonResponse({'code':10114,'error':'username error'})

        redis_cart = redis_conn.hget('cart_%d'%user.id,sku.id)

        # if sku.id.encode() in redis_cart:
        #     redis_cart[sku.id.encode()].count += 1
        if redis_cart:
            redis_count = json.loads(redis_cart)['count']
            redis_count += count
            if redis_count > stock:
                return JsonResponse({'code':10115,'error':'count > stock too'})
            status = json.dumps({'count':redis_count,'selected':1})
            redis_conn.hset('cart_%d' % user.id, sku.id, status)
        else :
            status = json.dumps({'count':count,'selected':1})
            redis_conn.hset('cart_%d'%user.id,sku.id,status)

        skus_list = self.get_cart_list(user.id)
        return JsonResponse({'code':200,'data':skus_list})


        # cart_dict = request.cart_dict
        # sku_id = request.sku_id
        # sku = request.sku  # 11: 红袖添香
        # count = cart_dict.get('count')
        # try:
        #     count = int(count)
        # except Exception as e:
        #     print(e)
        #     return JsonResponse({'code': 30102, 'error': "传参不正确"})
        # if count > sku.stock:
        #     return JsonResponse({'code': 30103, 'error': '购买数量超过库存'})
        # user = request.user
        # if user.username != username:
        #     return JsonResponse({'code': 30104, 'error': '非登录者用户'})
        # redis_cart = redis_conn.hgetall('cart_%d' % user.id)  # {b'9': b'{"count": 18, "selected": 1}'}
        #
        # # 如果redis中存在 则累增
        # if sku_id.encode() in redis_cart.keys():
        #     redis_c = redis_conn.hget('cart_%d' % user.id, sku_id)  # b'{"count": 21, "selected": 1}'
        #     count_r = int(json.loads(redis_c)['count'])
        #     count_r += count
        #     # 添加qi
        #     if count_r > sku.stock:
        #         return JsonResponse({'code': 30103, 'error': '购买数量超过库存'})
        #     status = json.dumps({'count': count_r, 'selected': 1})
        #     redis_conn.hset('cart_%d' % user.id, sku_id, status)
        # # 否则hmset插入Redis
        # else:
        #     # 默认都为勾选状态 1勾选 0未勾选
        #     status = json.dumps({'count': count, 'selected': 1})  # {"count": 21, "selected": 1}
        #     redis_conn.hset('cart_%d' % user.id, sku_id, status)
        #     print("管道2执行完毕")
        # skus_list = self.get_cart_list(user.id)
        # return JsonResponse({'code': 200, 'data': skus_list})

    # 查询购物车
    @logging_check
    def get(self, request, username):
        user = request.user
        if user.username != username:
            return JsonResponse({'code':10111,'error':'username error'})
        sku_list = self.get_cart_list(user.id)
        return JsonResponse({'code':200,'data':sku_list})


        # user = request.user
        # if user.username != username:
        #     return JsonResponse({'code': 30104, 'error': '非登录者用户'})
        # redis_cart = redis_conn.hgetall('cart_%d' % user.id)
        # for s_id in redis_cart.keys():
        #     redis_c = redis_conn.hget('cart_%d' % user.id, s_id)
        #     count_r = int(json.loads(redis_c)['count'])
        #     status = json.dumps({'count': count_r, 'selected': 1})
        #     redis_conn.hset('cart_%d' % user.id, s_id, status)
        # skus_list = self.get_cart_list(user.id)
        # return JsonResponse({'code': 200, 'data': skus_list})

    # 删除购物车
    @logging_check
    def delete(self, request, username):
        """
       1.拿出用户需要删除的sku_id
       2.删除用户的数据库中的sku_id
       3.返回购物车中的数据。
       """
        sku_id = request.sku_id
        user = request.user
        if username != user.username:
            return JsonResponse({'code':10116,'error':'username error '})

        redis_conn.hdel('cart_%d'%user.id,sku_id)

        skus_list = self.get_cart_list(user.id)

        return JsonResponse({'code':200,'data':skus_list})



        # sku_id = request.sku_id
        # user = request.user
        # if user.username != username:
        #     return JsonResponse({'code': 30104, 'error': '非登录者用户'})
        #
        # # 从hash值中删除该SKU_ID
        # redis_conn.hdel('cart_%d' % user.id, sku_id)
        # skus_list = self.get_cart_list(user.id)
        # return JsonResponse({'code': 200, 'data': skus_list})

    @logging_check
    def put(self, request, username):
        """
        1.取出前端传递的数据。
        2.根据前端传递的标志进行判断是增加、减少
            2.1 如果是增加的话，对于数量增加。
            2.2 如果是删除的话，对于数量减少。
        """
        json_obj = json.loads(request.body)
        state = json_obj.get('state')
        # sku_id = json_obj.get('sku_id')
        user = request.user
        if username != user.username:
            return JsonResponse({'code': 10116, 'error': 'username error '})
        if state in ('add','del'):
            sku_id = json_obj.get('sku_id')
            try:
                sku = SKU.objects.get(id=sku_id)
            except Exception:
                return JsonResponse({'code':10117,'error':'sku error'})
            redis_goods = redis_conn.hget('cart_%d'%user.id,sku_id)
            if not redis_goods:
                return JsonResponse({'code':10118,'error':'redis goods not find'})
            count_redis = json.loads(redis_goods)['count']
            count_redis = int(count_redis)
            if state == 'add':
                count_redis += 1
                if count_redis > sku.stock:
                    return JsonResponse({'code':10119,'error':'count_redis > sku.stock'})
            else :
                count_redis -= 1
                if count_redis < 1:
                    count_redis = 1
            status = json.dumps({'count':count_redis,'selected':1})
            redis_conn.hset('cart_%d'%user.id,sku_id,status)
            skus_list = self.get_cart_list(user.id)
            return JsonResponse({'code':200,'data':skus_list})

        # state ['select','unselect','selectall','unselectall']
        elif state in ['select','unselect']:
            sku_id = json_obj.get('sku_id')
            if not sku_id:
                return JsonResponse({'code':10117,'error':'sku_id error'})

            if state == 'select':
                skus_list = self.set_select_unselect(user.id,sku_id,1)
            else :
                skus_list = self.set_select_unselect(user.id,sku_id,0)

            return JsonResponse({'code':200,'data':skus_list})

        elif state in ['selectall', 'unselectall']:
            if state == 'selectall':
                skus_list = self.set_selectall_unselectall(user.id,1)
            else :
                skus_list = self.set_selectall_unselectall(user.id,0)

            return JsonResponse({'code':200,'data':skus_list})




























        # cart_dict = json.loads(request.body)
        # state = cart_dict.get('state')
        # user = request.user
        # if user.username != username:
        #     return JsonResponse({'code': 30104, 'error': '非登录者用户'})
        #
        # # 判断增加还是减少
        # if state == 'add' or state == "del":
        #     sku_id = cart_dict.get('sku_id')
        #     try:
        #         sku = SKU.objects.get(id=sku_id)
        #     except Exception as e:
        #         return JsonResponse({'code': 30101, 'error': "未找到商品"})
        #     redis_c = redis_conn.hget('cart_%d' % user.id, sku_id)
        #     if not redis_c:
        #         return JsonResponse({'code': 30101, 'error': '未找到商品'})
        #     count = int(json.loads(redis_c)['count'])
        #
        #     # 检查数据
        #     if state == 'add':
        #         # 向hash中存储商品的ID,和数量
        #         count += 1
        #         if count > sku.stock:
        #             return JsonResponse({'code': 30103, 'error': '购买数量超过库存'})
        #         status = json.dumps({'count': count, 'selected': 1})
        #         redis_conn.hset('cart_%d' % user.id, sku.id, status)
        #         skus_list = self.get_cart_list(user.id)
        #         return JsonResponse({'code': 200, 'data': skus_list})
        #
        #     elif state == 'del':
        #         if count > 1:
        #             count -= 1
        #             status = json.dumps({'count': count, 'selected': 1})
        #             redis_conn.hset('cart_%d' % user.id, sku.id, status)
        #             skus_list = self.get_cart_list(user.id)
        #         else:
        #             status = json.dumps({'count': 1, 'selected': 1})
        #             redis_conn.hset('cart_%d' % user.id, sku.id, status)
        #             skus_list = self.get_cart_list(user.id)
        #         return JsonResponse({'code': 200, 'data': skus_list})
        #
        # # 判断是否勾选
        # if state == 'select' or state == 'unselect':
        #     sku_id = cart_dict.get('sku_id')
        #     # 勾选
        #     if state == 'select':
        #         skus_list = self.set_select_unselect(user.id, sku_id, 1)
        #         return JsonResponse({'code': 200, 'data': skus_list})
        #
        #     # 取消勾选
        #     if state == 'unselect':
        #         skus_list = self.set_select_unselect(user.id, sku_id, 0)
        #         return JsonResponse({'code': 200, 'data': skus_list})
        #
        # # 判断是否全选
        # if state == 'selectall' or state == 'unselectall':
        #     if state == 'selectall':
        #         skus_list = self.set_selectall_unselectall(user.id, 1)
        #         return JsonResponse({'code': 200, 'data': skus_list})
        #
        #     if state == 'unselectall':
        #         skus_list = self.set_selectall_unselectall(user.id, 0)
        #         return JsonResponse({'code': 200, 'data': skus_list})


