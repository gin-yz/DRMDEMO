from django.urls import path
from django.conf.urls import url

from apps.operations.views import AddFavView

urlpatterns = [
    # 添加收藏
    url(r'^fav/$', AddFavView.as_view(), name="fav"),

]