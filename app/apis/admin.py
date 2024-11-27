'''
admin.py

file to handle code logic related to admin api
'''

# imports 
from flask import Blueprint, jsonify
from ..models import db, Professional, Customer, ServiceRequest, Reviews
from datetime import datetime
from sqlalchemy import func

admin_api = Blueprint('admin_api', __name__, url_prefix='/admin')

@admin_api.route('/summary_data', methods=['GET'])
def get_dashboard_data():
    active_professionals_count = Professional.query.filter_by(is_active=True).count()

    active_customers_count = Customer.query.filter_by(is_active=True).count()

    service_requests_count = ServiceRequest.query.count()

    reviews_count = Reviews.query.count()

    # Service Requests Over Time (for chart)
    # Example query to get service requests per day
    service_requests_over_time = db.session.query(
        func.date(ServiceRequest.time_of_request).label('date'),
        func.count(ServiceRequest.id).label('count')
    ).group_by('date').all()

    dates = [str(item.date) for item in service_requests_over_time]
    service_requests_counts = [item.count for item in service_requests_over_time]

    return jsonify({
        'active_professionals': active_professionals_count,
        'active_customers': active_customers_count,
        'service_requests': service_requests_count,
        'reviews': reviews_count,
        'dates': dates,
        'service_requests_over_time': service_requests_counts
    })
