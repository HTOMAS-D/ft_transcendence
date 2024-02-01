from models.models import User
import os
import jwt
import pyotp
import time
import logging

################################################################################
# Session JWT                                                                  #
#                                                                              #
# ownerId : user.id                                                            #
# type: string : 'session', 'totp', 'temp'                                     #
# iat: number, ISO 8601                                                        #
# exp: number, ISO 8601                                                        #
#                                                                              #
# temp type is used when authenticating but it still needs a totp code         #
################################################################################

ENCR_METHOD="HS256"

# Creates a session, returns a JWT
def create(user: User,
           t: str,
           session_length : int = int(os.environ.get("SESSION_LENGTH", 3600))) -> str:
    jwt_secret = os.environ.get('JWT_SECRET')
    data = {
        'ownerId' : user.id,
        'type' : t,
        'iat':  int(time.time()),
        'exp': int(time.time()) + session_length,
    }
    return jwt.encode(data, os.environ.get("JWT_SECRET"), ENCR_METHOD)

# Validates a session token (JWT)
# You can optionally provide a type to validate that the JWT is a certain type
# If it's an invalid session it will return None, otherwise it will return the user id
def validate(token: str, t: str = '') -> User:
    try:
        data = jwt.decode(token, os.environ.get("JWT_SECRET"), ENCR_METHOD)
        if (time.time() > data['exp'] or (t != '' and data['type'] != t)):
            return None
        try:
            return User.objects.get(id=data['ownerId'])
        except:
            return None
    except:
        return None

def decode(token) -> any:
    try:
        return jwt.decode(token, os.environ.get("JWT_SECRET"), ENCR_METHOD)
    except:
        return None

# Validates a totp key
def validate_totp(user: User, key : str) -> bool:
    totp = pyotp.TOTP(user.totp_secret)
    return totp.verify(key)

