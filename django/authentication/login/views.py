from django.http import HttpResponse
from models.models import User
from general.errors import errorResponse, errorInvalidMethod
import sessions
import datetime
import json
import hashlib
import os
import logging

# Authenticates a user via username/password
def authenticate_user(request):
    match(request.method):
        case 'POST':
            # Validate input data
            try:
                data = json.loads(request.body)
            except:
                return errorResponse(400, 'Invalid body')

            keys = ['login', 'password']
            if (not all(key in data for key in keys)):
                return errorResponse(400, 'Invalid body')

            # Get the user
            u = None
            try:
                u = User.objects.get(username=data['login'])
            except:
                try:
                    u = User.objects.get(email=data['login'])
                except:
                    return errorResponse(401, 'Invalid credentials')

            # Calculate hash
            h = hashlib.sha256(str.encode(data['password']))
            # Compare hash
            if (u.password != h.hexdigest()):
                return errorResponse(401, 'Invalid credentials')


            # Create response with session
            res = HttpResponse()
            res.status_code = 200
            if (request.COOKIES.get('session_totp')):
                res.delete_cookie('session_totp') # Make sure the user doesn't have a totp session
            # create session cookie
            t = 'session'
            # If the user has 2fa active create a temp session instead until user is authenticated
            if (u.totp_secret):
                t = 'temp'
            sc = sessions.create(u, t)
            scd = sessions.decode(sc)
            res.set_cookie('session', sc, expires=datetime.datetime.fromtimestamp(scd['exp']), httponly=True)
            return res

        case 'PATCH': # Used for updating temp session once a totp key has been obtained
            # Check if required cookies are present
            if (not request.COOKIES.get('session') or not request.COOKIES.get('session_totp')):
                return errorResponse(400, 'Missing session cookie(s)')
            s_d = None
            s_totp_d = None
            try:
                s_d = sessions.decode(request.COOKIES.get('session'))
                s_totp_d = sessions.decode(request.COOKIES.get('session_totp'))
                if (s_d['ownerId'] != s_totp_d['ownerId']):
                    raise ValueError('ownerId\'s don\'t match')
            except:
                res = errorResponse(401, 'Invalid session cookie(s)')
                res.delete_cookie('session_totp') # make sure the session totp is invalidated
                return res

            u = None
            try:
                u = User.objects.get(id=s_d['ownerId'])
            except:
                res = errorResponse(401, 'Invalid session cookie(s)')
                res.delete_cookie('session_totp') # make sure the session totp is invalidated
                return res

            st = sessions.create(u, 'session')
            st_d = sessions.decode(st)

            res = HttpResponse()
            res.status_code = 200
            res.set_cookie('session', st, expires=datetime.datetime.fromtimestamp(st_d['exp']), httponly=True)
            res.delete_cookie('session_totp')
            return res

        case _:
            return errorInvalidMethod()
