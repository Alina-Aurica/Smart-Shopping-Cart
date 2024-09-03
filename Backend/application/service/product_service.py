from application.dto.productDTO import ProductDTO
from application.model.models import Product
from application.repository.product_repository import ProductRepository


class ProductService:
    @staticmethod
    def create_product(**data):
        product_DTO = ProductDTO()
        product_data = product_DTO.load(data)

        product_new = Product(name=product_data.get('name'),
                              quantity_min=product_data.get('quantity_min'),
                              quantity_max=product_data.get('quantity_max'),
                              stock=product_data.get('stock'),
                              image_url=product_data.get('image_url')
                              )

        return ProductRepository.add_product(product_new)

    @staticmethod
    def delete_product(product_id):
        return ProductRepository.delete_product(product_id)

    @staticmethod
    def update_product(product_id, data):
        return ProductRepository.update_product(product_id, data)

    @staticmethod
    def get_product_by_id(product_id):
        return ProductRepository.find_product_by_id(product_id)

    @staticmethod
    def get_product_by_name(product_name):
        return ProductRepository.find_product_by_name(product_name)

    @staticmethod
    def get_all_products():
        products = ProductRepository.find_all_products()
        return [product.repr() for product in products]
