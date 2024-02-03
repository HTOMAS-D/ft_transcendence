from django.http import HttpResponse
from models.models import User
from general.errors import errorResponse, errorInvalidMethod
import json
import sessions
import logging
import jwt
import datetime

def authenticate_totp(request):
    match(request.method):
        case 'POST':
            data = None
            totp_token = None
            try:
                data = json.loads(request.body)
                totp_token = data['totp_token']
            except:
                return errorResponse(400, 'Invalid body')
            sc = request.COOKIES.get('session')
            if (not sc):
                return errorResponse(400, 'No session cookie')
            if (not sessions.validate(sc)):
                return errorResponse(401, 'Invalid session cookie')
            scd = sessions.decode(sc)
            u = None
            try:
                u = User.objects.get(id=scd['ownerId'])
            except:
                return errorResponse(500, 'Unkown user')
            if (not sessions.validate_totp(u, totp_token)):
                return errorResponse(401, 'Invalid totp token')

            res = HttpResponse()
            res.status_code = 200
            tjwt = sessions.create(u, 'totp', 60)
            tjwt_d = sessions.decode(tjwt)
            res.set_cookie('session_totp', tjwt, expires=datetime.datetime.fromtimestamp(tjwt_d['exp']), httponly=True)
            return res


        case _:
            return errorInvalidMethod()
