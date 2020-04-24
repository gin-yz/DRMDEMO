from django.http import JsonResponse, HttpResponse


def RateLimitViews(request, exception):
    if request.META['PATH_INFO'] == '/music/comment/':
        return JsonResponse({
            "status": "fail",
            "msg": "抱歉，您在一分钟内只能评论一次，请勿重复灌水！"
        })
    if (request.META['PATH_INFO'] == '/users/musicianmusicsolddetial/') | (
            request.META['PATH_INFO'] == '/users/modifyfreestyle/'):
        return JsonResponse({
            "status": "fail",
            "msg": "抱歉，为了减少系统压力，您在五分钟内只能提交一次，请勿重复提交！"
        })
    if request.META['PATH_INFO'] == '/users/info/':
        return JsonResponse({
            "status": "fail",
            "msg": "抱歉，为了减少系统压力，您在三十分钟内只能修改三次，请勿重复提交！"
        })
    if (request.META['PATH_INFO'][:24] == '/music/modifymymuiscinfo') & (request.META['REQUEST_METHOD'] == 'POST'):
        return HttpResponse("抱歉，为了减少系统压力，您在一小时内只能修改三次，请勿重复提交！")

    if (request.META['PATH_INFO'][:24] == '/music/modifymymuiscinfo') & (request.META['REQUEST_METHOD'] == 'GET'):
        return HttpResponse("抱歉，为了减少系统压力，您在一小时内只能修改三次，请勿重复提交！")

    if request.META['PATH_INFO'] == '/users/musicianmusicdetial/':
        return HttpResponse("抱歉，为了减少系统压力，您在五分钟内只能提交一次，请勿重复提交！")
