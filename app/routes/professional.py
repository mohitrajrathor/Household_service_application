'''
professional.py

file to handle professional role related route logic.
'''

# imports 
from flask import Blueprint, render_template, request, redirect, flash, url_for, session, current_app
from ..models import Service, Professional, ServiceRequest, Reviews
from .. import db
from sqlalchemy.exc import IntegrityError
import logging
from functools import wraps
import os
import uuid
from ..utils import is_prof
from sqlalchemy import func


# SECTION: instances

# professional blueprint instance
prof = Blueprint('professional', __name__, url_prefix='/professional')

# SECTION: routes logic
# register logic
@prof.route('/register', methods=['GET', 'POST'])
def register():
    '''
    route function to render register page for professional and register user using post method.

    return:
        render register page || register user using post method.
    '''
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        service_id = request.form['service_id']
        exp = request.form['experience']
        desc = request.form['description']


        # check if email exist already
        if Professional.query.filter_by(email=email).first():
            flash("Email already exist!", "danger")
            return redirect(url_for("professional.register"))

        # file handle
        file = request.files['verify-doc']

        if file.filename == '':
            print("no file selected!")
            flash('Valid file is required', 'warning')
            return redirect(url_for('professional.register'))

        if file.filename.lower().endswith('.pdf'):
            filename = uuid.uuid4().hex + '.pdf'
          
        file.save(os.path.join(current_app.instance_path, "uploads", filename))

        prof = Professional(
            name=name, 
            email=email,
            phone_number=int(phone),
            service_type_id=int(service_id),
            experience=int(exp),
            description=desc,
            doc_path=filename
        )

        prof.set_password(password)


        try:
            db.session.add(prof)
            db.session.commit()

            session['id'] = prof.id
            session['role'] = 'professional'

            return redirect(url_for("professional.dashboard"))
        except IntegrityError as i:
            flash('Input must be correct, check Details again!', 'warning')
            logging.error(f"IntegrityError: {i}")
            db.session.rollback()

            return redirect(url_for('professional.register'))
        
        except Exception as e:
            logging.error(e)
            db.session.rollback()

            flash("Something unusual happened!", 'danger')
            return redirect(url_for("professional.register"))
 

    if 'role' in session and session['role'] == 'professional':
        flash('Already Logged in !', 'success')
        return redirect(url_for('professional.dashboard'))

    params = {
        'services' : Service.query.all()
    }

    return render_template('professional/register.html', **params)


@prof.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        next = request.args.get('next')

        data = request.form
        user_email = data['email']
        password = data['password']

        # fetching user details
        user = Professional.query.filter_by(email=user_email).first()

        if not user:
            flash('Email is wrong!', 'warning')
            return redirect(url_for('professional.login'))

        if user.check_password(password):
            session['role'] = 'professional'
            session['id'] = user.id

            flash("Logged in successfully", "success")

            return redirect(next if next else url_for('professional.dashboard'))
        
        flash("Incorrect credentials!", 'danger')
        return redirect(url_for('professional.login', next=next))
        

    # check is user is already logged in 
    if 'role' in session and session['role'] == 'professional':
        flash('Already Logged in !', 'success')
        return redirect(url_for('professional.dashboard'))

    return render_template('professional/login.html')



# update proflie
@prof.route('/update-profile', methods=['POST'])
@is_prof
def update_profile():
    data = request.form
    user = Professional.query.get(int(session['id']))

    user.name = data.get('name')
    user.phone_number = data.get('phone')
    user.service_id = data.get('service_id')
    user.experience = data.get('experience')
    user.description = data.get('description')

    try:
        db.session.commit()
        flash("Profile updated successfully!", 'success')
        return redirect(url_for('professional.dashboard'))
    except Exception as e:
        db.session.rollback()
        flash("Some error occurred!", 'danger')
        return redirect(url_for('professional.dashboard'))




# dashboard route
@prof.route('/')
@prof.route('/dashboard')
@is_prof
def dashboard():
    
    user = Professional.query.get(int(session['id']))
    services = Service.query.all()
    service_requests = user.service_requests
    search_req = request.args.get('search_req')

    avg_rating = db.session.query(func.avg(Reviews.rating))\
        .filter(Reviews.prof_id == user.id)\
        .scalar()
    
    if avg_rating:
        avg_rating = round(avg_rating, 2)

    if search_req:
        service_requests = ServiceRequest.query.filter_by(professional_id=user.id).filter(ServiceRequest.title.ilike(f'%{search_req}%')).all()

    reviews = Reviews.query.filter_by(prof_id=user.id).all()

    params = {
        'user' : user,
        'services' : services,
        'requests' : service_requests,
        'avg_rat' : avg_rating,
        'reviews' : reviews
    }

    return render_template('professional/dashboard.html', **params)



# summary
@prof.route('/summary', methods=['POST', 'GET'])
@is_prof
def summary():
    return render_template('professional/summary.html')




@prof.route('/logout')
@is_prof
def logout():
    session.pop('role')
    session.pop('id')

    return redirect(url_for('professional.login'))


@prof.route('/accept-req/<int:req_id>')
@is_prof
def accept_req(req_id):

    req = ServiceRequest.query.get(req_id)

    req.service_status = 'in_progress'

    try: 
        db.session.commit()
        flash('Service accepted successfully!', 'success')
        return redirect(url_for('professional.dashboard'))
    
    except Exception as e:
        db.session.rollback()
        flash('Error occurred!', 'danger')
        return redirect(url_for('professional.dashboard'))
    

@prof.route('/reject-req/<int:req_id>')
@is_prof
def reject_req(req_id):

    req = ServiceRequest.query.get(req_id)

    req.service_status = 'rejected'

    try: 
        db.session.commit()
        flash('Service rejected successfully!', 'success')
        return redirect(url_for('professional.dashboard'))
    
    except Exception as e:
        db.session.rollback()
        flash('Error occurred!', 'danger')
        return redirect(url_for('professional.dashboard'))
    

@prof.route('/complete-req/<int:req_id>')
@is_prof
def complete_req(req_id):

    req = ServiceRequest.query.get(req_id)

    req.service_status = 'completed'

    try: 
        db.session.commit()
        flash('Service completed successfully!', 'success')
        return redirect(url_for('professional.dashboard'))
    
    except Exception as e:
        db.session.rollback()
        flash('Error occurred!', 'danger')
        return redirect(url_for('professional.dashboard'))