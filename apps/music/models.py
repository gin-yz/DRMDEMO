from django.db import models

# Create your models here.
from django.db.models import Q

from apps.users.models import BaseModel, UserProfile
from DjangoUeditor.models import UEditorField

commissionCharge = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06]


class WithoutMusic(BaseModel):
    owneraddress = models.CharField(max_length=42, verbose_name="账户地址", default="")
    music_transactionHash = models.CharField(verbose_name="交易hash", max_length=128)
    music_name = models.CharField(verbose_name="歌曲名", max_length=50, blank=False)
    music_desc = models.CharField(verbose_name="歌曲描述", max_length=300)
    music_bcId = models.CharField(verbose_name="歌曲上链id", max_length=32)
    music_status = models.BooleanField(verbose_name="歌曲状态", default=True)
    music_price1 = models.CharField(verbose_name="个人价格", max_length=128, default='')
    music_price2 = models.CharField(verbose_name="版权价格1", max_length=128, default='')
    music_price3 = models.CharField(verbose_name="版权价格2", max_length=128, default='')
    music_price4 = models.CharField(verbose_name="版权价格3", max_length=128, default='')
    music_price5 = models.CharField(verbose_name="版权价格4", max_length=128, default='')
    music_price6 = models.CharField(verbose_name="版权价格5", max_length=128, default='')
    music_hashLink = models.CharField(verbose_name="ipfshash", max_length=64)
    music_demoLink = models.CharField(verbose_name="ipfs试听音乐hash", max_length=64)

    class Meta:
        verbose_name = "未归入系统音乐"
        verbose_name_plural = verbose_name


class Music(BaseModel):
    owner = models.ForeignKey(UserProfile, null=True, blank=True, on_delete=models.CASCADE, verbose_name="版权拥有者")
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    music_detail = UEditorField(verbose_name="歌曲详情", width=900, height=300, imagePath="music/ueditor/images/",
                                filePath="music/ueditor/files/", default="")
    is_banner = models.BooleanField(default=False, verbose_name="是否广告位")
    image = models.ImageField(upload_to="music/%Y/%m", verbose_name="封面图", max_length=100)
    music_transactionHash = models.CharField(verbose_name="交易hash", max_length=128)

    music_name = models.CharField(verbose_name="歌曲名", max_length=50, blank=False)
    music_desc = models.CharField(verbose_name="歌曲描述", max_length=300)
    music_times = models.IntegerField(default=0, verbose_name="歌曲时长(秒)")
    music_bcId = models.CharField(verbose_name="歌曲上链id", max_length=32)
    music_status = models.IntegerField(verbose_name="歌曲状态", default=0)
    music_price1 = models.CharField(verbose_name="个人价格", max_length=128, default='')
    music_price2 = models.CharField(verbose_name="版权价格1", max_length=128, default='')
    music_price3 = models.CharField(verbose_name="版权价格2", max_length=128, default='')
    music_price4 = models.CharField(verbose_name="版权价格3", max_length=128, default='')
    music_price5 = models.CharField(verbose_name="版权价格4", max_length=128, default='')
    music_price6 = models.CharField(verbose_name="版权价格5", max_length=128, default='')
    music_hashLink = models.CharField(verbose_name="ipfshash", max_length=64)
    music_demoLink = models.CharField(verbose_name="ipfs试听音乐hash", max_length=64)
    keyfile = models.FileField(verbose_name='上传加密文件', upload_to='music/key/%Y/%m', default='')

    class Meta:
        verbose_name = "音乐版权信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.music_name

    def music_tag(self):
        return self.musictag_set.all()[:5]

    def show_image(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<img src='{}'>".format(self.image.url))

    show_image.short_description = "图片"

    def hot_num(self):
        return 0.6 * self.all_sell_count() + 0.2 * self.fav_nums + 0.2 * self.click_nums

    # 这首歌售出盈利
    def all_sell_money(self):
        usermusic_list = self.usermusic_set.filter(purchase_status=2)
        all_money = 0
        for usermusic in usermusic_list:
            all_money += float(usermusic.music_price) - commissionCharge[usermusic.purchase_permission - 1]
        return all_money

    def all_sell_count(self):

        music_list = self.usermusic_set.filter(purchase_status=2)
        return len(music_list)


class BannerMusic(Music):
    class Meta:
        verbose_name = "首页推荐音乐"
        verbose_name_plural = verbose_name
        proxy = True


class MusicTag(BaseModel):
    music = models.ForeignKey(Music, on_delete=models.CASCADE, verbose_name="歌曲")
    tag = models.IntegerField(verbose_name="标签")

    class Meta:
        verbose_name = "歌曲标签"
        verbose_name_plural = verbose_name

    def __int__(self):
        return self.tag

    def show_name(self):
        tag_list = ['古典', '爵士', '摇滚', '放克', '后摇', '电子', '嘻哈', '乡村', '蓝草', '民谣', '拉丁', '雷鬼', '氛围', '古风', '迪斯科', '重金属',
                    '轻音乐', '中国风', '管弦乐', '布鲁斯', '巴洛克', '新民乐', '新时代', '车库', '拉格泰姆', '摇摆爵士', '酷爵士乐', '比波普爵士', '神游舞曲',
                    'EDM', 'House', 'Trap', 'R&B']
        return tag_list[self.tag - 1]


class MusicComments(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    music = models.ForeignKey(Music, on_delete=models.CASCADE, verbose_name="音乐")
    comments = models.CharField(max_length=200, verbose_name="评论内容")

    class Meta:
        verbose_name = "音乐评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comments
