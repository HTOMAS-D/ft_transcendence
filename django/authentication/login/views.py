from django.http import HttpResponse
from models.models import User
import sessions
import datetime
import json
import hashlib
import os
import logging

# This is just for testing the login and should be removed once we have a login page
def login_test(request):
    res = '\
    <!DOCTYPE html>\
    <html lang="en">\
    <head>\
        <meta charset="UTF-8">\
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">\
        <title>Login Form</title>\
        <!-- Bootstrap CSS -->\
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">\
    </head>\
    <body>\
    \
    <div class="container mt-5">\
        <div class="row justify-content-center">\
            <div class="col-md-6">\
                <h2 class="text-center mb-4">Login Form</h2>\
                <form id="loginForm">\
                    <div class="form-group">\
                        <label for="usernameEmail">Username/Email</label>\
                        <input type="text" class="form-control" id="usernameEmail" name="usernameEmail" required>\
                    </div>\
                    <div class="form-group">\
                        <label for="password">Password</label>\
                        <input type="password" class="form-control" id="password" name="password" required>\
                    </div>\
                    <button type="button" class="btn btn-primary" onclick="submitLoginForm()">Login</button>\
                </form>\
            </div>\
        </div>\
    </div>\
    \
    <script>\
        function submitLoginForm() {\
            var loginValue = document.getElementById("usernameEmail").value;\
            var passwordValue = document.getElementById("password").value;\
    \
            var jsonData = {\
                "login": loginValue,\
                "password": passwordValue\
            };\
    \
            fetch("/login/", {\
                method: "POST",\
                headers: {\
                    "Content-Type": "application/json",\
                },\
                body: JSON.stringify(jsonData),\
            })\
            .then(data => {\
                console.log("Success:", data.text());\
            })\
            .catch((error) => {\
                console.error("Error:", error);\
            });\
        }\
    </script>\
    \
        </body>\
        </html>\
    '
    return HttpResponse(res)

def errorResponse(code, message) -> HttpResponse:
    res = HttpResponse()
    res.status_code = code
    res.content = f"{'error':'${message}'}"
    res['Content-Type'] = 'application/json'
    return res

# Authenticates a user via username/password
def authenticate_user(request):
    match(request.method):
        case 'POST':
            # Validate input data
            data = json.loads(request.body)
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
            # Validate input data
            data = json.loads(request.body)
            if ('totp_key' not in data):
                return errorResponse(400, 'Invalid body')
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
                u = User.objects.get(id=s_d.ownerId)
            except:
                res = errorResponse(401, 'Invalid session cookie(s)')
                res.delete_cookie('session_totp') # make sure the session totp is invalidated
                return res

            st = sessions.create(u, 'session')
            st_d = sessions.decode(u, st)

            res = HttpResponse()
            res.status_code = 200
            res.set_cookie('session', st, expires=datetime.datetime.fromtimestamp(st_d['exp']), httponly=True)
            return res

        case _:
            return  errorResponse(405, 'Invalid method')
