from models.models import User
import os
import jwt
import time

################################################################################
# Session JWT                                                                  #
#                                                                              #
# ownerId : user.id                                                            #
# iat: number, ISO 8601                                                        #
# exp: number, ISO 8601                                                        #
################################################################################

ENCR_METHOD="HS256"

# Creates a session, returns a JWT
def create(user):
    jwt_secret = os.environ.get('JWT_SECRET')
    data = {
        'ownerId' : user.id,
        'iat':  int(time.time()),
        'exp': int(time.time()) + int(os.environ.get("SESSION_LENGTH", 3600)),
    }
    return jwt.encode(data, os.environ.get("JWT_SECRET"), ENCR_METHOD)

# Validates a session token (JWT)
def validate(jwt):
    try:
        data = jwt.decode(jwt, os.environ.get("JWT_SECRET"), ENCR_METHOD)
        if (time.time() > data['exp']):
            return None
        return data['ownerId']
    except:
        return None
    return

# creates a totp session
def create_totp(user, totp):
    return

# validates a totp session
def validate_totp():
    return
