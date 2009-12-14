# Create your views here.

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.handlers.wsgi import STATUS_CODE_TEXT
from django.contrib.auth import authenticate, login, logout

try:
    import json
except ImportError, e:
    import simplejson as json # python < 2.6

from models import UserBucket, OperationLog, Operation
import S3
from util import load_config


def with_auth(function):

    def wrapper(self, request, *args, **kwargs):
        user = self.is_authenticated(request)
        if user:
            login(request, user)
            return function(self, request, *args, **kwargs)
        else:
            return self.auth_error(request)

    wrapper.__name__ = function.__name__
    return wrapper


class Handler(object):

    def __init__(self):
        self.config = load_config() 
        self.aws = S3.QueryStringAuthGenerator(
                                self.config.get("AWS", "access_key_id"),
                                self.config.get("AWS", "secret_access_key") )


    def _get_json_response(self, dictionary):
        json_response = json.dumps(dictionary)
        response = HttpResponse(json_response, mimetype="application/json")
        response['Content-Disposition'] = 'attachment; filename="result.json"'
        return response


    def is_authenticated(self, request):
        if not request.META.has_key('HTTP_AUTHORIZATION'):
            logout(request)
            return False
        (authmeth, auth) = request.META['HTTP_AUTHORIZATION'].split(' ', 1)
        if authmeth.lower() != 'basic':
            return False
        auth = auth.strip().decode('base64')
        username, password = auth.split(':', 1)
        return authenticate(username=username, password=password)


    def auth_error(self, request):
        status_code = 401
        response = HttpResponse(mimetype = 'aplication/json')
        response.status_code = status_code
        response_dict = {
            "error-message" : '%d %s' % (status_code, STATUS_CODE_TEXT[status_code]),
            "status-code" : status_code,
        }
        json.dump(response_dict, response)
        response['WWW-Authenticate'] = 'Basic realm="Restricted Access"' 
        return response

    
    def get_bucketname(self, request):
        bucket = UserBucket.objects.get(user__username=request.user)
        return bucket.name



    @with_auth
    def call_method(self, request, key, method="GET", headers={}):
        bucket = self.get_bucketname(request)
        url = self.aws.generate_url(method, bucket, key, headers=headers)

        ol = OperationLog(  user=User.objects.get(username=request.user),
                            operation = Operation.objects.get(name=method),
                            path = key )
        ol.save()
        return self._get_json_response({'url':url, 'id' : ol.id })

    def get(self, request, key):
        return self.call_method(request, key)

    def put(self, request, base64_of_md5, key):
        return self.call_method(request, key, method="PUT", 
                                headers = { 'Content-MD5': base64_of_md5  })

    def delete(self, request, key):
        return self.call_method(request, key, method="DELETE")

    @with_auth
    def list(self, request):
        bucket = self.get_bucketname(request)
        url = self.aws.list_bucket(bucket)
        ol = OperationLog(  user=User.objects.get(username=request.user),
                            operation = Operation.objects.get(name="LIST"))
        ol.save()
        return self._get_json_response({'url':url, 'id' : ol.id })





handler = Handler()