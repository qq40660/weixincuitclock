from django.http import HttpResponse
from cuitclock.simpleweixin.weixinsdk import *
from cuitclock.clock.simsimi import SimSimi
from django.utils.encoding import smart_str
from django.views.decorators.csrf import csrf_exempt

token = ''


def callback(msg_type, data):
    if msg_type == TEXT:
        simi = SimSimi()
        content = smart_str(data['Content'])
        reply = simi.chat(content)
        return response_text(reply)

@csrf_exempt
def weixin(request):
    if request.method == 'GET':
        return HttpResponse(check_signature(token, request.GET), content_type="text/plain")
    elif request.method == 'POST':
        return HttpResponse(process_request(smart_str(request.raw_post_data), callback), content_type="application/xml")

