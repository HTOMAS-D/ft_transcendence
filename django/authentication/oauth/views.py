from django.http import HttpResponse
from models.models import User
from general.errors import errorResponse
import requests
import logging
import os
import sessions
import urllib.parse
import datetime

logger = logging.getLogger(__name__)

# This is just a test function to with a button to go to the oauth
# TODO: refactor this once we have an actual place for the oauth button
def oauth_test(request):
    test_button = f'\
    <head>\
        <meta charset="UTF-8">\
        <meta name="viewport" content="width=device-width, initial-scale=1.0">\
        <title>OAUTH TEST</title>\
    \
        <!-- Include Bootstrap CSS -->\
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">\
    </head>\
    <body>\
    \
    <!-- Bootstrap-style Button -->\
    <a href="https://api.intra.42.fr/oauth/authorize?client_id={os.environ.get("INTRA_ID")}&redirect_uri={urllib.parse.quote(os.environ.get("INTRA_REDIRECT_URI"), safe='')}&response_type=code" class="btn btn-primary">Try OAUTH</a>\
    '
    res = HttpResponse(test_button, content_type="text/html")
    return res

def oauth_callback(request):

    code = request.GET.get('code')

    if (not code):
        return errorResponse(400, 'No code provided')

    u = None
    try:
        # Convert a code to a token
        res = requests.post('https://api.intra.42.fr/oauth/token', params={
            'grant_type':'authorization_code',
            'client_id': os.environ.get('INTRA_ID'),
            'client_secret': os.environ.get('INTRA_SECRET'),
            'code': code,
            'redirect_uri': os.environ.get("INTRA_REDIRECT_URI")
        })

        token = res.json().get('access_token')

        # Obtain the owner of the token
        res = requests.get('https://api.intra.42.fr/v2/me', headers={'Authorization': f'Bearer {token}'}).json()
        # Get and/or create user
        # TODO: update this to use a user management service
        u, c = User.objects.get_or_create({'intra_id': res['id']})
        if (c):
            u.username = res['login']
            u.email = res['email']

        u.save()
    except:
        return errorResponse(500, 'Intra Api issues')

    # Return response with session cookie
    res = HttpResponse()
    res.status_code = 200
    t = 'session'
    if (u.totp_secret):
        t = 'temp'
    s = sessions.create(u, t)
    sd = sessions.decode(s)
    res.set_cookie('session', s, expires=datetime.datetime.fromtimestamp(sd['exp']), httponly=True)
    return res