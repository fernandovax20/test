from datetime import datetime, timezone


class User:
    def __init__(self, id: int, name: str, email: str, created_at: datetime = None):
        self.id = id
        self.name = name
        self.email = email
        self.created_at = created_at or datetime.now(timezone.utc)

    @staticmethod
    def from_row(row: tuple) -> "User":
        return User(id=row[0], name=row[1], email=row[2], created_at=row[3])

    @classmethod
    def all(cls) -> list["User"]:
        from app.repositories.user_repository import UserRepository
        return UserRepository.find_all()

    @classmethod
    def find(cls, user_id: int) -> "User | None":
        from app.repositories.user_repository import UserRepository
        return UserRepository.find_by_id(user_id)

    @classmethod
    def search(cls, query: str) -> list["User"]:
        from app.repositories.user_repository import UserRepository
        return UserRepository.search(query)

    @classmethod
    def find_by_email(cls, email: str) -> "User | None":
        from app.repositories.user_repository import UserRepository
        return UserRepository.find_by_email(email)

    @classmethod
    def create(cls, name: str, email: str) -> "User":
        from app.repositories.user_repository import UserRepository
        return UserRepository.create(name, email)

    def update(self, name: str, email: str) -> "User | None":
        from app.repositories.user_repository import UserRepository
        return UserRepository.update(self.id, name, email)

    def delete(self) -> bool:
        from app.repositories.user_repository import UserRepository
        return UserRepository.delete(self.id)
