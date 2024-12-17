from rest_framework import permissions


"""自定义权限类,重写has_permission方法"""
class IsOwnerOrReadOnly(permissions.BasePermission):


    def has_object_permission(self, request, view, obj):


        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        # 写请求需要检查用户是否是对象的作者
        return obj.user == request.user

