#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import json
from flask import session , redirect , url_for , request
from google_auth_oauthlib.flow import Flow


class OAuth(object):
    def __init__(self, app , file_path , redirect_uri=None , scopes = [
            'https://www.googleapis.com/auth/userinfo.profile',
            'https://www.googleapis.com/auth/plus.me',
            'https://www.googleapis.com/auth/userinfo.email']):

        self.app = app
        self.file_path = file_path
        self.scopes = scopes
        if redirect_uri == None:
            self.redirect_uri = open_and_read(file_path)
        else:
            self.redirect_uri = redirect_uri
        self.kwargs = {'scopes':scopes , 'redirect_uri':self.redirect_uri}

    def login_with_google(self , page):
        flow = Flow.from_client_secrets_file(self.file_path,**self.kwargs)

        authorization_url , state = flow.authorization_url(
            include_granted_scopes='true',prompt="select_account")

        session['state'] = state
        session['page'] = page

        return redirect(authorization_url)

    def blueprint_auth(self):
        from urllib.parse import urlparse

        path_to_callback = urlparse(self.redirect_uri)

        @self.app.route(path_to_callback.path)
        def authorization_callback():

            from google.auth.transport.requests import AuthorizedSession

            flow = Flow.from_client_secrets_file(self.file_path,**self.kwargs)
            flow.fetch_token(authorization_response=request.url)

            credentials = flow.credentials
            authed_session = AuthorizedSession(credentials)
            response = authed_session.get('https://www.googleapis.com/userinfo/v2/me').json()
            session['auth_gmail_user'] = {
                    'email':response['email'],
                    'picture':response['picture'],
                    'name':split_full_name(response['name'])
                }

            if 'hd' in response:
                session['auth_gmail_user']['domain'] = response['hd']


            return redirect(session['page'])

    def clear(self):
        del session['auth_gmail_user']

    def login_required(self, page):
        from functools import wraps
        import json
        try:
            self.blueprint_auth()
        except:
            pass
        @wraps(page)
        def decorator(*args , **kwargs):
            if 'auth_gmail_user' in session:
                if not hasattr(self , 'email'):
                    self.email = json.dumps(session['auth_gmail_user']['email'])
                    self.picture = json.dumps(session['auth_gmail_user']['picture'])
                    self.name= User_Name(**session['auth_gmail_user']['name'])

                    if 'domain' in session['auth_gmail_user']:
                        self.domain = json.dumps(session['auth_gmail_user']['domain'])

                return page(*args,**kwargs)
            else:        
                return self.login_with_google(request.url)

        return decorator

class LoginUser(object):
    def __init__(self , email , picture , name):
        self.email = email
        self.picture = picture
        self.name = name 
        
    def _add_domain_if_exist(self , domain):
        self.domain = domain

    @classmethod
    def user_withoud_gsuite(cls , email , picture , name ):
        args = (email , picture , name)
        return cls(*args) 

class User_Name(OAuth):
    def __init__(self, first_name , surname , full_name):
        self.first_name = first_name
        self.surname = surname
        self.full_name = full_name

    def __str__(self):
        return self.full_name.__str__()

def open_and_read(file):
    
    file = open( file , 'r')
    json_file_object = json.loads(file.read())
    first_linkt_to_redirect = json_file_object['web']['redirect_uris'][1]
    file.close()

    return first_linkt_to_redirect

def split_full_name(name):
    name_array = name.split(' ')
    return {'first_name':name_array[0] , 'surname':name_array[1] , 'full_name':name}