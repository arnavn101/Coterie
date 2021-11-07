import json
from rest_framework.views import APIView
from django.db.utils import IntegrityError
import json
from authUser.authentication import check_auth
from django.http import JsonResponse
from locationUser.models import BluetoothData, LocationData

class SendCoords(APIView):
    def post(self, request):
        request_params = request.POST.dict()
        success, user, token_or_error = check_auth(request_params=request_params)
        if (not success):
            return JsonResponse(token_or_error, status=500)
        del request_params['token_user']

        try:
            LocationData.objects.create(user_id=user, **request_params)
        except IntegrityError as e:
                return JsonResponse({"errors": f'Not Enough Params: {e}'}, status=500)
        #TODO Do something with new location data

        return JsonResponse({
            'success': True,
            'errors': '',
        })

class SendBluetoothData(APIView):
    def post(self, request):
        request_params = request.POST.dict()
        success, user, token_or_error = check_auth(request_params=request_params)
        if (not success):
            return JsonResponse(token_or_error, status=500)
        del request_params['token_user']

        try:
            BluetoothData.objects.create(user_id=user, **request_params)
            #TODO Do something with new bluetooth data
        except IntegrityError as e:
                return JsonResponse({"errors": f'Not Enough Params: {e}'}, status=500)

        return JsonResponse({
            'success': True,
            'errors': '',
        })

