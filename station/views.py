
from datetime import datetime, timedelta
import hashlib
import json
import random
from django import http
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Q
from django.views import View
from django.core.mail import send_mail
from django.db.models.signals import post_save # 触发信号
from django.dispatch import receiver # 接收信号
from django.contrib.auth.models import User as AuthUser # 导入django自带的User模型
from django.conf import settings
from rest_framework.authtoken.models import Token # 导入Token模型

from rest_framework.permissions import IsAuthenticated # 导入认证权限类

from station.permission import IsOwnerOrReadOnly # 导入重写后的自定义权限类

from station.models import Category, User, Product
from station.serializers import ProductSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView # 类视图
from rest_framework import generics # 通用类视图
from rest_framework import viewsets # 视图集

from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication # 认证

# 定义一个装饰器来标记视图需要检查五分钟内是否发送过验证码
def require_time_check(view_func):
    def wrapper(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapper.__dict__.update(view_func.__dict__)
    wrapper.time_check = True
    return wrapper


# 定义一个装饰器来标记视图需要检查用户是否登录
def require_login_check(view_func):
    def wrapper(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapper.__dict__.update(view_func.__dict__)
    wrapper.login_check = True
    return wrapper


""" 结合Django信号机制: 当用户创建时,使用信号生成token, 并保存到数据库 """
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def generate_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


""" apiview函数式编程定义视图接口"""
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication]) # 为方法定义指定接口限制访问方式，超过全局认证，该接口只能使用token认证访问，用户名密码认证失效
@permission_classes([IsAuthenticated])  # 为方法定义指定接口权限认证，超过全局认证
def ProductList(request):
    """
    商品列表视图
    """
    if request.method == "GET":
        s = ProductSerializer(Product.objects.all(), many=True)
        return Response(s.data, status=status.HTTP_200_OK)
    elif request.method == "POST":
        s = ProductSerializer(data=request.data, partial=True)
        if s.is_valid():
            s.save()
            return Response(data=s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET', 'PUT', 'DELETE'])
def ProductDetail(request, pk):
    """
    商品详情视图
    """
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return Response(data={"msg": "Product not found"}, status=status.HTTP_404_NOT_FOUND)
    else:
        if request.method == "GET":
            s = ProductSerializer(instance=product)
            return Response(data=s.data, status=status.HTTP_200_OK)
        
        elif request.method == "PUT":
            s = ProductSerializer(instance=product, data=request.data, partial=True)
            if s.is_valid():
                s.save()
                return Response(data=s.data, status=status.HTTP_200_OK)
            return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)
        
        elif request.method == "DELETE":
            s.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

""" 使用类视图api定义接口 类视图为主"""
class ProductViewSet(APIView):

    authentication_classes = [TokenAuthentication] # 类中定义指定接口权限认证，超过全局认证，该接口只能使用token认证访问，用户名密码认证失效

    permission_classes = [IsAuthenticated] # 类中定义指定接口权限认证，超过全局认证


    def get(self, request):
        queryset = Product.objects.all()
        s = ProductSerializer(instance=queryset, many=True)
        return Response(data=s.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        s = ProductSerializer(data=request.data, partial=True)  # data是前端传来的数据
        if s.is_valid():
            s.save()
            return Response(data=s.data, status=status.HTTP_201_CREATED)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductDetailViewSet(APIView):
    def get_object(self, pk):
        try:
            return Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response(data={"msg": "Product not found"}, status=status.HTTP_404_NOT_FOUND)    

    def get(self, request, pk):
        queryset = self.get_object(pk)
        s = ProductSerializer(instance=queryset)
        return Response(data=s.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        queryset = self.get_object(pk)
        s = ProductSerializer(instance=queryset, data=request.data, partial=True)
        if s.is_valid():
            s.save()
            return Response(data=s.data, status=status.HTTP_200_OK)
        return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        queryset = self.get_object(pk)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

"""使用通用类视图定义接口"""
class ProductGenericViewSet(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    def perform_create(self, serializer):
        serializer.save()


class ProductDetailGenericViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_update(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        instance.delete()


"""使用视图集定义接口"""
class ProductViewSets(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer





class RegisterView(View):
    """
    注册视图
    """
    # 检查五分钟内是否发送过验证码
    time_check = True

    def get(self, request):
        return render(request, "station/register.html")
    
    @require_time_check
    def post(self, request):
        if request.method == "POST":
            # 1.提取数据
            email = request.POST.get("email")
            phonenumber = request.POST.get("phonenumber")
            username = request.POST.get("username")
            password = request.POST.get("password")

            # 2.验证用户是否已使用邮箱或手机号注册
            user_ret = User.objects.filter(Q(email=email)|Q(phonenumber=phonenumber)).first()
            if user_ret:
                return http.JsonResponse({"status": 1, "errmsg": "该邮箱或手机号已注册"})
            else:
                # 3.未注册则调用发送验证码视图
                send_ret = self.send_email(request, email)
                
                # 判断发送是否成功
                if send_ret:
                    
                    # 4.记录用户信息
                    request.session["username"] = username
                    request.session["email"] = email
                    request.session["phonenumber"] = phonenumber
                    request.session["password"] = password

                    print(f'username: {username}, email: {email}, phonenumber: {phonenumber}, password: {password}')

                    # 5.返回json响应提示用户检查邮箱
                    response = http.JsonResponse({"status": 3, "errmsg": "验证码已发送，请检查邮箱"})
                    response.set_cookie("time", datetime.now().isoformat())

                    return response
                else:
                    return http.JsonResponse({"status": 4, "errmsg": "验证码发送失败，请重新发送"})

    @require_time_check
    def send_email(self, request, email):
        """
        发送验证码
        """
        # 1 哈希生成6位随机字符验证码
        code = hashlib.sha256(str(random.randint(100000, 999999)).encode()).hexdigest()[:6]

        # 2 发送验证码至邮箱
        send_mail(
            subject="测试邮箱验证码",
            message=f"尊敬的用户您好！\n您的验证码是: <b>{code}</b>,请在5分钟内进行验证,否则验证码将失效。如果该验证码不为您本人申请,请忽略。",
            from_email="ackerman0919@163.com",
            recipient_list=[email],
            fail_silently=False
        )
        request.session["code"] = code
        return True
    

@require_time_check
def register_sendemail(request, email):
    """
    发送验证码视图
    """
    # 1 哈希生成6位随机字符验证码
    code = hashlib.sha256(str(random.randint(100000, 999999)).encode()).hexdigest()[:6]

    # 2 发送验证码至邮箱
    send_ret = send_mail(
        subject="测试邮箱验证码",
        message=f"尊敬的用户您好！\n您的验证码是: <b>{code}</b>,请在5分钟内进行验证,否则验证码将失效。如果该验证码不为您本人申请,请忽略。",
        from_email="ackerman0919@163.com",
        recipient_list=[email],
        fail_silently=False
    )

    # 3 判断发送是否成功
    if send_ret:
        # 4.session记录验证码
        request.session["code"] = code
        # 5.cookie记录发送时间
        response = http.JsonResponse({"status": 3, "errmsg": "验证码已发送，请检查邮箱"})
        response.set_cookie("time", datetime.now().isoformat())
        return response
    else:
        return http.JsonResponse({"status": 4, "errmsg": "验证码发送失败，请重新发送"})


def check_code(request):
    """
    检查验证码
    """
    # 判断请求方法
    if request.method == "POST":
        # 1.判断cookie中是否有时间且session中是否有邮箱和验证码
        cookie_time = request.COOKIES.get("time")
        email = request.session.get("email")
        session_code = request.session.get("code")
        if cookie_time and email and session_code:
            # 转换cookie中的时间字符串为datetime对象
            try:
                send_time = datetime.datetime.fromisoformat(cookie_time)
                # 2.检查验证码是否失效
                if datetime.datetime.now() - send_time > datetime.timedelta(minutes=5):
                    return http.JsonResponse({
                        "status": 11, 
                        "errmsg": "验证码已失效，请重新发送"
                    })
            except ValueError:
                # 如果时间格式转换失败，提示请重新发送验证码
                return http.JsonResponse({
                        "status": 11, 
                        "errmsg": "验证码已失效，请重新发送"
                    })
        else:
            # 3.如果cookie中没有时间，提示请重新发送验证码
            return http.JsonResponse({
                    "status": 12, 
                    "errmsg": "请重新发送验证码"
                })


        
        # 4.从请求体中获取用户输入的验证码    
        code = request.POST.get("code")

        # 5. 从session中获取用户信息
        user_name = request.session.get("username")
        phonenumber = request.session.get("phonenumber")
        password = request.session.get("password")
        print(f'session_code: {session_code}, code: {code}')


        # 6.判断验证码是否正确
        if session_code == code:
            # 7.如果正确，则删除session中的code和cookie中的time
            del request.session["code"]
            del request.COOKIES["time"]

            # 8.生成用户id
            user_id_front = email[:email.find("@")]
            user_id_behind = email[email.find("@")+1:]
            user_id_middle = user_id_behind[:user_id_behind.find(".")]
            user_id = user_id_front + user_id_middle

            # 9.在数据库中创建用户
            user_ret = User.objects.create(
                user_id=user_id,
                email=email,
                phonenumber=phonenumber,
                password=password,
                user_name=user_name
            )
            # 10.判断用户是否注册成功
            if user_ret:
                # 11.使用session记录用户id
                request.session["user_id"] = user_id



                # 12.使用cookie记录用户user_name
                response = http.JsonResponse({"status": 5, "errmsg": "注册成功!"})
                response.set_cookie("user_name", user_name)
                response.set_cookie("is_login", True)

                # 13.删除session中多余的用户信息
                del request.session["username"]
                del request.session["email"]
                del request.session["phonenumber"]
                del request.session["password"]

                # 注册成功返回json响应
                return response
            else:
                # 14.返回json响应提示用户注册失败
                return http.JsonResponse({"status": 6, "errmsg": "注册失败!"})
        else:
            # 15.返回json响应提示用户验证码错误
            return http.JsonResponse({"status": 7, "errmsg": "验证码错误, 请重新输入!"})
    else:
        # 16.返回json响应提示用户请求方法错误
        return http.JsonResponse({"status": 12, "errmsg": "请求方法错误!"})


class LoginView(View):
    """
    登录视图
    """
    def get(self, request):
        return render(request, "station/login.html")
    
    def post(self, request):
        # 1.提取数据
        identifier = request.POST.get("identifier")
        password = request.POST.get("password")

        # 2.检查用户是否存在
        user_ret = User.objects.filter(Q(email=identifier)|Q(phonenumber=identifier)).first()
        if user_ret:
            # 3.检查密码是否正确
            if user_ret.password == password:
                # 4.使用cookie记录用户user_name及状态使用session记录用户的user_id，并返回json响应
                request.session["user_id"] = user_ret.user_id
                response = http.JsonResponse({"status": 8, "errmsg": "登录成功!"})
                response.set_cookie("user_name", user_ret.user_name)
                response.set_cookie("is_login", True)

                print(f"user_id: {request.session.get('user_id')}, user_name: {request.COOKIES.get('user_name')}, is_login: {request.COOKIES.get('is_login')}")
                return response
            else:
                # 5.返回json响应提示用户密码错误
                return http.JsonResponse({"status": 9, "errmsg": "用户名或密码错误,请重新输入!"})
            
        else:
            # 用户不存在
            return http.JsonResponse({"status": 10, "errmsg": "用户不存在,请创建账号!"})


def logout(request):
    """
    退出登录视图
    """
    print(f"退出前:user_id: {request.session.get('user_id')}, user_name: {request.COOKIES.get('user_name')}, is_login: {request.COOKIES.get('is_login')}")
    # 1.清除session和cookie中的数据 
    del request.session["user_id"]
    response = http.JsonResponse({"status": 15, "errmsg": "退出登录成功!"})
    response.delete_cookie('user_name')
    response.delete_cookie('is_login')
    try:
        print(f"退出后:user_id: {request.session.get('user_id')}, user_name: {request.COOKIES.get('user_name')}, is_login: {request.COOKIES.get('is_login')}")
    except:
        pass
    # 2.重定向到首页
    return response

def index(request):
    """
    首页视图
    """
    return render(request, "station/index.html")

def about(request):
    """
    关于视图
    """
    return render(request, "station/about.html")


@require_login_check
def personal(request):
    """
    个人中心视图
    """
    user_id = request.session.get("user_id")
    user_ret = User.objects.filter(user_id=user_id).first()
    return render(request, "station/personal.html", {"User": user_ret})


def icon(request):
    """
    404页面视图
    """
    return render(request, "common/icon.html")

def service(request):
    """
    服务视图
    """
    return render(request, "station/service.html")

def shop(request):
    """
    商店视图
    """
    return render(request, "station/shop.html")

def contact(request):
    """
    联系视图
    """
    return render(request, "station/contact.html")

def product(request):
    """
    产品视图
    """
    return render(request, "station/product.html")

def typography(request):
    """
    排版视图
    """
    return render(request, "station/typography.html")

def single(request):
    """
    单页视图
    """
    return render(request, "station/single.html")    













