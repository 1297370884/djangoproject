import datetime
from django import http
from django.utils.deprecation import MiddlewareMixin

from station.models import User


class check_timeout(MiddlewareMixin):
    '''
        检查验证码是否在5分钟内发送过
    '''
    def process_view(self, request, view_func, view_args, view_kwargs):

        # 检查类视图是否有 time_check标记
        if hasattr(view_func, 'time_check'):
        
            if request.method == "POST":
                # 取出当前输入邮箱
                current_email = request.POST.get("email")
                # 取出session中邮箱
                session_email = request.session.get("email")
                # 取出session中验证码
                session_code = request.session.get("code")

                # 取出cookie中邮件发送时间
                cookie_time = request.COOKIES.get("time")

                # 判断cookie中是否有时间且session中是否有邮箱和验证码
                if cookie_time and session_email and session_code:
                    # 转换cookie中的时间字符串为datetime对象
                    try:
                        send_time = datetime.datetime.fromisoformat(cookie_time)
                        # 检查是否在5分钟内且email相同
                        if (datetime.datetime.now() - send_time <= datetime.timedelta(minutes=5) and 
                            current_email == session_email):
                            return http.JsonResponse({
                                "status": 2, 
                                "errmsg": "五分钟内已发送过验证码，请检查邮箱"
                            })
                    except ValueError:
                        # 如果时间格式转换失败,继续执行视图函数
                        pass

        return None
            
class check_login(MiddlewareMixin):
    '''
        检查用户是否登录
    '''
    def process_view(self, request, view_func, view_args, view_kwargs):
        # 检查类视图是否有 login_check标记
        if hasattr(view_func, 'login_check'):
            # 取出session中的user_id
            user_id = request.session.get("user_id")
            # 取出cookie中的is_login
            is_login = request.COOKIES.get("is_login")
            # 取出cookie中的user_name
            user_name = request.COOKIES.get("user_name")
            # 判断是否登录
            if user_id and is_login and user_name:
                # 查询用户
                user_ret = User.objects.filter(user_id=user_id, user_name=user_name).first()
                
                # 检查用户是否存在
                if user_ret:
                    return None
                else:
                    # 
                    return http.JsonResponse({"status": 14, "errmsg": "用户未登录,请登录!"})
            else:
                return http.JsonResponse({"status": 14, "errmsg": "用户未登录,请登录!"})



   



