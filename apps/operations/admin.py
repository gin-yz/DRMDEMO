from django.contrib import admin
from apps.operations.models import *


class BannerAdmin(admin.ModelAdmin):
    list_display = ['type', 'index', 'title', 'url']
    search_fields = ['index', 'title', 'url', 'type']
    list_filter = ['index', 'type']
    list_editable = ['index', 'title', 'url']


class UserMusicAdmin(admin.ModelAdmin):
    list_display = ['user', 'purchase_bcId', 'music', 'purchase_permission', 'purchase_status', 'purchase_isUpdate',
                    'timestamp', 'get_vailtime', ]
    search_fields = ['user', 'purchase_bcId', 'music', 'purchase_permission', 'purchase_status', 'purchase_isUpdate',
                     'timestamp', 'purchase_transactionHash']
    list_filter = ['user', 'music', 'purchase_status', 'purchase_isUpdate']
    list_editable = []


class WitchoutUserMusicAdmin(admin.ModelAdmin):
    list_display = ['purchase_bcId', 'product_bcId', 'purchase_permission', 'purchase_isUpdate', 'bought_address',
                    'timestamp', 'music_price']
    search_fields = ['purchase_bcId', 'product_bcId', 'purchase_permission', 'purchase_isUpdate', 'bought_address',
                     'timestamp', 'music_price']
    list_filter = ['product_bcId', 'purchase_isUpdate', 'bought_address','music_price']
    list_editable = []


class UserFavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'fav_id', 'fav_type']
    search_fields = ['user', 'fav_id', 'fav_type']
    list_filter = ['user', 'fav_id', 'fav_type']
    list_editable = ['fav_id', 'fav_type']


admin.site.register(Banner, BannerAdmin)
admin.site.register(UserMusic, UserMusicAdmin)
admin.site.register(WitchoutUserMusic, WitchoutUserMusicAdmin)
admin.site.register(UserFavorite, UserFavoriteAdmin)
