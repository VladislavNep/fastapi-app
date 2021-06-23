import json
from fastapi import APIRouter, HTTPException, Response, status, Security, Depends
from fastapi.security import HTTPAuthorizationCredentials
from core.dependencies import security, is_authentication
from schemas.user import UserSingUp, UserAuth
from services.auth import auth
from services.user import get_user_by_email, user_create_for_sing_up


router = APIRouter()


@router.post('/signup')
def signup(user_data: UserSingUp):
    new_user = user_create_for_sing_up(user=user_data)
    access_token, refresh_token = auth.generate_tokens(user=new_user)

    return Response(status_code=status.HTTP_200_OK, content=json.dumps(
        {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'is_superuser': new_user.is_superuser
        }
    ))


@router.post('/login')
def login(user_data: UserAuth):
    user = get_user_by_email(email=user_data.email)

    if user is None:
        raise HTTPException(status_code=401, detail='User does not exists')
    elif not user.User.check_password(user_data.password):
        raise HTTPException(status_code=401, detail='Invalid email or password')

    access_token, refresh_token = auth.generate_tokens(user=user.User)

    return Response(status_code=status.HTTP_200_OK, content=json.dumps(
        {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'is_superuser': user.User.is_superuser
        }
    ))


@router.post('/refresh-token')
def refresh_token(credentials: HTTPAuthorizationCredentials = Security(security)):
        refresh_token = credentials.credentials
        new_access_token, new_refresh_token = auth.refresh_token(token=refresh_token)

        return Response(status_code=status.HTTP_200_OK, content=json.dumps(
            {
                'access_token': new_access_token,
                'refresh_token': new_refresh_token
            }
        ))


@router.post('/logout', dependencies=[Depends(is_authentication)])
def logout(credentials: HTTPAuthorizationCredentials = Security(security)):
        access_token = credentials.credentials
        auth.logout(token=access_token)

        return Response(status_code=status.HTTP_200_OK)
