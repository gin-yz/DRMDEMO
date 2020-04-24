from django.contrib.auth.mixins import LoginRequiredMixin
from pure_pagination import Paginator, PageNotAnInteger
from django.db.models import Q, F
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, reverse
from django.views.generic import View
import ipfshttpclient, json
from ratelimit.decorators import ratelimit
from web3 import Web3
from apps.music.models import Music, MusicTag, MusicComments
from apps.operations.forms import UploadOneForm, UploadTwoForm, PurchaseOneForm, PurchaseTwoForm, \
    UpdateMyPermissionOneForm, UpdateMyPermissionTwoForm, DownloadKeyForm, UserFavForm, ModifyMusicForm, UEditorForm, \
    UploadFileForm, RefundMusicForm
from apps.operations.models import UserMusic, UserFavorite, Banner
from apps.users.models import UserProfile
from apps.operations.tasks import uploadKeyFile, productSoldDetail, sendKey

client = ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001/http')


class IndexView(View):
    def get(self, request, *args, **kwargs):
        banners_top = Banner.objects.filter(type=1).order_by("index")
        banners_musics = Banner.objects.filter(type=2).order_by("index")
        recommand_musics = Music.objects.filter(is_banner=True)[:6]
        users = UserProfile.objects.all()[:15]
        return render(request, "index.html", {
            "banners_top": banners_top,
            "recommand_musics": recommand_musics,
            "banners_musics": banners_musics,
            "users": users,
            "s_type": "music"
        })


def loadcontact(w3, contract):
    fn_abi = 'F:\\onedrive\\blockchain\\code\\final\\demo\\{0}.abi'.format(contract)
    fn_addr = 'F:\\onedrive\\blockchain\\code\\final\\demo\\{0}.addr'.format(contract)

    with open(fn_abi) as f:
        abi = json.load(f)

    with open(fn_addr) as f:
        addr = f.read()
        addr = Web3.toChecksumAddress(addr.lower())

    return w3.eth.contract(address=addr, abi=abi)


w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
action = loadcontact(w3, 'cys')


class UploadMusicView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "uploadmusic"
        ueditorform = UploadOneForm()
        return render(request, 'usercenter-upload-music.html', {
            "current_page": current_page,
            'form': ueditorform,
        })


class UploadOneView(LoginRequiredMixin, View):
    login_url = "/login/"

    def post(self, request):
        uploadone_form = UploadOneForm(request.POST, request.FILES, instance=request.user)
        if uploadone_form.is_valid():

            # 钱包验证
            address = uploadone_form.cleaned_data['address']
            if request.user.address.lower() != address:
                return JsonResponse({'errormsg': "付款钱包与账户钱包不一致！"})

            # ipfs上传
            demoLinkfile = uploadone_form.cleaned_data['demoLinkfile']
            hashLinkfile = uploadone_form.cleaned_data['hashLinkfile']
            demoLinkfileHash = client.add(demoLinkfile, recursive=True)
            hashLinkfileHash = client.add(hashLinkfile, recursive=True)
            fileHash_filter = Music.objects.filter(music_hashLink=hashLinkfileHash['Hash'])
            if fileHash_filter:
                if fileHash_filter.first().music_status == 1:
                    return JsonResponse({'errormsg': '该文件已上传'})
                elif fileHash_filter.first().music_bcId:
                    return JsonResponse({'errormsg': '请您对该文件重新加密后上传'})
            # print(demoLinkfileHash['Hash'], hashLinkfileHash['Hash'])

            # 价格转list
            price_list = []
            music_price1 = uploadone_form.cleaned_data['music_price1']
            music_price2 = uploadone_form.cleaned_data['music_price2']
            music_price3 = uploadone_form.cleaned_data['music_price3']
            music_price4 = uploadone_form.cleaned_data['music_price4']
            music_price5 = uploadone_form.cleaned_data['music_price5']
            music_price6 = uploadone_form.cleaned_data['music_price6']
            price_list.append(str(Web3.toWei(music_price1, 'ether')))
            price_list.append(str(Web3.toWei(music_price2, 'ether')))
            price_list.append(str(Web3.toWei(music_price3, 'ether')))
            price_list.append(str(Web3.toWei(music_price4, 'ether')))
            price_list.append(str(Web3.toWei(music_price5, 'ether')))
            price_list.append(str(Web3.toWei(music_price6, 'ether')))

            # 转utf8
            music_name_utf8 = ''
            music_desc_utf8 = ''
            music_name = uploadone_form.cleaned_data['music_name']
            music_desc = uploadone_form.cleaned_data['music_desc']
            for item in music_name:
                music_name_utf8 += item.encode('unicode_escape').decode('utf-8')
            for item in music_desc:
                music_desc_utf8 += item.encode('unicode_escape').decode('utf-8')
            # print(music_name_utf8, music_desc_utf8)

            # 保存数据库
            if not fileHash_filter:
                musicone = Music()
            else:
                musicone = Music.objects.filter(music_hashLink=hashLinkfileHash['Hash']).first()
            musicone.music_name = music_name
            musicone.music_desc = music_desc
            musicone.music_price1 = music_price1
            musicone.music_price2 = music_price2
            musicone.music_price3 = music_price3
            musicone.music_price4 = music_price4
            musicone.music_price5 = music_price5
            musicone.music_price6 = music_price6
            musicone.image = uploadone_form.cleaned_data['image']
            musicone.music_hashLink = hashLinkfileHash['Hash']
            musicone.music_demoLink = demoLinkfileHash['Hash']
            musicone.keyfile = uploadone_form.cleaned_data['keyfile']
            musicone.owner = request.user
            musicone.music_times = uploadone_form.cleaned_data['music_times']
            musicone.music_status = 2
            musicone.music_detail = uploadone_form.cleaned_data['music_detail']
            musicone.save()

            # 标签保存
            music_tags = uploadone_form.cleaned_data['music_tags']
            if len(music_tags.split(",")) > 5:
                return JsonResponse({'errormsg': '标签数量应小于5个'})
            musicmodel = Music.objects.filter(music_hashLink=hashLinkfileHash['Hash']).first()
            if not fileHash_filter:
                if music_tags:
                    for tag in music_tags.split(","):
                        tsgmodel = MusicTag()
                        tsgmodel.music = musicmodel
                        tsgmodel.tag = int(tag)
                        tsgmodel.save()
            else:
                old_tags = MusicTag.objects.filter(music=musicmodel)
                old_tags.delete()
                if music_tags:
                    for tag in music_tags.split(","):
                        tsgmodel = MusicTag()
                        tsgmodel.music = musicmodel
                        tsgmodel.tag = int(tag)
                        tsgmodel.save()

            return JsonResponse({
                'demoLinkfileHash': demoLinkfileHash['Hash'],
                'hashLinkfileHash': hashLinkfileHash['Hash'],
                'msg': 'success',
                'price_list': price_list,
                'music_name_utf8': music_name_utf8,
                'music_desc_utf8': music_desc_utf8,
            })
        else:
            # print(uploadone_form.errors)
            return JsonResponse(uploadone_form.errors)


class UploadFileView(LoginRequiredMixin, View):
    login_url = "/login/"

    def post(self, request):
        uploadfile_form = UploadFileForm(request.POST, request.FILES)
        if uploadfile_form.is_valid():
            ipfs_file = request.FILES.get('ipfs_file')
            fileHash = client.add(ipfs_file, recursive=True)

            return JsonResponse({"status": "success", 'msg': "文件上传成功", "fileHash": fileHash})

        else:
            return JsonResponse(uploadfile_form.errors)


class PurchaseOneView(View):
    def post(self, request, *args, **kwargs):
        """
               用户购买，
               """
        # 先判断用户是否登录
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录"
            })

        pur_one_form = PurchaseOneForm(request.POST)
        if pur_one_form.is_valid():
            music_bcId = pur_one_form.cleaned_data['music_bcId']
            purchase_permission = pur_one_form.cleaned_data['purchase_permission']
            price = pur_one_form.cleaned_data['price']
            projectname = pur_one_form.cleaned_data['projectname']
            print(projectname)
            if (int(purchase_permission) != 1) & (projectname == ''):
                return JsonResponse({"status": "fail",
                                     "msg": '请填写授权项目名称！'})
            address = request.POST.get('address', '')
            if request.user.address.lower() != address:
                return JsonResponse({"status": "fail",
                                     "msg": '付款钱包与账户钱包不一致！'})
            # # 自己不能买自己的
            music_own = Music.objects.filter(owner_id=int(request.user.id)).filter(music_bcId=int(music_bcId))
            if music_own:
                return JsonResponse({
                    "status": "fail",
                    "msg": "不能买自己的版权"
                })

            music_buy = Music.objects.filter(music_bcId=int(music_bcId)).first()
            purchase_music = UserMusic()
            purchase_music.user = request.user
            purchase_music.music = music_buy
            purchase_music.purchase_permission = int(purchase_permission)
            pur_one_form.projectname = projectname
            purchase_music.music_price = str(price)
            purchase_music.save()

            project_name_utf8 = ''
            for item in projectname:
                project_name_utf8 += item.encode('unicode_escape').decode('utf-8')
            print(project_name_utf8)

            return JsonResponse({
                "status": "success",
                'music_bcId': int(music_bcId),
                'purchase_permission': int(purchase_permission),
                'purchase_music_id': purchase_music.id,
                'money': int(str(Web3.toWei(price, 'ether'))),
                'project_name_utf8': project_name_utf8
            })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": '参数错误'
            })


class MyPurMusicView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        music_list = []
        pur_musics = UserMusic.objects.filter(user=request.user).order_by('-add_time')
        # for music in pur_musics:
        #     music.check_vaild()
        #     if music.check_upload():
        #         uploadKeyFile.apply_async(args=(music.user.address, music.user.publickey, music.purchase_bcId))
        #         music.key_ipfshash = "padding"
        #         music.save()

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # p0 = Paginator(list_vaild, per_page=4, request=request)
        p = Paginator(pur_musics, per_page=5, request=request)
        # list_cut_vaild = p0.page(page)
        my_musics = p.page(page)
        # lst_objects = zip(my_musics.object_list, list_cut_vaild.object_list)
        return render(request, "usercenter-mymusic.html", {
            "all_my_musics": my_musics,
            "current_page": 'mycourse',
            # 'lst_objects':lst_objects,
        })


class UpdateMyPermissionOneView(LoginRequiredMixin, View):
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        update_one_form = UpdateMyPermissionOneForm(request.POST)
        if update_one_form.is_valid():
            id = update_one_form.cleaned_data['id']
            old_music = UserMusic.objects.filter(id=int(id)).filter(Q(purchase_status=2) | Q(purchase_status=1)).last()
            comments = MusicComments.objects.filter(music=old_music.music).order_by('-add_time')
            is_comment = request.POST.get('is_comment', 'False')
            if old_music.purchase_isUpdate:
                if old_music.purchase_isUpdate != int(old_music.purchase_bcId):
                    return HttpResponseRedirect(reverse('users:mypurchase_music'))
            if int(id) == 6:
                return HttpResponseRedirect(reverse('users:mypurchase_music'))
            if old_music.user != request.user:
                return HttpResponseRedirect(reverse('music:detail', kwargs={'music_id': old_music.music_id}))
            old_permit = int(old_music.purchase_permission)
            old_permit_list = [0, 0, 0, 0, 0, 0]
            for i in range(0, int(old_permit)):
                old_permit_list[i] = 1

            music = old_music.music
            # 获取收藏状态
            has_fav_music = False
            has_fav_composer = False
            if request.user.is_authenticated:
                if UserFavorite.objects.filter(user=request.user, fav_id=music.id, fav_type=1):
                    has_fav_music = True
                if UserFavorite.objects.filter(user=request.user, fav_id=music.owner.id, fav_type=2):
                    has_fav_composer = True

            # 通过音乐的tag做音乐的推荐
            tags = music.musictag_set.all()
            tag_list = [tag.tag for tag in tags]
            music_tags = MusicTag.objects.filter(tag__in=tag_list).exclude(music__id=music.id)
            related_music = set()
            for course_tag in music_tags:
                related_music.add(course_tag.music)

            return render(request, "course-update.html", {
                "music": music,
                "has_fav_music": has_fav_music,
                "has_fav_composer": has_fav_composer,
                "related_music": related_music,
                'old_permit_list': old_permit_list,
                'selectlist': int(old_permit),
                "old_music": old_music,
                'is_comment': is_comment,
                'comments': comments,
            })


class PurDetialDownView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        usermusic_id = request.GET.get('id')
        usermusic = UserMusic.objects.filter(id=int(usermusic_id)).first()
        if usermusic.user != request.user:
            return HttpResponse('警告，请不要发送无端请求')

        transactiondetial = w3.eth.getTransaction(usermusic.purchase_transactionHash)
        PurchaseStorage = action.functions.getPurchaseStorageById(int(usermusic.purchase_bcId)).call(
            {'from': request.user.address})
        ProductStorage = action.functions.getProductStorageById(int(usermusic.music.music_bcId)).call(
            {'from': request.user.address})
        recipt = [
            'prodcut id:%s' % usermusic.music.music_bcId,
            'product name with utf-8:%s' % ProductStorage[0],
            'product ipfs file hash:%s' % ProductStorage[1],
            'product ipfs audition hash:%s' % ProductStorage[2],
            'product status:%s' % ProductStorage[3],
            "product description with utf-8:%s" % ProductStorage[5],
            'purchase id:%s' % usermusic.purchase_bcId,
            'music perimission:%s' % PurchaseStorage[1],
            'purchase timestamp:%s' % PurchaseStorage[2],
            'purchase address:%s' % PurchaseStorage[3],
            'purchase update:%s' % PurchaseStorage[4],
            'transactionHash:%s' % usermusic.purchase_transactionHash,
            'nonce:%s' % transactiondetial['nonce'],
            'blockHash:%s' % transactiondetial['blockHash'].hex(),
            'blockNumber:%s' % transactiondetial['blockNumber'],
            'transactionIndex:%s' % transactiondetial['transactionIndex'],
            'value(wei):%s' % transactiondetial['value'],
            'gas:%s' % transactiondetial['gas'],
            'gasPrice:%s' % transactiondetial['gasPrice']
        ]
        # print(transactiondetial,PurchaseStorage)
        response = HttpResponse(content_type='application/txt')
        response['Content-Disposition'] = 'attachment; filename=%s.txt' % (usermusic.purchase_transactionHash)
        for line in recipt:
            response.write(line + '\n')
        return response


class DownloadKeyView(LoginRequiredMixin, View):
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        music_from = DownloadKeyForm(request.POST)
        if music_from.is_valid():
            music_id = music_from.cleaned_data['music_id']
            music_objects = UserMusic.objects.filter(id=int(music_id)).filter(user=request.user)
            if not music_objects:
                return JsonResponse({
                    "status": "fail",
                    "msg": '您还未购买'})
            bought_music = music_objects.last()
            bought_music.check_vaild()
            if bought_music.purchase_status == 3:
                return JsonResponse({
                    "status": "fail",
                    "msg": '您的版权已失效'})
            if bought_music.key_ipfshash == '':
                # 传送密钥服务器
                uploadKeyFile.apply_async(
                    args=(request.user.address, request.user.publickey, bought_music.purchase_bcId,
                          bought_music.music.music_bcId))
                bought_music.key_ipfshash = "padding"
                bought_music.save()
                return JsonResponse({
                    "status": "fail",
                    "msg": "您已完成购买，后台服务器正在处理，请耐心等待"})
            elif (bought_music.key_ipfshash == "padding"):
                return JsonResponse({
                    "status": "fail",
                    "msg": "您已完成购买，后台服务器正在处理，请稍后再试"})
            else:
                sendKey.delay(bought_music.purchase_bcId,bought_music.key_ipfshash,bought_music.user.email)
                return JsonResponse({
                    "status": "success",
                    'msg':"您的密钥文件已发至您的邮箱，请注意查收！页面即将跳转展示密钥。",
                    "ipfs": bought_music.key_ipfshash})

        else:
            return JsonResponse({
                "status": "fail",
                "msg": '发送未知错误，请联系管理员'
            })


class AddFavView(View):
    def post(self, request, *args, **kwargs):
        """
        用户收藏，取消收藏
        """
        # 先判断用户是否登录
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录"
            })

        user_fav_form = UserFavForm(request.POST)
        if user_fav_form.is_valid():
            fav_id = user_fav_form.cleaned_data["fav_id"]
            fav_type = user_fav_form.cleaned_data["fav_type"]
            if (fav_type == 2) & (int(request.user.id) == int(fav_id)):
                return JsonResponse({
                    "status": "fail",
                    "msg": "请不要收藏自己"
                })
            if fav_type == 1:
                music = Music.objects.filter(id=int(fav_id))
                if music:
                    music = music.first()
                    if music.owner == request.user:
                        return JsonResponse({
                            "status": "fail",
                            "msg": "请不要收藏自己的作品"
                        })
            # 是否已经收藏
            existed_records = UserFavorite.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            if existed_records:
                existed_records.delete()

                if fav_type == 1:
                    music = Music.objects.get(id=fav_id)
                    music.fav_nums = F('fav_nums') - 1
                    music.save()
                elif fav_type == 2:
                    user = UserProfile.objects.get(id=fav_id)
                    user.fav_nums = F('fav_nums') - 1
                    user.save()

                return JsonResponse({
                    "status": "success",
                    "msg": "收藏"
                })
            else:
                user_fav = UserFavorite()
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.user = request.user
                user_fav.save()
                if fav_type == 1:
                    music = Music.objects.get(id=fav_id)
                    music.fav_nums = F('fav_nums') + 1
                    music.save()
                elif fav_type == 2:
                    user = UserProfile.objects.get(id=fav_id)
                    user.fav_nums = F('fav_nums') + 1
                    user.save()

                return JsonResponse({
                    "status": "success",
                    "msg": "已收藏"
                })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })


class MusicianHomeView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "musicianhome"

        all_musics = Music.objects.filter(owner=request.user)[0:4]

        return render(request, "usercenter-musician-home.html", {
            "all_musics": all_musics,
            "current_page": current_page,
        })


class MusicianMusicView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        if request.user.is_producter == False:
            return HttpResponse('error')
        musics = Music.objects.filter(owner=request.user).exclude(music_bcId='').order_by('-add_time')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(musics, per_page=4, request=request)
        my_musics = p.page(page)
        return render(request, "usercenter-musician-music.html", {
            "all_my_musics": my_musics,
            "current_page": 'musicianmusic',
        })


class MusicianMusicDetial(LoginRequiredMixin, View):
    login_url = "/login/"

    @ratelimit(key='ip', rate='1/300s', block=True)
    def get(self, request, *args, **kwargs):
        usermusic_id = request.GET.get('id')
        usermusic = Music.objects.filter(id=int(usermusic_id)).first()
        if usermusic.owner != request.user:
            return HttpResponse('警告，请不要发送无端请求')

        transactiondetial = w3.eth.getTransaction(usermusic.music_transactionHash)
        blockdetail = w3.eth.getBlock(int(transactiondetial['blockNumber']))
        PriceStorage = action.functions.getProductPriceById(int(usermusic.music_bcId)).call()
        ProductStorage = action.functions.getProductStorageById(int(usermusic.music_bcId)).call(
            {'from': request.user.address})
        recipt = [
            'prodcut id:%s' % usermusic.music_bcId,
            'product name with utf-8:%s' % ProductStorage[0],
            'product ipfs file hash:%s' % ProductStorage[1],
            'product ipfs audition hash:%s' % ProductStorage[2],
            'product status:%s' % ProductStorage[3],
            'product description with utf-8:%s' % ProductStorage[5],
            'transactionHash:%s' % usermusic.music_transactionHash,
            'from:%s' % transactiondetial['from'],
            'nonce:%s' % transactiondetial['nonce'],
            'blockHash:%s' % transactiondetial['blockHash'].hex(),
            'blockNumber:%s' % transactiondetial['blockNumber'],
            'transactionIndex:%s' % transactiondetial['transactionIndex'],
            'value(wei):%s' % transactiondetial['value'],
            'gas:%s' % transactiondetial['gas'],
            'gasPrice:%s' % transactiondetial['gasPrice'],
            'timestamp:%s' % blockdetail['timestamp'],
            'miner:%s' % blockdetail['miner'],
            'price1(wei):%s' % PriceStorage[0],
            'price2(wei):%s' % PriceStorage[1],
            'price3(wei):%s' % PriceStorage[2],
            'price4(wei):%s' % PriceStorage[3],
            'price5(wei):%s' % PriceStorage[4],
            'price6(wei):%s' % PriceStorage[5],
        ]
        response = HttpResponse(content_type='application/txt')
        response['Content-Disposition'] = 'attachment; filename=%s.txt' % (usermusic.music_transactionHash)
        for line in recipt:
            response.write(line + '\n')
        return response


def test(request):
    from apps.operations import tasks
    res = tasks.add.delay(1, 2)
    return HttpResponse(res.task_id)


@ratelimit(key='ip', rate='1/300s', block=True)
def musicianmusicsolddetial(request):
    if request.POST and request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录"
            })
        music_id = request.POST.get('music_id')
        music = Music.objects.filter(music_bcId=str(music_id))
        if not music:
            return JsonResponse({
                "status": 'fail',
                "msg": '请不要发送无端请求！'
            })
        music = music.first()
        if music.owner != request.user:
            return JsonResponse({
                "status": 'fail',
                "msg": '请不要发送无端请求！'
            })
        productSoldDetail.delay(str(music_id), str(request.user.email))
        return JsonResponse({
            "status": 'success'
        })
    else:
        return JsonResponse({
            "status": 'fail',
            "msg": '请求出错，请再次提交！'
        })
