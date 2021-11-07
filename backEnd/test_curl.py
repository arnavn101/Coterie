import json

import requests
from os.path import basename
from profileUser.interests_list import interests_dict
import pprint
import random

URL_API = 'http://137.184.103.104:8000'


# URL_API = 'http://127.0.0.1:8000'


# Register Account
def register_account(email_address, password):
    data = {
        'email_address': email_address,
        'password': password
    }
    response = requests.post(f'{URL_API}/auth/account/create', data=data)
    response_data = response.json()
    # assert response_data['user_created'] is True
    return response_data['token']


# Login account
def login_account(email_address, password):
    data = {
        'email_address': email_address,
        'password': password
    }
    response = requests.post(f'{URL_API}/auth/account/login', data=data)
    response_data = response.json()
    # assert response_data['user_created'] is True
    return response_data['token']


# Create Profile
def create_profile(profile_picture_path, token_user, first_name, last_name, categories_selected):
    data = {
        'profile_picture_data': (basename(profile_picture_path), open(profile_picture_path, 'rb')),
        'token_user': (None, token_user),
        'first_name': (None, first_name),
        'last_name': (None, last_name),
        'categories_selected': (None, categories_selected),
    }
    response = requests.post(f'{URL_API}/profile/manage', files=data)
    response_data = response.json()
    return response_data
    # assert response_data['success'] is True


# Get Profile with Token
def get_profile_token(token_user):
    params = (
        ('token_user', token_user),
    )
    response = requests.get(f'{URL_API}/profile/details', params=params)
    response_data = response.json()
    return response_data
    # assert response_data['errors'] == ''


# Get profile with UID
def get_profile_uid(uid_user):
    params = (
        ('uid', uid_user),
    )
    response = requests.get(f'{URL_API}/profile/details', params=params)
    response_data = response.json()
    return response_data
    # assert response_data['errors'] == ''


# Post coords data based on token_user
def post_location_coords(token_user, latitude, longitude):
    data = {
        'token_user': token_user,
        'latitude': latitude,
        'longitude': longitude
    }
    response = requests.post(f'{URL_API}/location/coords', data=data)
    response_data = response.json()
    return response_data
    # assert response_data['success'] is True


# Post location data
def post_bluetooth_coords(token_user, devices_nearby):
    data = {
        'token_user': token_user,
        'devices_nearby': devices_nearby
    }
    response = requests.post(f'{URL_API}/location/bluetooth', data=data)
    response_data = response.json()
    return response_data
    # assert response_data['success'] is True


# Get Field availabilities

def get_field_availabilities():
    response = requests.get(f'{URL_API}/profile/availselections')
    response_data = response.json()
    return response_data


# Create a Match Request given token_user and corresponding uid
def create_match_request(token_user, uid):
    data = {
        'token_user': token_user,
        'uid': uid
    }
    response = requests.post(f'{URL_API}/matches/request/send', data=data)
    response_data = response.json()
    return response_data
    # assert response_data['success'] is True


# Accept the Match Request given token_user and corresponding uid
def accept_match_request(token_user, uid):
    data = {
        'token_user': token_user,
        'uid': uid
    }
    response = requests.post(f'{URL_API}/matches/request/accept', data=data)
    response_data = response.json()
    return response_data
    # assert response_data['success'] is True


# Reject the Match Request given token_user and corresponding uid
def reject_match_request(token_user, uid):
    data = {
        'token_user': token_user,
        'uid': uid
    }
    response = requests.post(f'{URL_API}/matches/request/reject', data=data)
    response_data = response.json()
    return response_data
    # assert response_data['success'] is True


# Cancel the Match Request given token_user and corresponding uid
def cancel_match_request(token_user, uid):
    data = {
        'token_user': token_user,
        'uid': uid
    }
    response = requests.post(f'{URL_API}/matches/request/cancel', data=data)
    response_data = response.json()
    return response_data
    # assert response_data['success'] is True


# Get List of Matches (typeReturn either incoming or outgoing)
def list_match_request(token_user, type_output, match_type):
    params = (
        ('token_user', token_user),
        ('typeOutput', type_output),
        ('match_type', match_type)
    )
    response = requests.get(f'{URL_API}/matches/matchlist', params=params)
    response_data = response.json()
    return response_data
    # assert response_data['success'] is True


# Get List of Recommended Matches
def list_match_recommend_request(token_user):
    params = (
        ('token_user', token_user),
    )
    response = requests.get(f'{URL_API}/matches/recommendations', params=params)
    response_data = response.json()
    return response_data
    # assert response_data['success'] is True


# Get List of Recommended Matches
def list_user_stats(token_user):
    params = (
        ('token_user', token_user),
    )
    response = requests.get(f'{URL_API}/statboard', params=params)
    response_data = response.json()
    return response_data
    # assert response_data['success'] is True


# Test Major Interest Card
def test_uid_card(token_user, uid):
    params = (
        ('token_user', token_user),
        ('uid', uid)
    )
    response = requests.get(f'{URL_API}/matches/card', params=params)
    response_data = response.json()
    return response_data


# Test Major Interest Card
def test_recom_uid_card(token_user):
    params = (
        ('token_user', token_user),
    )
    response = requests.get(f'{URL_API}/matches/recommendations/cards', params=params)
    response_data = response.json()
    return response_data


# Testing Code
list_emails = [str(i) for i in range(20)]

list_tokens = [register_account(f'{i}@gmail.com', 'password1') for i in list_emails]
list_tokens_logged = [login_account(f'{i}@gmail.com', 'password1') for i in list_emails]
list_interests = list(interests_dict.keys())[:12]

profile_resp = [create_profile('test_png.png', list_tokens_logged[j], f'John{j}', f'Doe{j}',
                               json.dumps(random.sample(list_interests, 5)))
                for j in range(len(list_tokens_logged))]

profileDetails = [get_profile_token(t) for t in list_tokens_logged]

successLoc = [post_location_coords(list_tokens_logged[j], str(20 + j), str(70 + j)) for j in
              range(len(list_tokens_logged))]

successBlue = [post_bluetooth_coords(token, '{}') for token in list_tokens_logged]

# printer = pprint.PrettyPrinter(indent=4)
# printer.pprint(get_field_availabilities)

recomList = [list_match_recommend_request(token) for token in list_tokens_logged]

uid_card = test_uid_card(list_tokens_logged[0], 2)

list_user_stats(list_tokens_logged[0])

responses_match = [create_match_request(list_tokens_logged[i], i+2) for i in range(len(list_tokens_logged))]
accept_match_request(list_tokens_logged[1], 1)
respUID = test_recom_uid_card(list_tokens_logged[0])
# create_match_request(first_token, user_second_id)
# accept_match_request(second_token, user_first_id)
# create_match_request(first_token, 2)
# accept_match_request(second_token, 1)
# list_match_request(first_token, 'incoming', 1)
