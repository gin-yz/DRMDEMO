# users/forms.py
import re

from django import forms
from captcha.fields import CaptchaField
from .models import UserProfile


class LoginForm(forms.Form):
    '''登录验证表单'''
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})
    # def clean_username(self):
    #     mobile = str(self.data.get("mobile"))
    #     regex_mobile = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"
    #     regex_email = "^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$"
    #     p_mobile = re.compile(regex_mobile)
    #     p_email = re.compile(regex_email)
    #     if p_mobile.match(mobile):
    #         return mobile
    #     elif p_email.match(mobile):
    #         return mobile
    #     else:
    #         forms.ValidationError("账号格式输入错误")


class RegisterForm(forms.Form):
    '''注册验证表单'''
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=5)
    # 验证码
    captcha = CaptchaField(error_messages={'invalid':'验证码错误'})

class ForgetPwdForm(forms.Form):
    '''忘记密码'''
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})

class ReloadCaptcha(forms.Form):
    "重新注入验证码"
    value = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField()

class ModifyPwdForm(forms.Form):
    '''重置密码'''
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UploadImageForm(forms.ModelForm):
    '''用户更改图像'''
    class Meta:
        model = UserProfile
        fields = ['image']

class UserInfoForm(forms.ModelForm):

    '''个人中心信息修改'''
    class Meta:
        model = UserProfile
        fields = ['nick_name','gender','birthday','mobile','address','publickey']


class ChangePwdForm(forms.Form):
    password1 = forms.CharField(required=True,min_length=5,max_length=26)
    password2 = forms.CharField(required=True,min_length=5,max_length=26)

    # def clean(self):
    #     pwd1 = self.cleaned_data["password1"]
    #     pwd2 = self.cleaned_data["password2"]
    #     if pwd1 != pwd2:
    #         raise forms.ValidationError("密码不一致")
    #
    #     return self.cleaned_data

class ModifyFreestyleForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ["points","description"]
