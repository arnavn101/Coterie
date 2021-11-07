import json
from django.db.utils import IntegrityError
from rest_framework.views import APIView
from profileUser.models import ProfileUser
import json
from authUser.authentication import check_auth
from actionsUser.models import ActionsUser
from django.http import JsonResponse
import pdb
from interestsProfile.views import InterestProfileManager
import os
from profileUser.categories import categories
from hackathon_project_backend.settings import PROFILE_PICTURES_ROOT
from django.core import serializers


class UpdateProfile(APIView):
    def post(self, request):
        request_params = request.POST.dict()
        success, user, token_or_error = check_auth(request_params=request_params)
        interest_profile_mgr = InterestProfileManager(user)
        error = ''
        if not success:
            return JsonResponse(token_or_error, status=500)
        del request_params['token_user']
        this_profile = ProfileUser.objects.filter(user_id=user)

        try:
            request_params['categories_selected'] = json.dumps(request_params['categories_selected'])
        except KeyError as e:
            return JsonResponse({"errors": f'categories_selected param is missing'}, status=500)

        if this_profile.exists():
            try:
                this_profile.update(**request_params)
                this_profile = this_profile.first()
            except KeyError as e:
                return JsonResponse({"errors": f'Incorrect params: {e}'}, status=500)
            try:
                successThis = interest_profile_mgr.update_interests(
                    self.handle_request_list(this_profile.categories_selected))
                if not successThis:
                    raise KeyError('Invalid Keys')
            except KeyError as ke:
                return JsonResponse({"errors": f'Key does not exist: {ke}'}, status=500)
        else:
            # Otherwise, create a new profile
            try:
                this_profile = ProfileUser.objects.create(user_id=user, **request_params)
            except IntegrityError as e:
                return JsonResponse({"errors": f'Not Enough Params: {e}'}, status=500)
            
            except IntegrityError as e:
                return JsonResponse({"errors": f'Not Enough Params: {e}'}, status=500)

            try:
                successThis = interest_profile_mgr.initialize_interests(
                    self.handle_request_list(this_profile.categories_selected))
                if not successThis:
                    raise KeyError('Invalid Keys')
            except KeyError as ke:
                success = False
                error = f'Key does not exist: {ke}'

        if request.FILES:
            image = request.FILES['profile_picture_data']
            this_profile.profile_picture.save(image.name, image)

        if success:
            return JsonResponse({
                "success": success,
                "profile_picture_url": convert_db_url_to_actual(this_profile.profile_picture),
                "errors": error,
            })
        else:
            return JsonResponse({
                "success": success,
                "profile_picture_url": convert_db_url_to_actual(this_profile.profile_picture),
                "errors": error,
            }, status=500)

    # TODO - Json.loads twice may not be good
    def handle_request_list(self, input_list):
        return json.loads(json.loads(input_list))


class ExistsProfile(APIView):
    def get(self, request):
        request_params = json.loads(json.dumps(request.GET))
        success, user, token_or_error = check_auth(request_params=request_params)
        if not success:
            return JsonResponse(token_or_error, status=500)
        this_profile = ProfileUser.objects.filter(user_id=user)

        if this_profile.exists():
            return JsonResponse({
                "first_time": False,
                "errors": "",
            })
        else:
            return JsonResponse({
                "first_time": True,
                "errors": "",
            })


class DetailsProfile(APIView):
    def get(self, request):
        request_params = json.loads(json.dumps(request.GET))
        if 'token_user' in request_params:
            return self.token_details(request_params)
        elif 'uid' in request_params:
            return self.uid_details(request_params['uid'])
        else:
            return JsonResponse({
                "errors": "Either token_user or uid must be specified in params"
            }, status=500)

    def token_details(self, request_params):
        success, user, token_or_error = check_auth(request_params=request_params)
        if not success:
            return JsonResponse(token_or_error, status=500)
        this_profile = ProfileUser.objects.filter(user_id=user)
        return self.return_response(this_profile=this_profile)

    def uid_details(self, uid):
        this_profile = ProfileUser.objects.filter(user_id=uid)
        return self.return_response(this_profile=this_profile)

    def return_response(self, this_profile):
        if this_profile.exists():
            serialized_obj = json.loads(serializers.serialize('json', this_profile))[0]['fields']
            del serialized_obj['user_id']
            serialized_obj['errors'] = ''
            this_profile = this_profile.first()
            serialized_obj['profile_picture_url'] = PROFILE_PICTURES_ROOT + \
                                                    os.path.basename(this_profile.profile_picture.name)
            return JsonResponse(serialized_obj)
        else:
            return JsonResponse({
                "errors": "Profile not found",
            }, status=500)


class FieldsSelectionAvail(APIView):
    def get(self, request):
        return JsonResponse(categories)


def convert_db_url_to_actual(profile_picture):
    return PROFILE_PICTURES_ROOT + os.path.basename(profile_picture.name)
