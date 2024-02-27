# User creation
from django.http import HttpResponse
from general.errors import errorInvalidMethod, errorResponse
from models.models import User
from hashlib import sha256
import json
from .validation import passwordValidation, emailValidation, usernameValidation, pfpValidation
from sessions.sessions import validate
import logging

def updateUser(request):
    match(request.method):
        case 'PATCH':
            # Validate session
            c = request.COOKIES.get("session")
            if (not request.COOKIES.get("session")):
                return errorResponse(401, "No session cookie")
            u = validate(c)
            if (u == None):
                return errorResponse(401, "Invalid session cookie")

            # TODO: check totp

            # Validate body data
            data = None
            try:
                data = json.loads(request.body)
            except:
                return errorResponse(400, "Invalid body")

            keys = ['username', 'email', 'password', 'new_password', 'new_password_validation', 'pfp']
            if (not all(key in data for key in keys)):
                return errorResponse(400, "Invalid body")

            # validate username & email
            if (not usernameValidation(data['username'])):
                return errorResponse(400, 'Invalid username')
            if (User.objects.filter(username=data['username']).exists()):
                return errorResponse(409, 'Email already taken')
            if (not emailValidation(data['email'])):
                return errorResponse(400, 'Invalid email')
            if (User.objects.filter(email=data['email']).exists()):
                return errorResponse(409, 'Email already taken')


            u.username = data['username']
            u.email = data['email']

            h = sha256()
            h.update(str.encode(data['password']))
            pw_h = h.hexdigest()

            if (pw_h != u.password):
                return errorResponse(401, "Invalid credentials")

            # Password validation if necessary (these fields can be blank)
            if (data['new_password'] or data['new_password_validation']):
                if (not data['new_password'] or not data['new_password_validation']):
                    return errorResponse(400, "Invalid body")

                if (data['new_password'] != data['new_password_validation']):
                    return errorResponse(400, "New passwords do not match")
                if (passwordValidation(rdata['new_password'])):
                    return errorResponse(400, "New password does not match requirements")

                h = sha256()
                h.update(str.encode(data['new_password']))
                u.password = h.hexdigest()

            # Pfp validation if required
            if (data['pfp']):
                if (pfpValidation):
                    return errorResponse(400, "PFP not in correct format, expected data:image/jpeg;base64")
                u.pfp = data['pfp']
            u.save()

def registerUser(request):
    match(request.method):
        case 'POST':
            data = json.loads(request.body)
            # Validate body
            keys = ['username', 'email', 'password', 'password_validation']
            if (not all(key in data for key in keys)):
                return errorResponse(400, 'Invalid body')

            # Check uniqueness of username & email
            if (User.objects.filter(username=data['username']).exists()):
                return errorResponse(409, 'Username already in use')
            if (User.objects.filter(email=data['email']).exists()):
                return errorResponse(409, 'Email already in use')

            # Validate email & username
            if (not usernameValidation(data['username'])):
                return errorResponse(400, 'Invalid username')
            if (not emailValidation(data['email'])):
                return errorResponse(400, 'Invalid email')

            # Validate password
            if (data['password'] != data['password_validation']):
                return errorResponse(400, 'Password and validation do not match')
            if (not passwordValidation(data['password'])):
                return errorResponse(400, 'Password is not strong enough')

            # Create User
            u = User.objects.create()
            u.username = data['username']
            u.email = data['email']

            h = sha256()
            h.update(str.encode(data['password']))
            u.password = h.hexdigest()

            u.save()
            return HttpResponse()
        case _:
            return errorInvalidMethod()

def registerOauth(request):
    return HttpResponse("hello")

def getUserById(request, user_id):
    match(request.method):
        case 'GET':
            # Get the user
            u = None
            try:
                u = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return errorResponse(404, 'User not found')

            # generate and return User json
            res = HttpResponse()
            res['Content-Type'] = 'application/json'
            res.content = generateUserJson(u)
            return res
        case _:
            return errorInvalidMethod()

def getUserByCookie(request):
    # Validate session
    c = request.COOKIES.get("session")
    if (not request.COOKIES.get("session")):
        return errorResponse(401, "No session cookie")
    u = validate(c)
    if (u == None):
        return errorResponse(401, "Invalid session cookie")

    # generate response
    res = HttpResponse()
    res['Content-Type'] = 'application/json'
    res.content = generateUserJson(u)
    return res

    u = validate()

def getUserByUsername(request, username):
    match (request.method):
        case 'GET':
            u = None
            try:
                u = User.objects.get(username=username)
            except User.DoesNotExist:
                return errorResponse(404, 'User not found')
            res = HttpResponse()
            res['Content-Type'] = 'application/json'
            res.content = generateUserJson(u)
            return res
        case _:
            return errorInvalidMethod()

def generateUserJson(user):
    data = {
        "id": user.id,
        "intra_id": user.intra_id,
        "username" : user.username,
        "email": user.email,
        "pfp": user.pfp,
    }
    return json.dumps(data)
