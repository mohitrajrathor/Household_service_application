'''
# apis/customer.py

file to handle customer related logic
'''
from flask import Blueprint, jsonify, session
from ..models import db, ServiceRequest, Reviews, Customer
from datetime import datetime
from sqlalchemy import func

customer_api = Blueprint('customer_api', __name__, url_prefix='/customer')

@customer_api.route('/summary_data', methods=['GET'])
def get_dashboard_data():
    customer_id = session.get('id')
    customer = Customer.query.get(customer_id)

    # Active Service Requests for the customer
    active_requests_count = ServiceRequest.query.filter_by(customer_id=customer.id, service_status='requested').count()

    # Reviews for the customer (if they left reviews)
    reviews_count = Reviews.query.filter_by(cust_id=customer.id).count()

    # Service Requests Over Time (for chart)
    service_requests_over_time = db.session.query(
        func.date(ServiceRequest.time_of_request).label('date'),
        func.count(ServiceRequest.id).label('count')
    ).filter_by(customer_id=customer.id).group_by('date').all()

    dates = [str(item.date) for item in service_requests_over_time]
    service_requests_counts = [item.count for item in service_requests_over_time]

    # Return the data as a JSON response
    return jsonify({
        'active_requests': active_requests_count,
        'reviews': reviews_count,
        'dates': dates,
        'service_requests_over_time': service_requests_counts
    })
