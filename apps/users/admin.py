from django.contrib import admin
from apps.users.models import *


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['nick_name', 'is_active', 'email', 'address', 'mobile']
    search_fields = ['nick_name', 'is_active', 'email', 'address', 'mobile']
    list_filter = [ 'is_active']
    list_editable = []


class ProductUserAdmin(admin.ModelAdmin):
    list_display = ['nick_name', 'fav_nums', 'click_nums', 'is_active', 'email','get_all_music_num',
                    'get_all_sell_num', 'get_all_money', 'hot_num']
    search_fields = ['nick_name', 'fav_nums', 'click_nums', 'is_active', 'email', 'points', 'address', 'description']
    list_filter = ['is_active']
    list_editable = []

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        qs = qs.filter(is_producter=True)
        return qs


class UserMessageAdmin(admin.ModelAdmin):
    list_display = ['user', 'message', 'has_read']
    search_fields = ['user', 'message', 'has_read']
    list_filter = ['user', 'message', 'has_read']
    list_editable = []


class EmailVerifyRecordAdmin(admin.ModelAdmin):
    list_display = ['send_time', 'send_type', 'email', 'code']
    search_fields = ['send_time', 'send_type', 'email', 'code']
    list_filter = ['send_time', 'send_type', 'email']
    list_editable = []


admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ProductUser, ProductUserAdmin)
admin.site.register(UserMessage, UserMessageAdmin)
admin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
