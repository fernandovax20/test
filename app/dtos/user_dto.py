from dataclasses import dataclass
from app.models.user import User


@dataclass
class UserDTO:
    id: int
    name: str
    email: str
    created_at: str

    @staticmethod
    def from_model(user: User) -> "UserDTO":
        return UserDTO(
            id=user.id,
            name=user.name,
            email=user.email,
            created_at=user.created_at.strftime("%d/%m/%Y %H:%M"),
        )
