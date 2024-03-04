# User creation
from django.http import HttpResponse
from general.errors import errorInvalidMethod, errorResponse
from models.models import User
from hashlib import sha256
import json
from .validation import passwordValidation, emailValidation, usernameValidation, pfpValidation
from sessions.sessions import validate
import logging
import pyotp
import re

def userEndpoint(request):
    match(request.method):
        ########################################################################
        # GET - /user                                                          #
        #                                                                      #
        # Gets information about a logged in user via their session cookie     #
        ########################################################################
        case 'GET': # Get a user based on a cookie
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

        ########################################################################
        # POST - /user                                                         #
        #                                                                      #
        # Creates a user based on the json provided in the body                #
        # Expected JSON:                                                       #
        # {                                                                    #
        #     username: string // Validated by usernameValidation              #
        #     email: string // Validated by emailValidation                    #
        #     password: string // Validated by passwordValidation              #
        #     password_validation: string // Should be the same as `password`  #
        # }                                                                    #
        ########################################################################
        case 'POST':
            # Parse JSON
            data = None
            try:
                data = json.loads(request.body)
            except:
                return errorResponse(400, 'Invalid body')

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

            # Update user on database
            u.save()
            return HttpResponse()

        ########################################################################
        # PATCH - /user                                                        #
        #                                                                      #
        # Updates a user using the json in the body                            #
        # Expected JSON:                                                       #
        # {                                                                    #
        #     username: string // A users new username. Has to be unique, and  #
        #                         is validated by usernameValidation           #
        #     email: string // A users email. Has to be unique, and is         #
        #                      validated by emailValidation                    #
        #     password: string // A users current password. This is required   #
        #                         to update any user information               #
        #     new_password: string // Validated by passwordValidation          #
        #     new_password_validaion: string // Should be the same as          #
        #                                       `new_password`                 #
        #     pfp: string // Base64 encoded JPEG string, validated by          #
        # }                  pfpValidation                                     #
        ########################################################################
        case 'PATCH': # Update User information
            # Validate session
            c = request.COOKIES.get("session")
            if (not request.COOKIES.get("session")):
                return errorResponse(401, "No session cookie")
            u = validate(c)
            if (u == None):
                return errorResponse(401, "Invalid session cookie")

            # Validate body data
            data = None
            try:
                data = json.loads(request.body)
            except:
                return errorResponse(400, "Invalid body")

            keys = ['username', 'email', 'password', 'new_password', 'new_password_validation', 'pfp']
            if (not all(key in data for key in keys)):
                return errorResponse(400, "Invalid body")

            # Check password validity
            h = sha256()
            h.update(str.encode(data['password']))

            if (h.hexdigest() != u.password):
                return errorResponse(401, "Invalid credentials")

            # validate username & email
            if (u.username != data["username"]): # If the username has been updated
                if (not usernameValidation(data['username'])):
                    return errorResponse(400, 'Invalid username')
                if (User.objects.filter(username=data['username']).exists()):
                    return errorResponse(409, 'Email already taken')
            if (u.email != data["email"]): # If the username has been updated
                if (not emailValidation(data['email'])):
                    return errorResponse(400, 'Invalid email')
                if (User.objects.filter(email=data['email']).exists()):
                    return errorResponse(409, 'Email already taken')


            u.username = data['username']
            u.email = data['email']

            # New password validation
            # If both of these fields are left blank the password wont be updated
            if (data['new_password'] or data['new_password_validation']):
                if (data['new_password'] != data['new_password_validation']): # Check if passwords are equal
                    return errorResponse(400, "New passwords do not match")
                if (not passwordValidation(data['new_password'])): # Validate new password
                    return errorResponse(400, "New password does not match requirements")

                # Update user password
                h = sha256()
                h.update(str.encode(data['new_password']))
                u.password = h.hexdigest()

            # Pfp validation if the pfp has been updated
            if (u.pfp != data['pfp']):
                if (not pfpValidation(data['pfp'])):
                    return errorResponse(400, "PFP not in correct format, expected data:image/jpeg;base64")
                u.pfp = data['pfp']

            # Update the database
            u.save()

            res = HttpResponse()
            res['Content-Type'] = 'application/json'
            res.content = generateUserJson(u)
            return res

        case _:
            return errorInvalidMethod()

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

# Generating 2fa
def userTotp(request):
    match(request.method):
        case "GET":
            res = HttpResponse()
            res['Content-Type'] = 'application/json'
            res.content = f"{{\"totp_secret\": \"{pyotp.TOTP(pyotp.random_base32()).provisioning_uri(name='42 Transcendence')}\"}}"
            return res

        case "POST":
            c = request.COOKIES.get("session")
            if (not request.COOKIES.get("session")):
                return errorResponse(401, "No session cookie")
            u = validate(c)
            if (u == None):
                return errorResponse(401, "Invalid session cookie")

            data = json.loads(request.body)
            # Validate body
            keys = ['totp_secret', 'totp_key']
            if (not all(key in data for key in keys)):
                return errorResponse(400, 'Invalid body')
            if (not re.fullmatch("[A-Z2-7]{32}", data["totp_secret"])
                or not re.fullmatch("[0-9]{6}", data["totp_key"])):
                return errorResponse(400, 'Invalid secret or key')

            # Validate totp
            totp = pyotp.TOTP(data["totp_secret"])
            if (not totp.verify(data["totp_key"])):
                return errorResponse(401, "Invalid TOTP key")

            u.totp_secret = data['totp_secret']
            u.save()

            return HttpResponse()

        case _:
            return errorInvalidMethod()


def generateUserJson(user):
    data = {
        "id": user.id,
        "intra_id": user.intra_id,
        "username" : user.username,
        "email": user.email,
        "pfp": user.pfp,
        "has_2fa" : (user.totp_secret != ""),
    }
    return json.dumps(data)
