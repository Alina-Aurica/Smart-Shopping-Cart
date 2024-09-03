from sqlalchemy import desc

from application import db
from application.model.models import Weight


class WeightRepository:
    @staticmethod
    def add_weight(weight):
        db.session.add(weight)
        db.session.commit()
        return weight

    # folosit la logOut
    # pentru a sterge greutatea inregistrata
    # pentru o sesiune de cumparaturi
    @staticmethod
    def delete_weight_by_user_id(user_id):
        weights = Weight.query.filter_by(id_user=user_id).all()
        if weights:
            for weight in weights:
                db.session.delete(weight)
                db.session.commit()
            return weights
        return None

    @staticmethod
    def find_weight_by_id(weight_id):
        return Weight.query.get(weight_id)

    @staticmethod
    def find_all_weights():
        return Weight.query.all()

    # folosit in logic_project
    # pentru a obtine cea mai recenta cantarire
    # pentru o sesiune de cumparaturi
    @staticmethod
    def find_all_weights_ordered_by_register_at(user_id):
        return Weight.query.filter_by(id_user=user_id).order_by(desc(Weight.register_at)).all()
