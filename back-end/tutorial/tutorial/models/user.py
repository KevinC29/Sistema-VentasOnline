import bcrypt
from sqlalchemy import (
    Column,
    Integer,
    Text,
)
# from enum import Enum
from .meta import Base

# class RoleEnum(Enum):
#     PERSON = 'person'
#     ADMIN = 'admin'

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False, unique=True)
    role = Column(Text, nullable=False)

    password_hash = Column(Text)

    def set_password(self, pw):
        pwhash = bcrypt.hashpw(pw.encode('utf8'), bcrypt.gensalt())
        self.password_hash = pwhash.decode('utf8')

    def check_password(self, pw):
        if self.password_hash is not None:
            expected_hash = self.password_hash.encode('utf8')
            return bcrypt.checkpw(pw.encode('utf8'), expected_hash)
        return False

    def user_to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "role": self.role,
            "password_hash": self.password_hash
        }