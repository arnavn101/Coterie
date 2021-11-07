from django.shortcuts import render
import json
from rest_framework.views import APIView
from django.db.utils import IntegrityError
import json
from authUser.authentication import check_auth
from django.http import JsonResponse
from authUser.models import CustomAccount
from matchesUser.models import Matches
from django.core import serializers
from profileUser.models import ProfileUser
from profileUser.views import convert_db_url_to_actual
from interestsProfile.models import InterestProfile, AlgoIDToUserID
from interestsProfile.matching_algo import MatchingAlgo
from profileUser.interests_list import length
from actionsUser.models import ActionsUser


class CreateMatchRequest(APIView):
    def post(self, request):
        request_params = request.POST.dict()
        success, user, token_or_error = check_auth(
            request_params=request_params)
        if not success:
            return JsonResponse(token_or_error, status=500)
        del request_params['token_user']

        try:
            other_way_params = {'outgoing_user_id': CustomAccount.objects.get(id=request_params['uid']),
                                'incoming_user_id': user,
                                }

            dict_params = {'outgoing_user_id': user,
                           'incoming_user_id': CustomAccount.objects.get(id=request_params['uid']),
                           }
            if dict_params['outgoing_user_id'].id == dict_params['incoming_user_id'].id:
                return JsonResponse({
                    "success": False,
                    "errors": f"Why are you trying match with yourself--stop being weird.\
                            token_id and uid corresponds to the same user",
                }, status=500)
        except Exception as e:
            return JsonResponse({
                "success": False,
                "errors": f"SomethingBadHappened: {e}",
            }, status=500)

        existing_requests = Matches.objects.filter(**dict_params)
        other_way_requests = Matches.objects.filter(**other_way_params)

        if existing_requests.exists() or other_way_requests.exists():
            return JsonResponse({
                "success": False,
                "errors": "Match Request Already Exists",
            }, status=500)
        else:
            Matches.objects.create(**dict_params)
            actions, _ = ActionsUser.objects.get_or_create(user_id=CustomAccount.objects.get(id=request_params['uid']))

            actions.match_received.append(user.id)
            actions.save()

            return JsonResponse({
                "success": True,
                "errors": "",
            })


class AcceptMatchRequest(APIView):
    def post(self, request):
        request_params = request.POST.dict()
        success, user, token_or_error = check_auth(
            request_params=request_params)
        if not success:
            return JsonResponse(token_or_error, status=500)
        del request_params['token_user']

        try:
            dict_params = {'outgoing_user_id': CustomAccount.objects.get(id=int(request_params['uid'])),
                           'incoming_user_id': user,
                           }
            if dict_params['outgoing_user_id'].id == dict_params['incoming_user_id'].id:
                return JsonResponse({
                    "success": False,
                    "errors": f"Wow dude--stop trying to accept yourself. Make new friends.\
                            token_id and uid corresponds to the same user",
                }, status=500)
        except Exception as e:
            return JsonResponse({
                "success": False,
                "errors": f"SomethingBadHappened: {e}",
            }, status=500)

        existing_requests = Matches.objects.filter(**dict_params)

        if existing_requests.exists():
            if not existing_requests.first().match_status == 1:
                existing_requests.update(match_status=1)

                actions_user_approved, _ = ActionsUser.objects.get_or_create(user_id=CustomAccount.objects.get(id=request_params['uid']))
                actions_user_approved.match_approved.append(user.id)
                actions_user_approved.save()

                actions_user_received, _ = ActionsUser.objects.get_or_create(user_id=user)
                actions_user_received.match_received.remove(int(request_params['uid']))
                actions_user_received.save()

                return JsonResponse({
                    "success": True,
                    "errors": "",
                })
            else:
                return JsonResponse({
                    "success": False,
                    "errors": f"Match already exists between {dict_params['incoming_user_id'].email_address} \
                            and {dict_params['outgoing_user_id'].email_address}\
                            ",
                }, status=500)
        else:
            return JsonResponse({
                "success": False,
                "errors": f"Pending request does not exist. {dict_params['incoming_user_id'].email_address} \
                            cannot accept {dict_params['outgoing_user_id'].email_address}\
                            ",
            }, status=500)
        # TODO Add an action item to the accepted user


class RejectMatchRequest(APIView):
    def post(self, request):
        request_params = request.POST.dict()
        success, user, token_or_error = check_auth(
            request_params=request_params)
        if not success:
            return JsonResponse(token_or_error, status=500)
        del request_params['token_user']

        try:
            dict_params = {'outgoing_user_id': CustomAccount.objects.get(id=int(request_params['uid'])),
                           'incoming_user_id': user,
                           }
            if dict_params['outgoing_user_id'].id == dict_params['incoming_user_id'].id:
                return JsonResponse({
                    "success": False,
                    "errors": f"Wow dude--stop trying to reject yourself. Make new friends.\
                            token_id and uid corresponds to the same user",
                }, status=500)
        except Exception as e:
            return JsonResponse({
                "success": False,
                "errors": f"SomethingBadHappened: {e}",
            }, status=500)

        existing_requests = Matches.objects.filter(**dict_params)

        if existing_requests.exists():
            if not existing_requests.first().match_status == 1:
                existing_requests.update(match_status=-1)

                # TODO Initimate uid user that match was rejected

                actions_user_received, _ = ActionsUser.objects.get_or_create(user_id=user)
                actions_user_received.match_received.remove(int(request_params['uid']))
                actions_user_received.save()

                return JsonResponse({
                    "success": True,
                    "errors": "",
                })
            else:
                return JsonResponse({
                    "success": False,
                    "errors": f"Match already exists between {dict_params['incoming_user_id'].email_address} \
                            and {dict_params['outgoing_user_id'].email_address}\
                            ",
                }, status=500)
        else:
            return JsonResponse({
                "success": False,
                "errors": f"Pending request does not exist. {dict_params['incoming_user_id'].email_address} \
                            cannot accept {dict_params['outgoing_user_id'].email_address}\
                            ",
            }, status=500)


class CancelMatchRequest(APIView):
    def post(self, request):
        request_params = request.POST.dict()
        success, user, token_or_error = check_auth(
            request_params=request_params)
        if not success:
            return JsonResponse(token_or_error, status=500)
        del request_params['token_user']

        try:
            dict_params = {'outgoing_user_id': user,
                           'incoming_user_id': CustomAccount.objects.get(id=int(request_params['uid'])),
                           }
            if dict_params['outgoing_user_id'].id == dict_params['incoming_user_id'].id:
                return JsonResponse({
                    "success": False,
                    "errors": f"Wow dude--stop trying to cancel yourself. Make new friends.\
                            token_id and uid corresponds to the same user",
                }, status=500)
        except Exception as e:
            return JsonResponse({
                "success": False,
                "errors": f"SomethingBadHappened: {e}",
            }, status=500)

        existing_requests = Matches.objects.filter(**dict_params)

        if existing_requests.exists():
            if not existing_requests.first().match_status == 1:
                existing_requests.update(match_status=1)

                # TODO something not sure

                actions_user_received, _ = ActionsUser.objects.get_or_create(user_id=CustomAccount.objects.get(id=request_params['uid']))
                actions_user_received.match_received.remove(int(user.id))
                actions_user_received.save()

                return JsonResponse({
                    "success": True,
                    "errors": "",
                })
            else:
                return JsonResponse({
                    "success": False,
                    "errors": f"Match already exists between {dict_params['incoming_user_id'].email_address} \
                            and {dict_params['outgoing_user_id'].email_address}\
                            ",
                }, status=500)
        else:
            return JsonResponse({
                "success": False,
                "errors": f"Pending request does not exist. {dict_params['incoming_user_id'].email_address} \
                            cannot accept {dict_params['outgoing_user_id'].email_address}\
                            ",
            }, status=500)


class MatchList(APIView):
    def get(self, request):
        request_params = json.loads(json.dumps(request.GET))
        success, user, token_or_error = check_auth(
            request_params=request_params)
        if not success:
            return JsonResponse(token_or_error, status=500)
        del request_params['token_user']

        return self.get_match(user, request_params['typeOutput'], request_params['match_type'])

    # typeOutput either: incoming or outgoing
    def get_match(self, user, typeOutput: str, match_status: int):
        typeOutput += '_user_id'
        outgoing_requests = Matches.objects.filter(
            match_status=match_status, **{typeOutput: user})

        if outgoing_requests.exists():
            serialized_objs = json.loads(
                serializers.serialize('json', outgoing_requests))

            list_of_uids = []
            for serialized_obj in serialized_objs:
                list_of_uids.append(serialized_obj['fields'][f'{typeOutput}'])

            return JsonResponse({
                "success": True,
                "matching_uids": json.dumps(list_of_uids),
                "errors": "",
            })
        else:
            return JsonResponse({
                "success": True,
                "matching_uids": json.dumps([]),
                "errors": "",
            })


def get_closest_matches_user(user):
    user_id = user.id
    user_weight = list(InterestProfile.objects.get(
        user_id=user).dict_interests_weights.values())
    algo = MatchingAlgo(length)
    algo.deserialize_index()
    neighbour_indices = algo.k_nearest_neighbours(5, user_weight)
    record = AlgoIDToUserID.objects.get().mapping
    return [record[str(index)] for index in neighbour_indices if record[str(index)] != user_id]


class MatchRecommendation(APIView):
    def get(self, request):
        request_params = json.loads(json.dumps(request.GET))
        success, user, token_or_error = check_auth(
            request_params=request_params)
        if not success:
            return JsonResponse(token_or_error, status=500)
        del request_params['token_user']
        user_id_indices = get_closest_matches_user(user)
        try:

            return JsonResponse({
                "success": True,
                "suggested_uids": json.dumps(user_id_indices),
                "errors": "",
            })
        except Exception as e:
            return JsonResponse({
                "success": False,
                "suggested_uids": "",
                "errors": f"{e}",
            }, status=500)


class UIDCard(APIView):
    def get(self, request):
        request_params = json.loads(json.dumps(request.GET))
        success, user, token_or_error = check_auth(
            request_params=request_params)
        if not success:
            return JsonResponse(token_or_error, status=500)
        del request_params['token_user']

        try:
            uid = request_params['uid']
        except KeyError as ke:
            return JsonResponse({
                "errors": f"uid not in request: {ke}"
            }, status=500)

        token_user_interest_dict = InterestProfile.objects.get(
            user_id=user.id).dict_interests_weights
        uid_user_weights = InterestProfile.objects.get(
            user_id=uid).dict_interests_weights

        distances = ((k, abs(v - uid_user_weights[k]))
                     for k, v in token_user_interest_dict.items() if v != 0)

        major_interest = min(distances, key=lambda x: x[1])[0]

        uid_user = ProfileUser.objects.get(user_id=uid)

        return JsonResponse({
            "picture_url": convert_db_url_to_actual(uid_user.profile_picture),
            "major_match_interest": major_interest,
            "full_name": uid_user.first_name + " " + uid_user.last_name,
            "errors": "",
        }
        )


class UIDCardsRecommends(APIView):
    def get(self, request):
        request_params = json.loads(json.dumps(request.GET))
        success, user, token_or_error = check_auth(
            request_params=request_params)
        if not success:
            return JsonResponse(token_or_error, status=500)
        del request_params['token_user']

        user_id_indices = get_closest_matches_user(user)

        final_json_out = []

        try:
            for uid in user_id_indices:
                token_user_interest_dict = InterestProfile.objects.get(
                    user_id=user.id).dict_interests_weights
                uid_user_weights = InterestProfile.objects.get(
                    user_id=uid).dict_interests_weights

                distances = ((k, abs(v - uid_user_weights[k]))
                             for k, v in token_user_interest_dict.items() if v != 0)

                major_interest = min(distances, key=lambda x: x[1])[0]

                uid_user = ProfileUser.objects.get(user_id=uid)
                final_json_out.append({
                    "picture_url": convert_db_url_to_actual(uid_user.profile_picture),
                    "major_match_interest": major_interest,
                    "full_name": uid_user.first_name + " " + uid_user.last_name,
                    "uid": uid,
                })
        except KeyError as ke:
            return JsonResponse({
                "errors": f"uid not in request: {ke}"
            }, status=500)
        return JsonResponse(final_json_out, safe=False)

