# flask-starter
Prebuilt flask app with user authentication, user profile, and user following.

## Features
 * Authentication
 * User Profile
    * User Following
 * Database Support



## Generate Application Secret Key
In a python shell generate a secret token for the application. \

```
import secrets
secrets.token_hex(64)
```

Place this token in the .env file of the projects root directory.
#### .env
```
SECRET_KEY=91b47920cca5d2fce10d4096f90c0e69eceae11e0c537a263e22ff11cbacdf34c00492deb6643cf676b68efd12a781ec174ae3abbe7f8f1d83b00a8fee234927
```

## Setup SQLAlchemy Database
```
flask db init
flask db migrate -m "initial migration"
flask db upgrade
```

## Run the Application
```
flask run
```


## Responses

Requests that want to make a change but could not because the state requested is the current state recieve a response code of 202 instead of 200.
Example:
```
Status: 200 -> A user requesting to follow another user that they are not following.
Status: 202 -> A user requesting to follow another user, but is already following that user.
```

## Decorators

This project comes with a set of decorators to add and simplfy common functionality suc as user authentication and user lookups.\
These decorators return keyword arguments such as `token, current_user, target_user` or returns back to the api caller a message stating the error.

#### @token_required -> return token, current_user
#### @target_lookup -> returns target_user

## API Calls
The following is an example of working API calls for this project.

### Non Authentication Calls

##### /register
###### Request
```
{
    "email":"example2@email.com",
    "username": "test002",
    "password": "testpassword"  
}

##### Response
A valid response can be one of the following.
```
{
    "message": "registered successfully"
}
```

```
{
    "message": "username already used"
}
```

```
{
    "message": "email already used"
}
```


### /login
#### Request
The login call expects the login information to be passed through the `Authorization` header.\
The value to the `Authroization` header should be the username and password encoded with `base64` with the format `username:password` after the word `Basic`
```
{
   'Authorization': 'Basic dGVzdDAwMTp0ZXN0cGFzc3dvcmQ='
}
```

#### Response
A successful login response will provide an authorization token for the user that lasts 1 hour.\
This token should be placed in the header `x-access-token`
```
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJwdWJsaWNfaWQiOiJkZTk2NDNjNS02ZTQ1LTQyZWEtYTJlOS03YTA1Yjg3NmUwNTMiLCJjcmVhdGVkIjoiMjAyMi0wNS0xNVQxMjoyMzoxMi4yNzU1NTMiLCJleHBpcmVzIjoiMjAyMi0wNS0xNVQxMzoyMzoxMi4yNzU1NjYifQ.E0x5WInJirl3txAuLY8fEXNJYO_Mu0LhcR9Tp9Zt42o"
}
```

```
```
