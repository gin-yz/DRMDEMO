from django import forms

from apps.music.models import Music
from django.forms import fields
from apps.users.models import EmailVerifyRecord
from .models import Banner, UserFavorite


class UEditorForm(forms.ModelForm):
    class Meta:
        model = Music
        fields = ['music_detail']


class UploadOneForm(forms.ModelForm):
    demoLinkfile = fields.FileField()
    hashLinkfile = fields.FileField()
    music_tags = forms.CharField(required=True)
    address = forms.CharField(required=True, max_length=42, min_length=42)
    music_price1 = forms.DecimalField(required=True)
    music_price2 = forms.DecimalField(required=True, max_digits=256, decimal_places=5)
    music_price3 = forms.DecimalField(required=True, max_digits=256, decimal_places=5)
    music_price4 = forms.DecimalField(required=True, max_digits=256, decimal_places=5)
    music_price5 = forms.DecimalField(required=True, max_digits=256, decimal_places=5)
    music_price6 = forms.DecimalField(required=True, max_digits=256, decimal_places=5)

    # 上传阶段一
    class Meta:
        model = Music
        fields = ['music_desc', 'image', 'music_name', 'music_desc', 'music_times', 'music_detail', 'keyfile']


class UploadTwoForm(forms.Form):
    transactionHash = forms.CharField(required=True)
    blockNumber = forms.CharField(required=True)
    transactionIndex = forms.CharField(required=True)
    keyfile = fields.FileField()
    hashLinkfileHash = forms.CharField(required=True)


class UploadFileForm(forms.Form):
    ipfs_file = fields.FileField()


class PurchaseOneForm(forms.Form):
    music_bcId = forms.CharField(max_length=32, required=True)
    purchase_permission = forms.IntegerField(required=True)
    price = forms.CharField(max_length=128, required=True)
    projectname = forms.CharField(max_length=128, required=False)


class PurchaseTwoForm(forms.Form):
    transactionHash = forms.CharField(required=True)
    transactionIndex = forms.CharField(required=True)
    blockNumber = forms.CharField(required=True)
    music_bcId = forms.CharField(max_length=32, required=True)
    purchase_permission = forms.IntegerField(required=True)
    purchase_music_id = forms.CharField(max_length=128, required=True)


class UpdateMyPermissionOneForm(forms.Form):
    id = forms.IntegerField(required=True)


class UpdateMyPermissionTwoForm(forms.Form):
    transactionHash = forms.CharField(required=True)
    transactionIndex = forms.CharField(required=True)
    blockNumber = forms.CharField(required=True)
    old_music = forms.CharField(max_length=128, required=True)
    purchase_permission = forms.IntegerField(required=True)
    price = forms.CharField(max_length=128, required=True)


class DownloadKeyForm(forms.Form):
    music_id = forms.CharField(max_length=128, required=True)


class UserFavForm(forms.ModelForm):
    class Meta:
        model = UserFavorite
        fields = ["fav_id", "fav_type"]


class ModifyMusicForm(forms.Form):
    transactionHash = forms.CharField(required=True)
    transactionIndex = forms.CharField(required=True)
    blockNumber = forms.CharField(required=True)
    music_bcId = forms.CharField(max_length=32, required=True)


class RefundMusicForm(forms.Form):
    transactionHash = forms.CharField(required=True)
    transactionIndex = forms.CharField(required=True)
    blockNumber = forms.CharField(required=True)
    music_bcId = forms.CharField(max_length=32, required=True)
