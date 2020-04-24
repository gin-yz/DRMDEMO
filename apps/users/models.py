from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from functools import reduce
GENDER_CHOICES = (
    ("male", "男"),
    ("female", "女")
)


class BaseModel(models.Model):
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        abstract = True


class WithoutUserProfile(BaseModel):
    address = models.CharField(max_length=42, verbose_name="账户地址", default="", unique=True)
    is_producter = models.BooleanField(verbose_name='是否版权发布者', default=False)


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=10, verbose_name="昵称", default="")
    birthday = models.DateField(verbose_name="生日", null=True, blank=True)
    gender = models.CharField(verbose_name="性别", choices=GENDER_CHOICES, max_length=6)
    address = models.CharField(max_length=42, verbose_name="账户地址", null=True, unique=True)
    publickey = models.CharField(max_length=130, verbose_name="账户公钥", default="", )
    mobile = models.CharField(max_length=11, verbose_name="手机号码")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    image = models.ImageField(verbose_name="用户头像", upload_to="head_image/%Y/%m", default="head_image/default.jpg")
    is_producter = models.BooleanField(verbose_name='是否版权发布者', default=False)
    points = models.CharField(max_length=20, verbose_name="作曲风格", default='')
    description = models.CharField(max_length=50, verbose_name="个人描述", default='')


    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    # def unread_nums(self):
    #     #未读消息数量
    #     return self.usermessage_set.filter(has_read=False).count()

    def __str__(self):
        if self.nick_name:
            return self.nick_name
        else:
            return self.username

    # 代表歌曲
    def get_represent_music(self):
        all_music = self.music_set.filter(music_status=True)
        if all_music:
            all_music = sorted(all_music, key=lambda i: i.all_sell_count(), reverse=True)[0:3]
            return all_music
        else:
            return all_music

    # 所有歌曲数量
    def get_all_music_num(self):
        return self.music_set.all().count()

    # 所有歌曲销量
    def get_all_sell_num(self):
        music_list = self.music_set.all()
        all_num = 0
        for music in music_list:
            all_num += music.all_sell_count()
        return all_num

    # 所有歌曲销售金额
    def get_all_money(self):
        music_list = self.music_set.all()
        all_money = 0
        for music in music_list:
            all_money += float(music.all_sell_money())
        return all_money

    # 热度
    def hot_num(self):
        return 0.6 * self.get_all_sell_num() + 0.2 * self.click_nums + 0.2 * self.fav_nums

class ProductUser(UserProfile):
    class Meta:
        verbose_name = "音乐制作人"
        verbose_name_plural = verbose_name
        proxy = True


class UserMessage(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    message = models.CharField(max_length=200, verbose_name="消息内容")
    has_read = models.BooleanField(default=False, verbose_name="是否已读")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message

class EmailVerifyRecord(models.Model):
    send_choices = (
        ('register', '注册'),
        ('forget', '找回密码'),
        ('update_email', '修改邮箱')
    )

    code = models.CharField('验证码', max_length=20)
    email = models.EmailField('邮箱', max_length=50)
    send_type = models.CharField(choices=send_choices, max_length=30)
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = '邮箱验证码'
        verbose_name_plural = verbose_name
