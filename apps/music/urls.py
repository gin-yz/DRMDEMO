from django.urls import path
from django.conf.urls import url
from apps.music import views
from apps.music.views import MusicListView, MusicDetailView, ModifyMyMuiscInfoView
from apps.operations.views import PurchaseOneView

urlpatterns = [
    url(r'^musiclist/$', MusicListView.as_view(), name="musiclist"),
    url(r'^(?P<music_id>\d+)/$', MusicDetailView.as_view(), name="detail"),
    # 用户购买
    path("purchaseone/", PurchaseOneView.as_view(), name='purchaseone'),
    # 用户退款
    # path("refundmoney/",RefundMoneyView.as_view(),name='refundmoney'),
    # 修改版权状态
    # path("modifymusic/", ModifyMusicView.as_view(), name='modifymusic'),
    # url(r'^(?P<course_id>\d+)/comments/$', MusicCommentsView.as_view(), name="comments"),
    # 发表评论
    url(r'^comment/$', views.CommentMusic, name="comment"),
    # 删除评论
    path('deletecomm/',views.DeleteComment,name='deletecomm'),
    path('modifymymuiscinfo/',ModifyMyMuiscInfoView.as_view(),name='modifymymuiscinfo'),
]
