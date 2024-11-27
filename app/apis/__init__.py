from flask import Blueprint, jsonify
from . import service

# main api blueprint
api = Blueprint('api', __name__, url_prefix='/api')


# service api 
from . import service, general_api, admin, customer, professional
api.register_blueprint(service.service)
api.register_blueprint(general_api.gen_api)
api.register_blueprint(admin.admin_api)
api.register_blueprint(customer.customer_api)
api.register_blueprint(professional.professional_api)




@api.route('/test')
def test():
    return jsonify(
        {
            'message' : "api is working fine."
        }
    )