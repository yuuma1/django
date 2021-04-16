from django.views.generic import View
from django.http import JsonResponse

from thread.models import Vote

# newsapiです

class CreateVoteView(View):
  
    def post(self, request, *args, **kwargs):
        res = {
            'result': False,
            'message': '処理に失敗しました。'
        }
        # POST値に'comment_id'がなければBAD REQUESTとする
        if not 'comment_id' in request.POST:
            return JsonResponse(res, status=400)
        
        # コメントIDとIPアドレスの取得
        comment_id = request.POST['comment_id']
        ip_address = get_client_ip(request)

        # 既にIP登録があればコンフリクト
        if Vote.objects.filter(comment_id=comment_id, ip_address=ip_address):
            res['message'] = '投票済みです'
            return JsonResponse(res, status=409)
        
        # Voteの保存に成功した場合のみ成功
        if Vote.objects.create_vote(ip_address, comment_id):
            res['result'] = True
            res['message'] = 'ポイント追加しました'
            return JsonResponse(res, status=201)      
        else:
            return JsonResponse(res, status=500)

def get_client_ip(request):
  
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

