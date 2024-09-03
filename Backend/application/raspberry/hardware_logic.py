from application import db
from application.raspberry.servoMotors import *
from application.raspberry.weight import weight_logic
from application.service.product_service import ProductService
from application.service.shopping_list_service import ShoppingListService
from application.service.weight_service import WeightService

# functia de verificare a greutatii
def process_weight_value(weight_value, user_id, shopping_list_item):
    # verificam ultima valoare inregistrata de senzor inainte de acest produs
    # daca nu exista, se initializeaza cu 0
    weight_list = WeightService.get_all_weights_ordered_by_register_at(user_id)
    if len(weight_list) == 0:
        weight_list_last_value = 0
    else:
        weight_list_last_value = weight_list[0]["weight_value"]

    # se face diferenta dintre valoarea curenta integistrata si ultima valoare din DB
    weight_difference = weight_value - weight_list_last_value
    # se verifica greutatea
    product = ProductService.get_product_by_id(shopping_list_item.id_product)
    for i in range(shopping_list_item.number_of_products, 0, -1):
        if i != 0:
            # daca greutatea e okay, se scade nr de produse si se marcheaza ca recunoscut
            # altfel, se returneaza un obiect None
            if product.quantity_min <= weight_difference / i <= product.quantity_max:
                shopping_list_item.number_of_products -= i
                shopping_list_item.recognised = True
                db.session.commit()
                WeightService.create_weight(user_id, weight_value)
                return shopping_list_item
        else:
            return None
    return None


# logica scanarii de produse
def logic_project(label, user_id):
    # initializare servo-uri
    pwm1, pwm2 = init_servos()
    pwm1.start(0)
    pwm2.start(0)

    # verificam daca produsul se afla in lista
    # daca da, si cantitatea e mai mare ca 0 => se deschid usile si se verifica greutatea
    # altfel, se arunca un mesaj de eroare
    shopping_list_item = ShoppingListService.find_shopping_list_by_product_name(label)
    if shopping_list_item and shopping_list_item.number_of_products != 0:
        # deschidere capac
        try:
            servos_open_lid(pwm1, pwm2)
            time.sleep(5)
        except KeyboardInterrupt:
            pass

        # verificare greutate
        try:
            # valoarea primita de la senzor
            weight = weight_logic()
            # verificam daca se potriveste greutatea produsului
            shopping_list_item_new = process_weight_value(weight, user_id, shopping_list_item)
        except:
            shopping_list_item_new = None

        # daca produsul are greutatea potrivita => usile se inchid
        # altfel, mesaj de eroare
        if shopping_list_item_new:
            try:
                servos_close_lid(pwm1, pwm2)
                time.sleep(5)
            except KeyboardInterrupt:
                pass

            gpio_cleanup(pwm1, pwm2)
            return shopping_list_item
        else:
            gpio_cleanup(pwm1, pwm2)
            return "Too many/less products"
    else:
        return "No product found"


# functia de inchidere a capacului,
# pentru cazul in care:
# produsul exista pe lista,
# dar nu are o greutate corespunzatoare
def close_servo():
    # initializare servo-uri
    pwm1, pwm2 = init_servos()
    pwm1.start(0)
    pwm2.start(0)

    time.sleep(3)
    try:
        # mutare servo-uri in pozitia de inchis
        servos_close_lid(pwm1, pwm2)
        time.sleep(5)
    except KeyboardInterrupt:
        pass

    # se sterge semnalul de pe pini
    gpio_cleanup(pwm1, pwm2)

    return True
