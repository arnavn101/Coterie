
## User Auth 

### [POST] Create Account
```curl
POST /auth/account/create
```

#### Query Parameters
- email_address
- password_user

### Response
#### Successful Request
```json
{
  "user_created": true,
  "errors": "",
  "token": "random_token"
}
```

#### Failed Request
```json
{
  "user_created": false,
  "errors": "email address already exists",
  "token": ""
}
```

### [POST] Login Account
```curl
POST /auth/account/login
```

#### Query Parameters
- email_address
- password_user

### Response
#### Successful Request
```json
{
  "login_success": true,
  "errors": "",
  "token": "random_token"
}
```

#### Failed Request
```json
{
  "login_success": false,
  "errors": "email or password invalid",
  "token": ""
}
```

### [GET] Verify Logged in Status
```curl
GET /auth/account/verify
```

#### Query Parameters
- token_user

### Response
#### Successful Request
```json
{
  "logged_in": true,
  "errors": ""
}
```

#### Failed Request
```json
{
  "logged_in": false,
  "errors": "token expired, login again"
}
```

## User Profile

### [GET] Check Profile Creation
```curl
GET /profile/exists
```

#### Query Parameters
- token_user

### Response
#### If not first time user
```json
{
  "first_time": false,
  "errors": ""
}
```

#### If first time user
```json
{
  "first_time": true,
  "errors": ""
}
```

#### If token not found (or user does not exist)
```json
{
  "first_time": false,
  "errors": "BadTokenError"
}
```

### [GET] Get user profile
```curl
GET /profile/details
```

#### Query Parameters
- token_user or uid

### Response
#### Successful Request
```json
{
  "first_name": "firstName",
  "last_name": "lastName",
  "email_address": "emailAddress@email.com",
  "profile_picture": "urlProfilePicture",
  "tag_interests": ["education", "movies", "games"],
  "errors": ""
}
```

#### Failed Request
```json
{
  "first_name": "",
  "last_name": "",
  "email_address": "",
  "profile_picture": "",
  "tag_interests": [],
  "errors": "BadTokenError"
}
```

### [GET] Get field availabilities
```curl
GET /profile/availselections
```

#### Query Parameters
- None

### Response
#### Successful Request
```json
{
  "categories": {
    "entertainment": ["music", "games", "anime"],
    "technology": ["coding", "news"],
    "...": ["...", "..."]
  }
}
```

#### Failed Request
```json
{
    "categories": {},
    "errors": "BackendFailure"
}
```

### [POST] Create/Update profile
```curl
POST /profile/manage
```

#### Query Parameters
- token_user
- first_name
- last_name
- profile_picture_data
- categories_dictionary with prototype:
```json
{
  "categories": {
    "entertainment": ["music", "games", "anime"],
    "technology": ["coding", "news"],
    "...": ["...", "..."]
  }
}
```

### Response
#### Update Successful 
```json
{
  "success": true,
  "profile_picture_url": "someUrl.com/abc.png",
  "errors": ""
}
```

#### Update Failure
```json
{
  "success": false,
  "profile_picture_url": "",
  "errors": "token/category/backend failure"
}
```


## User Location
### [POST] Send Coordinates
```curl
POST /location/coords
```

#### Query Parameters
- token_user
- latitude
- longitude

### Response
#### Sent Successfully 
```json
{
  "success": true,
  "errors": ""
}
```

#### Update Failure
```json
{
  "success": false,
  "errors": "BackEndFailure/BadTokenError"
}
```

### [POST] Send Bluetooth Nearby
```curl
POST /location/bluetooth
```

#### Query Parameters
- token_user
- [list_users_nearby]

### Response
#### Sent Successfully 
```json
{
  "success": true,
  "errors": ""
}
```

#### Update Failure
```json
{
  "success": false,
  "errors": "BackEndFailure/BadTokenError"
}
```

## User Matches 
Display potential matches

### [GET] Get UID Card
```curl
GET /matches/card
```

#### Query Parameters
- uid
- token_user

### Response
#### Request Success 
```json
{
  "picture_url": "<URL>",
  "major_match_interest": "Movies",
  "full_name": "Harry Porter",
  "errors": "",
}
```

#### Request Failure
```json
{
  "picture_url": "",
  "major_match_interest": "",
  "full_name": "",
  "errors": "BackEndFailure/BadTokenError/BadUID"
}
```

### [GET] Get List of Match Recommendations
```curl
GET /matches/recommendations
```

#### Query Parameters
- token_user

### Response
#### Request Success 
```json
{
  "success": true,
  "suggested_uids": [
    0,
    1,
    2,
    ...
  ],
  "errors": "",
}
```

#### Request Failure
```json
{
  "success": false,
  "suggested_uids": [],
  "errors": "BackEndFailure/BadTokenError/BadUID"
}
```

### [GET] Get List of Matches
```curl
GET /matches/matchlist
```

#### Query Parameters
- token_user
- type typeOutput(incoming or outgoing)
- match_type (1 for confirmed matches, 0 for pending, -1 for rejected)

### Response
#### Request Success 
```json
{
  "success": true,
  "matching_uids": [
    "0",
    "1",
    ""
  ],
  "errors": "",
}
```

#### Request Failure
```json
{
  "success": false,
  "matching_uids": [],
  "errors": "BackEndFailure/BadTokenError/BadUID"
}
```



### [POST] Create Match Request
```curl
POST /matches/request/send
```

#### Query Parameters
- uid
- token_user

### Response
#### Request Success 
```json
{
  "success": true,
  "errors": "",
}
```

#### Request Failure
```json
{
  "success": false,
  "errors": "BackEndFailure/BadTokenError/BadUID"
}
```

### [POST] Accept Incoming match
```curl
POST /matches/request/accept
```

#### Query Parameters
- uid
- token_user

### Response
#### Request Success 
```json
{
  "success": true,
  "errors": "",
}
```

#### Request Failure
```json
{
  "success": false,
  "errors": "BackEndFailure/BadTokenError/BadUID"
}
```

### [POST] Reject Incoming match
```curl
POST /matches/request/reject
```

#### Query Parameters
- uid
- token_user

### Response
#### Request Success 
```json
{
  "success": true,
  "errors": "",
}
```

#### Request Failure
```json
{
  "success": false,
  "errors": "BackEndFailure/BadTokenError/BadUID"
}
```

### [POST] Cancel Outgoing match
```curl
POST /matches/request/cancel
```

#### Query Parameters
- uid
- token_user

### Response
#### Request Success 
```json
{
  "success": true,
  "errors": "",
}
```

#### Request Failure
```json
{
  "success": false,
  "errors": "BackEndFailure/BadTokenError/BadUID"
}
```

## Action Items
App periodically checks in with the backend to see if there are incoming updates (for example, any successful matches, or nearby matched interest user).

### [GET] 
```curl
GET /actions/
```

#### Query Parameters
- token_user

### Response
#### Request Success 
```json
{
  "success": true,
  "actions": {
    "nearby" : ["uid1", "uid2", "..."],
    "match_approved": ["uid1", "uid2", "..."],
    "match_received": ["uid1", "uid2", "..."],
  },
  "errors": "",
}
```

#### Request Failure
```json
{
  "success": false,
  "actions": [],
  "errors": "BackEndFailure/BadTokenError/BadUID"
}
```

## Stat Board
App periodically requests backend for information on user's
statistics.

### [GET] 
```curl
GET /statboard/
```

#### Query Parameters
- token_user

### Response
#### Request Success 
```json
{
  "success": true,
  "number_active_matches": 5,
  "number_incoming_matches": 10,
  "number_outgoing_matches": 7,
  "errors": "",
}
```

#### Request Failure
```json
{
  "success": false,
  "number_active_matches": -1,
  "number_incoming_matches": -1,
  "number_outgoing_matches": -1,
  "errors": "BackEndFailure/BadTokenError"
}
```
