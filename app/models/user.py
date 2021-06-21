from sqlalchemy import Boolean, Column, Integer, String
from passlib.hash import pbkdf2_sha256
from core.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    def check_password(self, password: str) -> bool:
        return pbkdf2_sha256.verify(password, self.password)
