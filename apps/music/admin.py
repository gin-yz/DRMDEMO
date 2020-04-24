from django.contrib import admin
from apps.music.models import *

admin.site.site_header = "区块链音乐版权管理系统"

admin.site.site_title="区块链音乐版权管理系统"

@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ['owner','music_bcId','music_name','is_banner',"add_time",'music_status',  'fav_nums', 'click_nums',
                    'all_sell_count', "all_sell_money", "hot_num"]
    search_fields = ['music_name', 'music_desc', 'music_bcId', 'music_status', 'owner']
    list_filter = ['owner','music_status',"add_time"]
    list_editable = ["music_status",'is_banner']

@admin.register(BannerMusic)
class BannerMusicAdmin(admin.ModelAdmin):
    list_display = ['music_bcId','music_name',"add_time",'music_status', 'owner', 'fav_nums', 'click_nums',
                    'all_sell_count', "all_sell_money", "hot_num"]
    search_fields = ['music_name', 'music_desc', 'music_bcId', 'music_status', 'owner']
    list_filter = ['owner','music_status',"add_time"]
    list_editable = ["music_status"]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.filter(is_banner=True)
        return qs


@admin.register(WithoutMusic)
class WithoutMusicAdmin(admin.ModelAdmin):
    list_display = ['music_name', 'music_bcId', 'owneraddress', 'music_transactionHash', 'music_status', 'music_desc']
    search_fields = ['music_name', 'music_bcId', 'owneraddress', 'music_transactionHash', 'music_status', 'music_desc']
    list_filter = [ 'owneraddress', 'music_status']
    list_editable = []


@admin.register(MusicComments)
class MusicCommentsAdmin(admin.ModelAdmin):
    list_display = ['user', 'music', 'comments']
    search_fields = ['user', 'music', 'comments']
    list_filter = ['user', 'music']
    list_editable = ['music', 'comments']


@admin.register(MusicTag)
class MusicTagAdmin(admin.ModelAdmin):
    list_display = ['music', 'tag', 'show_name']
    search_fields = ['music', 'tag']
    list_filter = ['music', 'tag']
    list_editable = ['tag']