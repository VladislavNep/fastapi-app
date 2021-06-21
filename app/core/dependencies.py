from fastapi.security import HTTPBearer
from fastapi import Request
from services.auth import auth
from fastapi import HTTPException, status

security = HTTPBearer()


def is_authentication(request: Request):
    access_token = request.headers.get('Authorization')
    if access_token:
        access_token = access_token.split()[1]
        is_auth = auth.is_authentication(token=access_token)
        if not is_auth:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You UNAUTHORIZED")


def is_admin(request: Request):
    access_token = request.headers.get('Authorization')
    if access_token:
        access_token = access_token.split()[1]
        user = auth.get_jwt_claims(token=access_token)
        if not user['user']['is_superuser']:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Permission Denied")
