"""djangoproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken import views
# from rest_framework.schemas import get_schema_view # 导入获取schema的视图
from rest_framework.documentation import include_docs_urls


# schema_view = get_schema_view(title='API Schema', description='API Schema for the API') # 获取schema的视图

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),  # 获取token的接口
    # path('api-auth/', include('rest_framework.urls')),  # DRF登录退出
    path('admin/', admin.site.urls),
    path('docs/', include_docs_urls(title='API Documentation', description='API Documentation for the API')), # 获取schema的视图
    path('station/', include('station.urls')),  # 简化include的使用
    # path('schema/', schema_view), # 获取schema的视图

    
]
