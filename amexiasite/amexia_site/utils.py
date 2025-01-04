import jwt
from django.conf import settings
from datetime import datetime, timedelta

def generate_jwt_token(user):
    payload = {
        'user_id': user.id,
        'name': user.name,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token
