from typing import List
from fastapi import APIRouter, Security, status, Response, HTTPException, Depends
from core.dependencies import security, is_authentication, is_admin
from fastapi.encoders import jsonable_encoder
from schemas.user import UserDetail, UserCreate, UserUpdate
from services.user import get_users, get_user_by_id, user_delete, user_create, update_user

router = APIRouter()


@router.get(
    '/users',
    response_model=List[UserDetail],
    dependencies=[Security(security), Depends(is_authentication)]
)
def get_list_users():
    users = get_users()
    return users


@router.get(
    '/users/{user_id}',
    response_model=UserDetail,
    dependencies=[Security(security), Depends(is_authentication)]
)
def get_user(user_id: int):
    user = get_user_by_id(user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail='user not found')

    return user.User


@router.delete(
    '/users/{user_id}/delete',
    dependencies=[Security(security), Depends(is_authentication), Depends(is_admin)]
)
def delete_user(user_id: int):
    user = user_delete(user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail='user not found')

    return Response(status_code=status.HTTP_200_OK)


@router.post(
    '/users',
    response_model=UserDetail,
    dependencies=[Security(security), Depends(is_authentication), Depends(is_admin)]
)
def create_user(user: UserCreate):
    new_user = user_create(user=user)
    return new_user


@router.put(
    '/users/{user_id}/update',
    dependencies=[Security(security), Depends(is_authentication), Depends(is_admin)]
)
def user_update(user_id: int, data: UserUpdate):
    data = jsonable_encoder(data)
    update_user(user_id=user_id, data=data)
    return Response(status_code=status.HTTP_200_OK)