from flask import Flask
from flask_cors import CORS

from application.model.models import db
from config import Config

# functia de creere a aplicatiei
def create_app():
    # configurarea aplicatiei
    app = Flask(__name__)
    app.config.from_object(Config)

    from application.model import models

    # initializarea si creerea bazei de date
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # specificarea IP-urilor si port-urilor cu care comunica
    CORS(app, resources={r"/*": {"origins": ["http://localhost:4200", "http://192.168.40.158:4200"]}})

    # instantierea controller-elor
    from .controller.user_controller import user_controller
    app.register_blueprint(user_controller)
    from .controller.product_controller import product_controller
    app.register_blueprint(product_controller)
    from .controller.shopping_list_controller import shopping_list_controller
    app.register_blueprint(shopping_list_controller)
    from .controller.auth_controller import auth_controller
    app.register_blueprint(auth_controller)
    from .controller.inference_controller import inference_controller
    app.register_blueprint(inference_controller)

    return app
