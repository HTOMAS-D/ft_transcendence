from django.http import HttpResponse
from models.models import User
import json
import hashlib
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

# Create your views here.
def authenticate_user(request):
    # TODO: actually send an error response
    # Check if the method is actually a post request
    if (request.method != 'POST'):
        return HttpResponse('{"msg": "NOT POST REQUEST"}', content_type='application/json')

    # Get the user
    data = json.loads(request.body)
    u = User.objects.get(username=data['login'])
    # Calculate hash
    h = hashlib.sha256(str.encode(data['password']))
    # Compare hash
    if (u.password == h.hexdigest()):
        return HttpResponse('{"msg": "Correct Password"}', content_type='application/json')
    return HttpResponse('{"msg": "Incorrect password"}', content_type='application/json')