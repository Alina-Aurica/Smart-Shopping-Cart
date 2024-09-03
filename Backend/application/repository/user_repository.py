from application import db
from application.model.models import User


# db.session.add() - adaugare in baza de date
# db.session.delete() - stergere din baza de date
# db.session.commit() - salvarea schimbarilor in baza de date
# query - pentru interogari de tip SELECT... FROM... WHERE...
class UserRepository:
    @staticmethod
    def add_user(user):
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def delete_user(user_id):
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return True
        return False

    @staticmethod
    def update_user(user_id, data):
        user = User.query.get(user_id)
        if user:
            user.name = data.get('name', user.name)
            user.email = data.get('email', user.email)
            user.password = data.get('password', user.password)
            db.session.commit()
        return user

    @staticmethod
    def find_user_by_id(user_id):
        return User.query.get(user_id)

    @staticmethod
    def find_user_by_name(name):
        return User.query.filter_by(name=name).first()

    @staticmethod
    def find_user_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def find_user_by_password(password):
        return User.query.filter_by(password=password).first()

    @staticmethod
    def find_user_by_email_and_password(email, password):
        return User.query.filter_by(email=email, password=password).first()
