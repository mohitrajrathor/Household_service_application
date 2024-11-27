# apis/professional.py

from flask import Blueprint, jsonify, session
from ..models import db, ServiceRequest, Reviews, Professional
from datetime import datetime
from sqlalchemy import func

professional_api = Blueprint('professional_api', __name__, url_prefix="/professional")

@professional_api.route('/summary_data', methods=['GET'])
def get_dashboard_data():
    professional_id = session.get('id')
    professional = Professional.query.get(professional_id)

    # Active Service Requests for the professional
    active_requests_count = ServiceRequest.query.filter_by(professional_id=professional.id, service_status='requested').count()

    # Completed Services for the professional
    completed_services_count = ServiceRequest.query.filter_by(professional_id=professional.id, service_status='completed').count()

    # Reviews for the professional
    reviews_count = Reviews.query.filter_by(prof_id=professional.id).count()

    # Completed Services Over Time (for chart)
    completed_services_over_time = db.session.query(
        func.date(ServiceRequest.date_of_completion).label('date'),
        func.count(ServiceRequest.id).label('count')
    ).filter_by(professional_id=professional.id, service_status='completed').group_by('date').all()

    dates = [str(item.date) for item in completed_services_over_time]
    completed_services_counts = [item.count for item in completed_services_over_time]

    # Return the data as a JSON response
    return jsonify({
        'active_requests': active_requests_count,
        'completed_services': completed_services_count,
        'reviews': reviews_count,
        'dates': dates,
        'completed_services_over_time': completed_services_counts
    })
