from django.conf.global_settings import STATIC_ROOT
from django.contrib import admin
from django.urls import path, re_path
# from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
from django.conf.urls import url, include
from DRMDEMO.settings import MEDIA_ROOT

from apps.users.views import LoginView, RegisterView, ActiveUserView, ForgetPwdView, ResetView, ModifyPwdView, \
    LogoutView, MusicianListView, MusicianDetailView
from apps.operations.views import IndexView
from django.views.generic.base import RedirectView
from apps.music.views import PriceIntroduceView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('register/', RegisterView.as_view(), name="register"),
    re_path('active/(?P<active_code>.*)/', ActiveUserView.as_view(), name='user_active'),
    path('forget/', ForgetPwdView.as_view(), name='forget_pwd'),
    re_path('reset/(?P<active_code>.*)/', ResetView.as_view(), name='reset_pwd'),
    path('modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve, {"document_root":STATIC_ROOT}),
    url(r'^ueditor/', include('DjangoUeditor.urls')),
    # 个人相关页面
    url(r'^users/', include(('apps.users.urls', "users"), namespace="users")),

    # 音乐相关页面
    url(r'^music/', include(('apps.music.urls', "music"), namespace="music")),

    # 用户相关操作
    url(r'^op/', include(('apps.operations.urls', "operations"), namespace="op")),

    # 版权发布者相关页面

    url(r'^musician/$', MusicianListView.as_view(), name="musician"),
    url(r'^musician/(?P<musician_id>\d+)/$', MusicianDetailView.as_view(), name="musician_detail"),

    path('', IndexView.as_view(), name='index'),

    url(r'^favicon.ico$', RedirectView.as_view(url=r'static/images/reform/favicon.ico')),
    # path('receiveuploadsystem/',csrf_exempt(views.receiveuploadsystem),name = 'receiveuploadsystem'),

    # 首页后两个页面
    path('priceintroduce/',PriceIntroduceView.as_view(),name = 'priceintroduce'),
    # path('howtostart/',HowToStartView.as_view(),name='howtostart'),


]
