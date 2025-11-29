from app import dbq
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.user_roles_model import UserRoles
class Users(dbq.Model):
    user_id: Mapped[str] = mapped_column(String(255), primary_key=True, nullable=False, unique=True)
    user_role: Mapped[str] = mapped_column(Integer, nullable=False)
    username: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)

    def to_dict(self) -> dict:
        return {
            "user_id": self.user_id,
            "user_role": Users.retrieve_user_role_title(self.user_id),
            "username": self.username,
            "full_name": self.full_name,
        }
    
    @staticmethod
    def user_exists(username: str) -> bool:
        return dbq.session.query(Users).filter_by(username=username).first() is not None
    
    @staticmethod
    def retrieve_all_users() -> list:
        users = dbq.session.query(Users).all()
        return [u.to_dict() for u in users]
    
    @staticmethod
    def retrieve_user_by_id(user_id: str):
        return dbq.session.query(Users).filter_by(user_id=user_id).first()
    
    @staticmethod
    def retrieve_user_by_username(username: str):
        return dbq.session.query(Users).filter_by(username=username).first()
    
    @staticmethod
    def retrieve_user_id(username: str):
        result = dbq.session.query(Users.user_id).filter_by(username=username).first()
        return result[0] if result is not None else None
    
    @staticmethod
    def retrieve_user_role_title(user_id: str):
        user_role_id = dbq.session.query(Users.user_role).filter_by(user_id=user_id).first()
        result = dbq.session.query(UserRoles.user_role_title).filter_by(user_role_id=user_role_id[0]).first()
        return result[0] if result is not None else None
    
    @staticmethod
    def retrieve_username(user_id: str):
        result = dbq.session.query(Users.username).filter_by(user_id=user_id).first()
        return result[0] if result is not None else None
    
    @staticmethod
    def retrieve_password(user_id: str):
        result = dbq.session.query(Users.password).filter_by(user_id=user_id).first()
        return result[0] if result is not None else None
    
    @staticmethod
    def retrieve_full_name(user_id: str):
        result = dbq.session.query(Users.full_name).filter_by(user_id=user_id).first()
        return result[0] if result is not None else None
    
    @staticmethod
    def retrieve_latest_user_id() -> str:
        latest = dbq.session.query(Users.user_id).order_by(Users.user_id.desc()).first()
        return latest[0] if latest is not None else None
    
    @staticmethod
    def add_user(user_id: str, user_role: int, username: str, password: str, full_name: str) -> None:
        new_user = Users(
            user_id=user_id,
            user_role=user_role,
            username=username,
            password=password,
            full_name=full_name
        )
        dbq.session.add(new_user)
        dbq.session.commit()