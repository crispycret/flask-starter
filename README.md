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

