from app import dbq
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

class UserRoles(dbq.Model):
    user_role_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_role_title: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    def to_dict(self) -> dict:
        return {
            "user_role_id": self.user_role_id,
            "user_role_title": self.user_role_title,
        }
    
    @staticmethod
    def retrieve_all_roles() -> list:
        roles = dbq.session.query(UserRoles).all()
        return [r.to_dict() for r in roles]
    
    @staticmethod
    def retrieve_role_by_id(role_id: int):
        return dbq.session.query(UserRoles).filter_by(user_role_id=role_id).first()