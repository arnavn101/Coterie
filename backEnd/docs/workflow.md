
## Initial New User

### Create a new account

Used Initially by new user. Response returns an access token 
which can be used to login until expiration.

### Check Logged in Status
Used everytime the user enters the app after initial creation. 
If token has expired, log out. 

### Log into account

Used to generate new tokens after expiration. Returns
another access token. 

## After log in

### Check Profile Creation

Used to check whether the logged in user is a returning or
first time user.

### Startup Page for user

Ask user for details (profile picture, name) and use field availability endpoint to
get all the fields that can be selected.

### Send user profile information to backend

Used after startup page and updates all the user's fields
in the backend.

## Periodic Tasks

### Location of user
Send user coordinates (lang, long) in addition to nearby bluetooth
devices to backend. For bluetooth usage, refer to https://stackoverflow.com/a/57890562/11761743


### Activity Board
Shows number of active matches, outgoing matches,
and incoming matches.

If clicked, gets list of active matches, 
list of recent outgoing matches, and 
list of incoming matches.

### Similar Users Card
Shows users based on similar interests. If clicked
on specific user, show their individual card.
