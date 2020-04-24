from django.conf.urls import url
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from apps.operations.views import UploadMusicView, UploadOneView, MyPurMusicView, \
    UpdateMyPermissionOneView, PurDetialDownView, DownloadKeyView, MusicianHomeView, \
    MusicianMusicView, MusicianMusicDetial, UploadFileView
from apps.users.views import UserInfoView, UploadImageView, ChangePwdView, SendEmailCodeView, UpdateEmailView, \
    UpdateKeyView, UpdateKeyValueView, MyFavView, MyFavMusicianView, MyMessageView,ModifyFreestyle
from apps.operations import views

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name="info"),
    url(r'^image/upload/$', UploadImageView.as_view(), name="image"),
    url(r'^update/pwd/$', ChangePwdView.as_view(), name="update_pwd"),
    # 发送邮箱验证码
    path("sendemail_code/", SendEmailCodeView.as_view(), name='sendemail_code'),
    # 修改邮箱
    path("update_email/", UpdateEmailView.as_view(), name='update_email'),
    # 生成新交易账户
    path("update_key/", UpdateKeyView.as_view(), name='update_key'),
    path("update_value/", csrf_exempt(UpdateKeyValueView.as_view()), name='update_value'),
    # 发布我的音乐版权
    path("uploadmusic/", UploadMusicView.as_view(), name='uploadmusic'),
    # 上传版权
    path("uploadone/", UploadOneView.as_view(), name='uploadone'),
    # 上传文件
    path("uploadfile/", UploadFileView.as_view(), name='uploadfile'),
    # 我的音乐
    url(r'^mypurchase_music/$', MyPurMusicView.as_view(), name='mypurchase_music'),
    # 更新音乐权限
    path('updatemusic/', UpdateMyPermissionOneView.as_view(), name='updatemusic'),
    # 下载购买详情
    path('purdetialdown/', PurDetialDownView.as_view(), name='purdetialdown'),
    # 下载密钥
    path('downloadkey/', DownloadKeyView.as_view(), name='downloadkey'),
    # 我的收藏
    url(r'^myfav/$', MyFavView.as_view(), name="myfav"),
    url(r'^myfav_musician/$', MyFavMusicianView.as_view(), name="myfav_musician"),
    # 发布版权信息中心
    path('musicianhome/', MusicianHomeView.as_view(), name='musicianhome'),
    # 发布的版权
    path('musicianmusic/', MusicianMusicView.as_view(), name='musicianmusic'),
    # 版权发布者查看版权具体信息
    path('musicianmusicdetial/', MusicianMusicDetial.as_view(), name='musicianmusicdetial'),
    path('musicianmusicsolddetial/', views.musicianmusicsolddetial, name='musicianmusicsolddetial'),
    # 我的消息
    url(r'^messages/$', MyMessageView.as_view(), name="messages"),
    # 修改freestyle
    path('modifyfreestyle/', ModifyFreestyle.as_view(), name='modifyfreestyle')
]
