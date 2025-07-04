"""
URL configuration for 去哪儿旅游数据分析推荐系统 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
#主路由配置文件，不处理用户具体路由，只做请求的分发，即分布式请求处理。具体的请求由各自应用进行处理
from django.contrib import admin #站点
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

from django.views.generic import RedirectView  # 添加这行  后加的2025年6.12  wx
urlpatterns = [
    path('admin/', admin.site.urls),   #django后台 站点管理
    path('app/',include('app.urls')), #app应用
    # path('',include('app.urls'))
    path('', RedirectView.as_view(url='/app/login/')),  # 重定向到登录页  后加的2025年6.12  wx
    path('app/captcha/', include('captcha.urls'))       # 后加的2025年6.12  wx
]

urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

admin.site.site_title = '旅游推荐系统管理端'  # 修改SimpleUI后台管理系统的网站标签页名称
admin.site.site_header = '旅游推荐系统管理端'  # 修改SimpleUI后台管理系统的网站名称：显示在登录页和首页



