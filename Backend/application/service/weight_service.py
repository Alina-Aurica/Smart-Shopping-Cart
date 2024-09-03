from application.dto.weightDTO import WeightDTO
from application.model.models import Weight
from application.repository.weight_repository import WeightRepository


class WeightService:
    @staticmethod
    def create_weight(user_id, weight):
        if weight and user_id:
            weight_new = Weight(id_user=user_id, weight_value=weight)
            return WeightRepository.add_weight(weight_new)
        else:
            return None

    @staticmethod
    def get_weight_by_id(weight_id):
        return WeightRepository.find_weight_by_id(weight_id)

    @staticmethod
    def get_all_weight():
        weights = WeightRepository.find_all_weights()
        return [weight.repr() for weight in weights]

    # returneaza lista cu greutatile inregistrate
    # pentru sesiunea curenta de cumparaturi
    # in ordine descrescatoare
    @staticmethod
    def get_all_weights_ordered_by_register_at(user_id):
        weights = WeightRepository.find_all_weights_ordered_by_register_at(user_id)
        return [weight.repr() for weight in weights]

    # sterge la logOut greutatile sesiunii curente
    @staticmethod
    def delete_weight_by_user_id(user_id):
        weights = WeightRepository.delete_weight_by_user_id(user_id)
        if weights:
            return [weight.repr() for weight in weights]
        else:
            return "No weight"

