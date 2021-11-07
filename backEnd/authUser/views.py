from django.http import JsonResponse
from authUser.authentication import ExpiringTokenAuthentication, check_auth
from rest_framework.authtoken.models import Token
from authUser.models import CustomAccount
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
import json


class CreateAccount(APIView):
    def post(self, request, *args, **kwargs):
        request_params = request.POST.dict()
        try:
            duplicate_users = CustomAccount.objects.filter(email_address=request_params['email_address'])
            if duplicate_users.exists():
                return JsonResponse({
                    'user_created': False,
                    'errors': 'email address already exists',
                    'token': ''},
                    status=500
                )

            this_user = CustomAccount.objects.create_user(**request_params)
            token_object = Token.objects.create(user=this_user)
            return JsonResponse({
                'user_created': True,
                'token': token_object.key,
                'errors': ''
            })
        except KeyError as e:
            return JsonResponse({
                'user_created': False,
                'token': '',
                'errors': f'BadRequest: Missing key\n{e}'
            }, status=500)


class LoginAccount(APIView):
    def post(self, request, *args, **kwargs):
        request_params = request.POST.dict()
        user = authenticate(**request_params)
        if user:
            login(request, user)
            Token.objects.filter(user_id=user.id).delete()  # delete old entry if exists
            token_object = Token.objects.create(user=user)
            return JsonResponse({
                'login_success': True,
                'token': token_object.key,
                'errors': ''
            })
        else:
            # Return an 'invalid login' error message.
            return JsonResponse({
                'login_success': False,
                'token': '',
                'errors': 'email or password invalid',
            }, status=500)


class VerifyAccount(APIView):
    def get(self, request, *args, **kwargs):
        request_params = json.loads(json.dumps(request.GET))
        success, user, response = check_auth(request_params=request_params)
        status = 200
        if not success:
            status=500
        return JsonResponse(response, status=status)
        
        
