# User creation
from django.http import HttpResponse
from general.errors import errorInvalidMethod, errorResponse
from models.models import User
from hashlib import sha256
import json
from .validation import passwordValidation, emailValidation, usernameValidation

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

        case _:
            return errorInvalidMethod()
    return HttpResponse()

def registerOauth(request):
    return HttpResponse("hello")

def getUser(request):
    return

def getUserIntra(request):
    return