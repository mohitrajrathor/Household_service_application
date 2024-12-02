'''
service.py

This module contains apis related to Service model CRUD and other functionalities related to Service.
'''

# imports
# from . import api
from ..routes.admin import is_admin
from .. import db
from ..models import Service
from flask import request, jsonify, Blueprint
from sqlalchemy.exc import IntegrityError


service = Blueprint('service', __name__, url_prefix='/service')

# create
@service.route('/create', methods=['POST'])
@is_admin
def create_service():
    data = request.get_json()
    name = data['name']
    price = data['price']
    description = data['description']
    time_required = data['time_required']

    new_service = Service(name=name, price=price, time_required=time_required, description=description)
    
    try:
        db.session.add(new_service)
        db.session.commit()
    except IntegrityError as i:
        print(i)
        return jsonify({
            'error' : "integrityerror occured"
        }), 409
    
    return jsonify({"message": f"{name} Service created successfully", "service": new_service.to_dict()}), 201


# get one servies
@service.route('get-<int:service_id>', methods=['GET'])
@is_admin
def get_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify(
            {
                'error' : "Service with id f<{service_id}> not exist"
            }
        )
    
    return jsonify(
        {
            "message" : "Service fetched successfully",
            "service" : service.to_dict()
        }
    ), 200


# get
@service.route('/get-all', methods=['GET'])
@is_admin
def get_all_services():
    services = Service.query.all()
    return jsonify([service.to_dict() for service in services]), 200


# update
@service.route('/update-<int:service_id>', methods=['PUT'])
@is_admin
def update_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404

    data = request.get_json()
    service.name = data.get('name', service.name)
    service.price = data.get('price', service.price)
    service.time_required = data.get('time_required', service.time_required)
    service.description = data.get('description', service.description)
    
    db.session.commit()
    return jsonify({"message": "Service updated successfully", "service": service.to_dict()}), 200


# delete
@service.route('/delete-<int:service_id>', methods=['DELETE'])
@is_admin
def delete_service(service_id):
    service = Service.query.get(service_id)
    if not service:
        return jsonify({"error": "Service not found"}), 404

    db.session.delete(service)
    db.session.commit()
    return jsonify({"message": "Service deleted successfully"}), 200


# search by name
@service.route('/search', methods=['GET'])
@is_admin
def search_services():
    search_term = request.args.get('name')
    services = Service.query.filter(Service.name.ilike(f"%{search_term}%")).all()
    return jsonify([service.to_dict() for service in services]), 200