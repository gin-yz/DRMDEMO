import time

from django.db import models

# Create your models here.
from apps.music.models import Music
from apps.users.models import BaseModel, UserProfile


def period_validity(permit):
    periodvalidity_list = [0, 12960000, 30758400, 94608000, 0, 0]
    return periodvalidity_list[permit - 1]


def convert_time_to_str(time):
    # 时间数字转化成字符串，不够10的前面补个0
    if (time < 10):
        time = '0' + str(time)
    else:
        time = str(time)
    return time


def sec_to_data(y):
    h = int(y // 3600 % 24)
    d = int(y // 86400)
    m = int((y % 3600) // 60)
    s = round(y % 60, 2)
    h = convert_time_to_str(h)
    m = convert_time_to_str(m)
    s = convert_time_to_str(s)
    d = convert_time_to_str(d)
    # 天 小时 分钟 秒
    return d + "天" + h + "小时" + m + "分钟" + s + "秒"


class Banner(BaseModel):
    title = models.CharField(max_length=100, verbose_name="标题")
    image = models.ImageField(upload_to="banner/%Y/%m", max_length=200, verbose_name="轮播图")
    url = models.URLField(max_length=200, verbose_name="访问地址")
    index = models.IntegerField(default=0, verbose_name="顺序")
    type =models.IntegerField(default=0, verbose_name="类型") #1为首页上方2为歌曲3为登录

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class UserFavorite(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    fav_id = models.IntegerField(verbose_name="数据id")
    fav_type = models.IntegerField(choices=((1, "音乐"), (2, "个人创作者")), default=1, verbose_name="收藏类型")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{user}_{id}".format(user=self.user.username, id=self.fav_id)



class WitchoutUserMusic(BaseModel):
    bought_address = models.CharField(max_length=42, verbose_name="购买钱包地址", default="", unique=True)
    purchase_bcId = models.CharField(verbose_name="购买凭证id", max_length=32, default='')
    purchase_transactionHash = models.CharField(verbose_name="交易hash", max_length=128, default='')
    product_bcId = models.CharField(verbose_name="购买版权id", max_length=32, default='')
    purchase_permission = models.IntegerField(default=0, verbose_name="购买的权限")
    purchase_isUpdate = models.IntegerField(verbose_name="是否升级", default=0)
    music_price = models.CharField(verbose_name="价格", max_length=128, default='')
    timestamp = models.CharField(verbose_name='上链时间戳', max_length=128, default='')
    class Meta:
        verbose_name = "系统外购买查看"
        verbose_name_plural = verbose_name


class UserMusic(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    music = models.ForeignKey(Music, on_delete=models.CASCADE, verbose_name="购买的音乐")
    purchase_bcId = models.CharField(verbose_name="购买凭证id", max_length=32, default='')
    purchase_transactionHash = models.CharField(verbose_name="交易hash", max_length=128, default='')
    purchase_permission = models.IntegerField(default=0, verbose_name="购买的权限")
    purchase_status = models.IntegerField(verbose_name="购买状态", default=0) #0未付款1未发送密钥服务器2成功3失效4为发送密钥升级5删除6退款
    purchase_isUpdate = models.IntegerField(verbose_name="是否升级", default=0)
    music_price = models.CharField(verbose_name="价格", max_length=128, default='')
    timestamp = models.CharField(verbose_name='上链时间戳', max_length=128, default='')
    key_ipfshash = models.CharField(verbose_name="keyipfshash", max_length=64, default='')
    projectname = models.CharField(verbose_name='授权项目名称',max_length=128,default='')

    class Meta:
        verbose_name = "用户系统购买管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.purchase_bcId

    def get_vailtime(self):
        # 已升级，版权无效
        if self.purchase_status == 0:
            return '未付款'
        elif (self.purchase_isUpdate != 0) & (self.purchase_isUpdate != int(self.purchase_bcId)):
            return '已升级，版权无效'
        elif self.purchase_status == 3:
            return '版权过期'
        elif self.purchase_status == 6:
            return '已退款'
        elif (int(self.purchase_permission) == 1) | (int(self.purchase_permission) == 5) | (
                int(self.purchase_permission) == 6):
            return '无限版权'
        # 返回剩余秒
        elif int(self.timestamp) + period_validity(int(self.purchase_permission)) >= int(time.time()):
            return sec_to_data(int(self.timestamp) + period_validity(int(self.purchase_permission)) - int(time.time()))
        # 版权失效
        else:
            return '版权失效'

    def check_vaild(self):
        if (int(self.purchase_permission) == 2) | (int(self.purchase_permission) == 3) | (
                int(self.purchase_permission) == 4):
            if (self.purchase_status == 2):
                if int(self.timestamp) + period_validity(int(self.purchase_permission)) < int(time.time()):
                    self.purchase_status = 3
                    self.save()

    def check_time(self):
        if self.purchase_status == 1:
            if int(self.timestamp) + 7200 < int(time.time()):
                return False
            return True
        return False

    def check_upload(self):
        if self.key_ipfshash == '':
            if self.purchase_status == 1:
                if int(self.timestamp) + 7200 < int(time.time()):
                    return True
                return False
            if self.purchase_status == 2:
                return True

