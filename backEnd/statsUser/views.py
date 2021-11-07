from rest_framework.views import APIView
import json
from authUser.authentication import check_auth
from django.http import JsonResponse
from matchesUser.models import Matches


class UserStats(APIView):
    def get(self, request):
        request_params = json.loads(json.dumps(request.GET))
        success, user, token_or_error = check_auth(
            request_params=request_params)
        if not success:
            return JsonResponse(token_or_error, status=500)
        del request_params['token_user']

        try:
            active_matches = Matches.objects.filter(match_status=1)
            incoming_matches = Matches.objects.filter(incoming_user_id=user, match_status=0)
            outgoing_matches = Matches.objects.filter(outgoing_user_id=user, match_status=0)

            return JsonResponse({
                "success": True,
                "number_active_matches": len(active_matches),
                "number_incoming_matches": len(incoming_matches),
                "number_outgoing_matches": len(outgoing_matches),
                "errors": "",
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "number_active_matches": -1,
                "number_incoming_matches": -1,
                "number_outgoing_matches": -1,
                "errors": "BackEndFailure/BadTokenError"
            }, status=500)
