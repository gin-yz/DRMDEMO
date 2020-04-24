import ipfshttpclient
from django.db.models import Q, F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger

from ratelimit.decorators import ratelimit

from apps.music.forms import CommentsForm, CommentsDeleteForm, receiveUploadSystemForm, modifyMusicInfoForm
from apps.music.models import Music, MusicTag, MusicComments
from apps.operations.forms import UploadOneForm
from apps.operations.models import UserFavorite, UserMusic
from apps.operations.views import action


class MusicListView(View):
    def get(self, request, *args, **kwargs):
        """获取音乐列表信息"""
        all_music = Music.objects.filter(music_status=1).order_by("-add_time")
        print(all_music)
        hot_music = sorted(Music.objects.filter(music_status=1), key=lambda i: i.hot_num(), reverse=True)[:4]
        # 搜索关键词
        keywords = request.GET.get("keywords", "")
        s_type = "music"
        if keywords:
            all_music = all_music.filter(Q(music_name__icontains=keywords) | Q(music_desc__icontains=keywords))

        # 标签查找
        list = request.GET.get('taglist', '')
        if list:
            strlist = list.split(",")
            if len(strlist) <= 5:
                for index, item in enumerate(strlist):
                    strlist[index] = int(item)
                music_tags = MusicTag.objects.filter(tag__in=strlist)
                related_musics = set()
                for music_tag in music_tags:
                    related_musics.add(music_tag.music.music_bcId)
                all_music = all_music.filter(music_bcId__in=related_musics)

        # 音乐排序
        sort = request.GET.get("sort", "")
        # 购买人数
        if sort == "buy_nums":
            all_music = sorted(all_music, key=lambda i: i.all_sell_count(), reverse=True)
        # 点击数
        elif sort == "click":
            all_music = all_music.order_by("-click_nums")
        # 收藏数
        elif sort == 'fav_nums':
            all_music = all_music.order_by("-fav_nums")
        # 热门综合指标
        elif sort == 'hot':
            all_music = sorted(all_music, key=lambda i: i.hot_num(), reverse=True)

        # 对音乐数据进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_music, per_page=12, request=request)
        musics = p.page(page)

        return render(request, "course-list.html", {
            "all_music": musics,
            "sort": sort,
            "hot_musics": hot_music,
            "keywords": keywords,
            "s_type": s_type,
            'taglist': list,
        })


class MusicDetailView(View):
    def get(self, request, music_id, *args, **kwargs):
        """
        获取音乐的详情
        """
        music = Music.objects.get(id=int(music_id))
        music.click_nums = F('click_nums') + 1
        music.save()
        comments = MusicComments.objects.filter(music=music).order_by('-add_time')
        is_comment = request.GET.get('is_comment', 'False')

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
            if course_tag.music.music_status ==1:
                related_music.add(course_tag.music)
        related_music = sorted(related_music, key=lambda i: i.all_sell_count(), reverse=True)[:3]
        if not related_music:
            related_music = Music.objects.filter(music_status=1).exclude(id=music.id).order_by("-add_time")[:3]
        return render(request, "course-detail.html", {
            "music": music,
            "has_fav_music": has_fav_music,
            "has_fav_composer": has_fav_composer,
            "related_music": related_music,
            'comments': comments,
            'is_comment': is_comment,
            "s_type":"music"
        })


@ratelimit(key='ip', rate='1/60s', block=True)
def CommentMusic(request):
    if request.POST and request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录"
            })

        comment_form = CommentsForm(request.POST)
        if comment_form.is_valid():
            music = comment_form.cleaned_data["music"]
            bought_music = UserMusic.objects.filter(music=music).filter(user=request.user)
            if bought_music:
                comments = comment_form.cleaned_data["comments"]
                comment = MusicComments()
                comment.user = request.user
                comment.comments = comments
                comment.music = music
                comment.save()

                return JsonResponse({
                    "status": "success",
                })
            else:
                return JsonResponse({
                    "status": "fail",
                    "msg": "您还未购买此版权"
                })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })


def DeleteComment(request):
    if request.POST and request.method == 'POST':
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录"
            })

        comment_form = CommentsDeleteForm(request.POST)
        if comment_form.is_valid():
            comment_id = comment_form.cleaned_data["comment_id"]
            music_comment = MusicComments.objects.filter(id=int(comment_id))
            if music_comment:
                music_comment.first().delete()
                return JsonResponse({
                    "status": "success",
                })
            else:
                return JsonResponse({
                    "status": "fail",
                    "msg": "请不要发送无端请求"
                })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "参数错误"
            })


def receiveuploadsystem(request):
    receive_data = receiveUploadSystemForm(request.POST)
    if receive_data.is_valid():
        purchase_bcId = receive_data.cleaned_data['purchase_bcId']
        ipfshash = receive_data.cleaned_data['ipfshash']
        bought_music = UserMusic.objects.filter(purchase_bcId=str(purchase_bcId))
        if bought_music:
            bought_music = bought_music.first()
            ipfs_hash = action.functions.getLicenseBypurchaseId(int(bought_music.purchase_bcId)).call()
            if str(ipfs_hash) == str(ipfshash):
                bought_music.key_ipfshash = ipfshash
                bought_music.save()
            return HttpResponse('ok')
    return HttpResponse('no')



class ModifyMyMuiscInfoView(View):
    @ratelimit(key='ip', rate='3/3600s', block=True)
    def get(self, request, *args, **kwargs):
        music_bcid = request.GET.get('id')
        music = Music.objects.filter(music_bcId=str(music_bcid))
        if music:
            music = music.first()
            if music.music_status == 1:
                return HttpResponse('请先下架版权')
            if music.owner != request.user:
                return HttpResponse('请不要发送无端请求')
        else:
            return HttpResponse("请不要发送无端请求")
        ueditorform = UploadOneForm()
        return render(request,'usercenter-modifymuicinfo.html',context={
            'music':music,
            'form':ueditorform,
        })

    @ratelimit(key='ip', rate='3/3600s', block=True)
    def post(self, request, *args, **kwargs):
        modifymusicform = modifyMusicInfoForm(request.POST)
        if modifymusicform.is_valid():
            music_bcId = modifymusicform.cleaned_data['music_bcId']

            music = Music.objects.filter(music_bcId=str(music_bcId))
            if music:
                music = music.first()
                if music.music_status == 1:
                    return JsonResponse({
                        'status': 'fail',
                        'msg': '请先下架版权'
                    })
                if music.owner != request.user:
                    return JsonResponse({
                        'status': 'fail',
                        'msg': '请不要发送无端请求'
                    })
            else:
                return JsonResponse({
                    'status': 'fail',
                    'msg': '请不要发送无端请求'
                })
            music.music_detail = modifymusicform.cleaned_data['music_detail']
            music.save()

            return JsonResponse({
                'status':'success',
                'msg':"保存成功！"
            })
        else:
            return JsonResponse({
                'status': 'fail',
                'msg': ','.join(modifymusicform.errors)
            })


class PriceIntroduceView(View):
    def get(self, request, *args, **kwargs):
        return render(request,'priceintroduce.html',context={
            "s_type": "music"
        })