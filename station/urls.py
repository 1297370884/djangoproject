from django.urls import path, include

from station import views
from rest_framework.routers import DefaultRouter # 路由器

app_name = 'station' # 给urls应用整体一个命名空间

# 创建路由器对象
router = DefaultRouter()

# 注册路由
router.register(viewset=views.ProductViewSets, prefix='viewset', basename='viewset')

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('about/', views.about, name='about'),
    path('personal/', views.personal, name='personal'),
    path('check_code/', views.check_code, name='check_code'),
    path('register_sendemail/', views.register_sendemail, name='register_sendemail'),
    path('service/', views.service, name='service'),
    path('shop/', views.shop, name='shop'),
    path('contact/', views.contact, name='contact'),
    path('product/', views.product, name='product'),
    path('typography/', views.typography, name='typography'),
    path('single/', views.single, name='single'),

    # 函数视图API
    path('func/products/list/', views.ProductList, name='fbv-product_list'),
    path('func/products/detail/<int:pk>/', views.ProductDetail, name='fbv-product_detail'),

    # 类视图API
    path('cbv/products/list/', views.ProductViewSet.as_view(), name='cbv-product_list'),    
    path('cbv/products/detail/<int:pk>/', views.ProductDetailViewSet.as_view(), name='cbv-product_detail'),

    # 使用通用类视图定义接口
    path('generic/products/list/', views.ProductGenericViewSet.as_view(), name='generic-product_list'),
    path('generic/products/detail/<int:pk>/', views.ProductDetailGenericViewSet.as_view(), name='generic-product_detail'),

    # 使用视图集定义接口
    # path('viewset/', views.ProductViewSets.as_view({'get': 'list', 'post': 'create'}), name='viewset-product_list'),
    # path('viewset/<int:pk>/', views.ProductViewSets.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='viewset-product_detail'),

    # 使用视图集+路由器定义接口
    path('', include(router.urls)),
]
