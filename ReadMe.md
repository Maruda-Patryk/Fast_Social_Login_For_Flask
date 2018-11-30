# Easy Social Login (With OAuth2)

Easy Social Login is a mini library for falsk which help user to login with popular social platform

Supported social profile
  - Google Account 
  - Facebook Account (Soon)
  - GitHub Account (Soon)
  - Linkedin Account (Soon)
 

# Google Account

  - You can chose scope that your aplication will be required
  - Create decorator with only one method
  - Get email , full-name , domain and photo from user's resources 

### Installation

To authorizate with Easy Social Login you must create 'OAuth' object 
Note that 'app' object is a Flask Class instance

```python
from google_login.login_with_google import OAuth

oauth = OAuth(app , 'web_client.json')
```
The 'web_client.json'is a .json file that you need to generate in you project on [GCP Console](https://console.cloud.google.com/)
(In credentail section: OAuth Client Id > Web aplication)


Note that the object named app in code is a Flask Class instance 
and remember that you need to create secret_key for you app 
```python
app = Flask(__name__)

app.secret_key = 'super_secret'
```

### How To Use

Implement 'login required' decorator

```python
@app.route('/login')
@oauth.login_required
def this_function_required_google_auth():
    ...
```

After authorization user will be redirect to previous page 

```python
@app.route('/some_path/that_user/copy_to/browser')
@oauth.login_required
def after_succes_login_user_will_return_here():
    return (request.url).__str__()
```


To get curent user's resorce

```python
@app.route('/paht')
@oauth.login_required
def this_function_print_users_resource():
    print(oauth.name)
    print(oauth.email)
    print(oauth.picture)
    if hasattr(oauth , 'domain'):
        print(oauth.domain)
    return ''
```

Revoke authoriazation

```python
@app.route('/sign-out')
@oauth.login_required
def sign_out():
    oauth.clear()
    return 'Bye Bye'
```

You can also use oauth instance on bluprint by import from __main__

in blueprint.py file
```python
...
from __main__ import oauth

some_blueprint = flask.Blueprint('some_blueprint', __name__)

@some_blueprint.route('/blueprint-path')
@oauth.login_required
def function_from_blueprint():
    return 'Hi {}, you are in blueprint'.format(oauth.name)
```

### Required Libs

[Google auth oauthlib](https://pypi.org/project/google-auth-oauthlib/)

```sh
$ pip install --upgrade google-auth-oauthlib
```


[Google's python lib](https://developers.google.com/api-client-library/python/)

```sh
$ pip install --upgrade google-api-python-client
```

### The Full Exemple 


```tree
|-exemple.py
|-web_client
|-google_login
| |-login_with_google.py
| |-...
```

In exemple.py
```python
from flask import Flask
from google_login.login_with_google import OAuth

app = Flask(__name__)
app.secret_key = 'super_secret'

oauth = OAuth(app , 'web_client.json')

@app.route('/login')
@oauth.login_required
def login():
    return 'Hello' + oauth.email

@app.route('/sign-out')
@oauth.login_required
def sign_out():
    oauth.clear()
    return 'Bye Bye'
```

How 'web_client.json' file should look (of course all keys should be fill with values)

```json
{"web":{"client_id":"","project_id":"","auth_uri":"","token_uri":"","auth_provider_x509_cert_url":"","client_secret":"","redirect_uris":[""]}}
```

### OAuth object resources

Model of login user:
```json
{
    "email":<current_user_email_addres>,
    "picture":<curent_user_picture>,
    "name":<curent_user_full_name> 
}
```
The name resources is <first_name> and <last_name> 

Only if user use G suite:
```json
{
    ...
    "domain":<curent_user_domain> 
}
```

In other case this key doesn't exist


