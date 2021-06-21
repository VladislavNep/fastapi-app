import datetime
import jwt
from fastapi import HTTPException
from models.user import User
from core.config import settings
import redis
from services.user import get_user_by_id


class JwtRedis:
    def __init__(self):
        self.redis_instance = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                                          db=settings.REDIS_DB, socket_timeout=5000)

    def remove_jwt_token_redis(self, user_id):
        """
        Удаляем ключи из редиса jwt tokens
        :param user_id:
        :return:
        """
        self.redis_instance.delete(f'{user_id}_REFRESH')
        self.redis_instance.delete(f'{user_id}_ACCESS')

    def set_jwt_token_to_redis(self, user_id, token, type_token, exp):
        """
        Создаем пользовательскую сессию, добавляем токены
        :param user_id:
        :param token:
        :param type_token:
        :param exp:
        :return:
        """
        self.redis_instance.set(name=f"{user_id}_{type_token}", value=token, keepttl=exp)

    def get_jwt_token_from_redis(self, user_id, type_token):
        """
        Забераем jwt token пользователя, для дальнейших манипуляций
        :param user_id:
        :param type_token:
        :return:
        """
        token = self.redis_instance.get(f"{user_id}_{type_token}")
        if token:
            return token.decode('UTF-8')

        return None

    def check_jwt(self, user_id, token, type_token):
        """
        Проверяем совпадает ли токен пользователя пришедший с http запросом,
        с кем который сохранен в рамках его сессии
        :param user_id:
        :param token:
        :param type_token:
        :return:
        """
        token_redis = self.get_jwt_token_from_redis(user_id, type_token)
        return token_redis == token


class Auth(JwtRedis):

    def is_authentication(self, token: bytes) -> bool:
        """
        Проверяем, аунтефицирован ли пользователь
        :param token:
        :return:
        """
        data = self.get_jwt_claims(token=token)
        user_id = data['user']['id']
        is_auth = self.check_jwt(user_id=user_id, token=token, type_token='ACCESS')

        return is_auth

    def logout(self, token: bytes) -> bool:
        """
        При выходе пользователя, затираем все его текущие сессии
        :param token:
        :return:
        """
        data = self.get_jwt_claims(token=token)
        user_id = data['user']['id']
        self.remove_jwt_token_redis(user_id=user_id)
        return True

    def create_access_token(self, user: User) -> bytes:
        """
        Генерируем токен пользователю и создаем сессию в редисе
        :param user:
        :return:
        """
        user_info = {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'is_superuser': user.is_superuser,
        }
        payload = {
            'user': user_info,
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        }

        token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256')
        # пишем в редис
        self.set_jwt_token_to_redis(user_id=user.id, token=token, type_token='ACCESS', exp=87400)

        return token

    def generate_tokens(self, user: User) -> tuple:
        try:
            access_token = self.create_access_token(user=user)
            refresh_token = self.create_refresh_token(user=user)

            return access_token, refresh_token
        except Exception as e:
            print(e)
            raise HTTPException(status_code=401, detail='generation tokens failed')

    def create_refresh_token(self, user: User) -> bytes:
        """
        Генерируем токен пользователю и создаем сессию в редисе
        :param user:
        :return:
        """
        payload = {
            'user': {
                'id': user.id
            },
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
        }
        refresh_token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256')
        self.set_jwt_token_to_redis(user_id=user.id, token=refresh_token, type_token='REFRESH',
                                    exp=605800)

        return refresh_token

    def refresh_token(self, token: bytes) -> tuple:
        """
        Обновляем пару токенов и сессию пользователя
        :param token:
        :return:
        """
        data = self.get_jwt_claims(token=token)
        user_id = data['user']['id']
        is_valid = self.check_jwt(user_id=user_id, token=token, type_token='REFRESH')

        if not is_valid:
            raise HTTPException(status_code=401, detail='Invalid jwt token')

        user = get_user_by_id(user_id=user_id)

        if user is None:
            raise HTTPException(status_code=401, detail='Invalid jwt token')

        access_token, refresh_token = self.generate_tokens(user=user.User)

        return access_token, refresh_token

    def remove_user_session(self, user_id: int) -> None:
        try:
            self.remove_jwt_token_redis(user_id=user_id)
        except Exception as e:
            raise HTTPException(status_code=401, detail='user session not found')

    @staticmethod
    def get_jwt_claims(token: bytes) -> dict:
        """
        Расшифровываем токен пользователя, для получения информации о нем
        :param token:
        :return:
        """
        try:
            data = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
            return data
        except jwt.ExpiredSignatureError:
            print('JWT Token has expired', flush=True)
            raise HTTPException(status_code=401, detail='jwt token expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail='Invalid jwt token')


auth = Auth()
