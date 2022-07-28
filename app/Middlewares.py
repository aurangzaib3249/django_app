
from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from django.http import HttpResponseForbidden    
no_limit=["login",'register']
# block requests for 60 sec if unauthurized user try urls more then 5 times except login and register 
class CustomAuthentications(MiddlewareMixin):
    def process_request(self,request):
        ip=get_client_ip(request)
        print("User ip:",ip)
        if request.user.is_authenticated:
            if cache.get(ip):
                data=cache.get(ip)
                print(ip,data)
                if data["counter"]>10:
                    return HttpResponseForbidden('<h1>Your Ip is blocked for 60 sec, Try again after 60 sec</h1>')
                else:
                    data["counter"]=data["counter"]+1
                    cache.set(ip,data,timeout=60)
            else:
                dict={'counter':1}
                cache.set(ip,dict,timeout=60)
        else:
            url=request.path
            if url and not url=="/":
                url=url.replace("/","")
            print(url)
            if not url in no_limit:
                if cache.get(ip):
                    data=cache.get(ip)
                    
                    if data["counter"]==5:
                        return HttpResponseForbidden("""<h1>Your Ip is blocked for 60 sec, Try again after 60 sec</h1>""")
                    else:
                        data["counter"]=data["counter"]+1
                        cache.set(ip,data,timeout=60)
                else:
                    dict={'counter':1,"user":"Other"}
                    cache.set(ip,dict,timeout=60)
            else:
                print("url is not blocked")
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    ip=None
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    elif request.META.get('HTTP_X_REAL_IP'):
        ip = request.META.get('HTTP_X_REAL_IP')
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip