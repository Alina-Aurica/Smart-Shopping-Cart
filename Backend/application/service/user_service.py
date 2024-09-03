from application.dto.userDTO import UserDTO
from application.model.models import User
from application.repository.user_repository import UserRepository
from werkzeug.security import generate_password_hash


class UserService:
    @staticmethod
    def create_user(**data):
        user_DTO = UserDTO()
        # validarea datelor prin DTO
        user_data = user_DTO.load(data)

        # criptarea parolei
        hashed_password = generate_password_hash(user_data.get('password'))
        user_new = User(name=user_data.get('name'),
                        email=user_data.get('email'),
                        password=hashed_password,
                        role=user_data.get('role')
                        )

        # verificare unicitatii email-ului
        if UserRepository.find_user_by_email(user_data.get('email')) is None:
            return UserRepository.add_user(user_new)
        return None

    @staticmethod
    def get_user_by_id(user_id):
        return UserRepository.find_user_by_id(user_id)

    @staticmethod
    def get_user_by_email(email):
        return UserRepository.find_user_by_email(email)

    @staticmethod
    def get_user_by_email_and_password(email, password):
        return UserRepository.find_user_by_email_and_password(email, password)