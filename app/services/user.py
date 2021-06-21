from typing import Union
from fastapi import HTTPException
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from core.config import settings
from core.database import db
from models.user import User
from psycopg2 import errors
from schemas.user import UserSingUp, UserCreate


def user_create(user: UserSingUp):
    """
    Создаем пользователя при регистрации без прав суперпользователя
    :param user:
    :return:
    """
    try:
        with db.session() as session:
            user_password = password_hash(password=user.password)
            user = User(
                email=user.email,
                password=user_password,
                first_name=user.first_name,
                last_name=user.last_name
            )
            session.add(user)
            session.commit()
            session.refresh(user)

        return user

    # UniqueViolation except
    except IntegrityError as e:
        # обертка с проверкой на дубликат записи в бд
        assert isinstance(e.orig, errors.lookup("23505"))
        raise HTTPException(status_code=400, detail='A duplicate user already exists')


def user_create_by_admin(user: UserCreate):
    try:
        with db.session() as session:
            user_password = password_hash(password=user.password)
            user = User(
                email=user.email,
                password=user_password,
                first_name=user.first_name,
                last_name=user.last_name,
                is_superuser=user.is_superuser,
            )
            session.add(user)
            session.commit()
            session.refresh(user)

        return user

    # UniqueViolation except
    except IntegrityError as e:
        assert isinstance(e.orig, errors.lookup("23505"))
        raise HTTPException(status_code=400, detail='A duplicate user already exists')


def password_hash(password):
    """
    При создании пользователя хештруем его пароль и кладем хеш уже в базу
    :param password:
    :return:
    """
    return pbkdf2_sha256.hash(password, rounds=200000, salt=settings.SECRET_KEY)


def get_user_by_id(user_id: int) -> Union[User, None]:
    with db.session() as session:
        user = session.execute(
            select(User).filter_by(id=user_id, is_active=True)
        ).first()
    return user


def user_delete(user_id: int) -> bool:
    """
    orm: update(User).where(User.id == user_id, User.is_active is True).values(is_active=False)
    :param user_id:
    :return:
    """
    with db.session() as session:
        result = session.execute(
            f"""
            UPDATE public.user
            SET is_active = false
            WHERE id = {user_id} AND is_active is true;
            """
        )
        session.commit()
    return bool(result)


def update_user(user_id: int, data: dict) -> None:
    """
    Динамическое обновление пользователя, какие поля заполнены такие и обновляем
    :param user_id:
    :param data:
    :return:
    """
    # исключает все None поля
    data = {k: v for k, v in data.items() if v}
    # если обновляем пароль, то сначала хешируем
    if 'password' in data:
        data['password'] = password_hash(password=data['password'])

    with db.session() as session:
        session.execute(
            update(User).
            where(User.id == user_id).
            values(**data)
        )
        session.commit()


def get_user_by_email(email: str) -> Union[User, None]:
    with db.session() as session:
        user = session.execute(
            select(User).filter_by(email=email, is_active=True)
        ).first()
    return user


def get_users():
    """
    SELECT id, first_name, last_name, email, is_active, is_superuser
    FROM public.user
    """
    with db.session() as session:
        users = session.execute(
            select(User)
        ).fetchall()

    return [user.User for user in users]
