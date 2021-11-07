from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from authUser.authentication import ExpiringTokenAuthentication, check_auth
from rest_framework.authtoken.models import Token
from actionsUser.models import ActionsUser
from rest_framework.views import APIView
from django.contrib.auth import authenticate, login
import json

class GetActionsUser(APIView):
    def get(self, request, *args, **kwargs):
        request_params = json.loads(json.dumps(request.GET))
        success, user, token_or_error = check_auth(
            request_params=request_params)
        if not success:
            return JsonResponse(token_or_error, status=500)
        del request_params['token_user']

        
        actions, _ = ActionsUser.objects.get_or_create(user_id=user)
        
        return JsonResponse({
            "success": True,
            "actions": {
                "match_approved": actions.match_approved,
                "match_received": actions.match_received,
            },
            "errors": "",
        })