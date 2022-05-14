# flask-starter
Prebuilt flask app with user authentication and profile.

## Features
 * Authentication
 * User Profile
 * * User Following
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
