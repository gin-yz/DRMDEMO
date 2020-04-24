from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import View
from eth_account import Account
from ratelimit.decorators import ratelimit
from web3 import Web3
from apps.music.models import Music
from apps.operations.models import Banner, UserFavorite
from apps.users.forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm, ReloadCaptcha, UserInfoForm, \
    UploadImageForm, ChangePwdForm, ModifyFreestyleForm
from apps.users.models import UserProfile, EmailVerifyRecord, UserMessage
from apps.utils.email_send import send_register_eamil
from pure_pagination import Paginator, PageNotAnInteger
import json


class CustomAuth(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(email=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))

        banners = Banner.objects.filter(type=3).order_by("index")
        next = request.GET.get("next", "")
        login_form = LoginForm()
        return render(request, "login.html", {
            "login_form": login_form,
            "next": next,
            "banners": banners
        })

    def post(self, request, *args, **kwargs):
        # 表单验证
        login_form = LoginForm(request.POST)
        banners = Banner.objects.filter(type=3).order_by("index")
        if login_form.is_valid():
            # 用于通过用户和密码查询用户是否存在
            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=user_name, password=password)
            # 1. 通过用户名查询到用户
            # 2. 需要先加密再通过加密之后的密码查询
            # user = UserProfile.objects.get(username=user_name, password=password)
            if user is not None:
                # 查询到用户
                if user.is_active:
                    # 只有注册激活才能登录
                    login(request, user)
                    # 登录成功之后应该怎么返回页面
                    next = request.GET.get("next", "")
                    if next:
                        return HttpResponseRedirect(next)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    all_records = EmailVerifyRecord.objects.filter(email=user_name)
                    if all_records:
                        for record in all_records:
                            record.delete()
                    send_register_eamil(user.email, 'register')
                    return render(request, 'login.html',
                                  {'msg': '您的账户未激活，邮件已重发，请前往邮箱激活', 'login_form': login_form, "banners": banners})
            else:
                # 未查询到用户
                return render(request, "login.html", {"msg": "用户名或密码错误", "login_form": login_form, "banners": banners})
        else:
            return render(request, "login.html", {"login_form": login_form,
                                                  "banners": banners})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("index"))


class RegisterView(View):
    '''用户注册'''

    def get(self, request):
        register_form = RegisterForm()
        banners = Banner.objects.filter(type=3).order_by("index")
        return render(request, 'register.html', {'register_form': register_form, "banners": banners})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        banners = Banner.objects.filter(type=3).order_by("index")
        if register_form.is_valid():
            user_name = request.POST.get('email', None)
            # 如果用户已存在，则提示错误信息
            user_exist = UserProfile.objects.filter(email=user_name)
            if user_exist:
                if user_exist.first().is_active == False:
                    all_records = EmailVerifyRecord.objects.filter(email=user_name)
                    if all_records:
                        for record in all_records:
                            record.delete()
                    send_register_eamil(user_name, 'register')
                    return render(request, 'register.html',
                                  {'register_form': register_form, 'msg': '用户未激活，邮件已重发，请前往邮箱激活', "banners": banners})
                return render(request, 'register.html',
                              {'register_form': register_form, 'msg': '用户已存在', "banners": banners})

            pass_word = request.POST.get('password', None)
            # 实例化一个user_profile对象
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            # 对保存到数据库的密码加密
            user_profile.set_password(pass_word)
            user_profile.save()
            send_register_eamil(user_name, 'register')
            return render(request, 'register.html',
                          {'register_form': register_form, 'msg': '邮件已发送，请前往邮箱激活', "banners": banners})
        else:
            return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        # 查询邮箱验证记录是否存在
        all_record = EmailVerifyRecord.objects.filter(code=active_code).last()

        if all_record:
            # 获取到对应的邮箱
            email = all_record.email
            # 查找到邮箱对应的user
            user = UserProfile.objects.get(email=email)
            user.is_active = True
            user.save()
            message = UserMessage()
            message.user = user
            message.message = "欢迎您入驻区块链音乐版权平台！"
            message.has_read = False
            message.save()
        # 验证码不对的时候跳转到激活失败页面
        else:
            all_record.delete()
            return render(request, 'active_fail.html')
        # 激活成功跳转到登录页面
        login_form = LoginForm()
        banners = Banner.objects.filter(type=3).order_by("index")
        all_record.delete()
        return render(request, "login.html", {'msg': '您的账户已激活', 'login_form': login_form, "banners": banners})


class ForgetPwdView(View):
    '''找回密码'''

    def get(self, request):
        forget_form = ForgetPwdForm()
        banners = Banner.objects.filter(type=3).order_by("index")
        return render(request, 'forgetpwd.html', {'forget_form': forget_form, "banners": banners})

    def post(self, request):
        banners = Banner.objects.filter(type=3).order_by("index")
        forget_form = ForgetPwdForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email', None)
            send_register_eamil(email, 'forget')
            return render(request, 'forgetpwd.html',
                          {'forget_form': forget_form, 'msg': '邮件已发送，请查看邮箱', "banners": banners})
        else:
            return render(request, 'forgetpwd.html', {'forget_form': forget_form, "banners": banners})


class ResetView(View):
    def get(self, request, active_code):
        forget_form = ForgetPwdForm()
        banners = Banner.objects.filter(type=3).order_by("index")
        all_records = EmailVerifyRecord.objects.filter(code=active_code).last()
        if all_records:
            email = all_records.email
            return render(request, "password_reset.html", {"active_code": active_code, 'email': email})
        else:
            return render(request, 'forgetpwd.html',
                          {'forget_form': forget_form, 'msg': '链接失效，请再次发送邮件', "banners": banners})


class ModifyPwdView(View):
    def post(self, request):
        forget_form = ForgetPwdForm()
        banners = Banner.objects.filter(type=3).order_by("index")
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            active_code = request.POST.get("active_code", "")
            if pwd1 != pwd2:
                return render(request, "password_reset.html",
                              {"email": email, "active_code": active_code, "msg": "两次输入密码不一致！"})
            all_records = EmailVerifyRecord.objects.filter(code=active_code).last()
            if all_records.email != email:
                all_records.delete()
                return render(request, 'forgetpwd.html',
                              {'forget_form': forget_form, 'msg': '发生未知错误，请再次发送邮件', "banners": banners})
            user = UserProfile.objects.filter(email=email).first()
            if user:
                user.set_password(pwd2)
                user.save()
            else:
                user_profile = UserProfile()
                user_profile.username = email
                user_profile.email = email
                user_profile.is_active = True
                user_profile.set_password(pwd2)
                user_profile.save()
            login_form = LoginForm()
            banners = Banner.objects.filter(type=3).order_by("index")
            all_records.delete()
            return render(request, "login.html", {'msg': '密码成功重置', 'login_form': login_form, "banners": banners})
        else:
            email = request.POST.get("email", "")
            active_code = request.POST.get("active_code", "")
            return render(request, "password_reset.html",
                          {"email": email, "active_code": active_code, "modify_form": modify_form})


class UserInfoView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "info"
        captcha_form = ReloadCaptcha()
        return render(request, "usercenter-info.html", {
            "captcha_form": captcha_form,
            "current_page": current_page,
        })

    @ratelimit(key='ip', rate='3/1800s', block=True)
    def post(self, request, *args, **kwargs):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            address = user_info_form.cleaned_data['address']
            if not Web3.isChecksumAddress(address):
                return JsonResponse({
                    "status": 'fail',
                    "msg": "地址格式不对！"
                })
            user_info_form.save()
            return JsonResponse({
                "status": "success",
            })
        else:
            return JsonResponse(user_info_form.errors)


class UploadImageView(LoginRequiredMixin, View):
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        # 处理用户上传的头像
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail"
            })


class ChangePwdView(LoginRequiredMixin, View):
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        pwd_form = ChangePwdForm(request.POST)
        if pwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")

            if pwd1 != pwd2:
                return JsonResponse({
                    "status": "fail",
                    "msg": "密码不一致"
                })
            user = request.user
            user.set_password(pwd1)
            user.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(pwd_form.errors)


class SendEmailCodeView(LoginRequiredMixin, View):
    '''发送邮箱修改验证码'''

    def get(self, request):
        email = request.GET.get('email', '')

        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已存在"}', content_type='application/json')

        send_register_eamil(email, 'update_email')
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    '''修改邮箱'''

    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")
        existed_records = EmailVerifyRecord.objects.filter(email=email, code=code, send_type='update_email')
        if existed_records:
            user = request.user
            user.email = email
            user.username = email
            user.save()
            for record in existed_records:
                record.delete()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码无效"}', content_type='application/json')


class UpdateKeyView(LoginRequiredMixin, View):
    def post(self, request):
        captcha_form = ReloadCaptcha(request.POST)
        if captcha_form.is_valid():
            one = request.POST.get('one')
            print(one)
            if one:
                return JsonResponse({
                    'msg': 'ok',
                })
        else:
            return JsonResponse(captcha_form.errors)


class UpdateKeyValueView(LoginRequiredMixin, View):
    def post(self, request):
        value = request.POST.get('value')
        print(value)
        account = Account.create()
        print('private => {0}'.format(account._key_obj))
        print('public  => {0}'.format(account._key_obj.public_key))
        print('address => {0}'.format(account.address))
        user = request.user
        user.address = account.address
        user.publickey = account._key_obj.public_key
        user.save()
        wallet = Account.encrypt(account.privateKey, value)
        response = HttpResponse(content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename=%s.json' % (account.address)
        response.write(json.dumps(wallet))
        return response


class MusicianListView(View):
    def get(self, request, *args, **kwargs):
        all_musicians = UserProfile.objects.filter(is_producter=True)
        musician_nums = all_musicians.count()

        hot_musicians = sorted(all_musicians, key=lambda i: i.hot_num(), reverse=True)[:5]

        keywords = request.GET.get("keywords", "")
        s_type = "musician"
        if keywords:
            all_musicians = all_musicians.filter(is_producter=True).filter(
                Q(nick_name__contains=keywords) | Q(points__contains=keywords) | Q(description__contains=keywords))

        # 对音乐家进行排序
        sort = request.GET.get("sort", "")
        if sort == "hot":
            all_musicians = sorted(all_musicians, key=lambda i: i.hot_num(), reverse=True)
        if sort == "click":
            all_musicians = all_musicians.order_by("-click_nums")
        if sort == "buy":
            all_musicians = sorted(all_musicians, key=lambda i: i.get_all_sell_num(), reverse=True)
        if sort == 'save':
            all_musicians = all_musicians.order_by('-fav_nums')

        # 对音乐家数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_musicians, per_page=10, request=request)
        musicians = p.page(page)

        return render(request, "teachers-list.html", {
            "musicians": musicians,
            "musician_nums": musician_nums,
            "sort": sort,
            "hot_musicians": hot_musicians,
            "keywords": keywords,
            "s_type": s_type
        })


class MusicianDetailView(View):
    def get(self, request, musician_id, *args, **kwargs):
        musician = UserProfile.objects.get(id=int(musician_id))

        musician_fav = False
        org_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_type=2, fav_id=musician.id):
                musician_fav = True
            if UserFavorite.objects.filter(user=request.user, fav_type=1, fav_id=musician.id):
                org_fav = True

        all_musicians = UserProfile.objects.filter(is_producter=True)
        hot_musicians = sorted(all_musicians, key=lambda i: i.hot_num(), reverse=True)[:5]
        music_list = musician.music_set.all()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(music_list, per_page=8, request=request)
        music_list = p.page(page)
        return render(request, "teacher-detail.html", {
            "musician": musician,
            "musician_fav": musician_fav,
            "hot_musicians": hot_musicians,
            "music_list": music_list,
            "s_type": 'musician',
        })


class MyFavView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfav"
        music_list = []
        fav_musics = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_music in fav_musics:
            music = Music.objects.filter(id=fav_music.fav_id)
            if music:
                music_list.append(music.first())

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(music_list, per_page=5, request=request)
        music_list = p.page(page)

        return render(request, "usercenter-fav-org.html", {
            "music_list": music_list,
            "current_page": current_page
        })


class MyFavMusicianView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfav_musician"
        musicians_list = []
        fav_musicians = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_musician in fav_musicians:
            musician = UserProfile.objects.get(id=fav_musician.fav_id)
            musicians_list.append(musician)

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(musicians_list, per_page=5, request=request)
        musicians_list = p.page(page)

        return render(request, "usercenter-fav-teacher.html", {
            "musician_list": musicians_list,
            "current_page": current_page,
        })

class MyMessageView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        messages = UserMessage.objects.filter(user=request.user)
        current_page = "message"
        for message in messages:
            message.has_read = True
            message.save()

        # 对讲师数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(messages, per_page=1, request=request)
        messages = p.page(page)

        return render(request, "usercenter-message.html",{
            "messages":messages,
            "current_page":current_page
        })

class ModifyFreestyle(LoginRequiredMixin,View):
    login_url = "/login/"
    @ratelimit(key='ip', rate='1/300s', block=True)
    def post(self, request):
        modifyfreestyle = ModifyFreestyleForm(request.POST)
        if modifyfreestyle.is_valid():
            request.user.points = modifyfreestyle.cleaned_data['points']
            request.user.description = modifyfreestyle.cleaned_data['description']
            request.user.save()
            return JsonResponse({
                'status':'success',
                'msg':'修改成功！'
            })
        else:
            return JsonResponse({
                'status':'fail',
                'msg':','.join(modifyfreestyle.errors)
            })