# from django.utils.deprecation import MiddlewareMixin
# from django.shortcuts import render,redirect
#
# class UserMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         path = request.path_info
#         if path == '/app/login/' or path == '/app/register/':
#             return None
#         else:
#             if not request.session.get('username'):
#                 return redirect('/app/login/')
#             else:
#                 return None
#
#
#     def process_view(self,request,callback,callback_args,callback_kwargs):
#         pass
#
#     def process_response(self,request,response):
#         return response


from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render, redirect


class UserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        path = request.path_info

        # 需要放行的路径白名单
        white_list = [
            '/app/login/',  # 登录页
            '/app/register/',  # 注册页
            '/app/captcha/'  # 新增验证码路径  <-- 关键修改
        ]

        # 检查请求路径是否在白名单
        if path in white_list:
            return None  # 直接放行

        # 需要登录的路径检查
        if not request.session.get('username'):
            return redirect('/app/login/')

        return None  # 已登录用户放行

    # 以下保持原样即可
    def process_view(self, request, callback, callback_args, callback_kwargs):
        pass

    def process_response(self, request, response):
        return response