'''
customer.py 

file to handle customer role related routes and functionalities.
'''

# imports 
from flask import Blueprint, render_template, request, flash, url_for, redirect, session
from ..models import Customer, Service, Professional, ServiceRequest, Reviews
from .. import db
from sqlalchemy.exc import IntegrityError
import logging
from functools import wraps
from ..utils import is_customer
from sqlalchemy import text
import datetime


# SECTION: Instance
customer = Blueprint("customer", __name__, url_prefix="/customer")
        

# SECTION: Routes
# register route
@customer.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        print(request.form)

        data = request.form
        name = data['name']
        email = data['email']
        password = data['password']
        phone = data['phone']
        str_addr = data['street_address']
        city = data['city']
        state = data['state']
        zipcode = data['zip']

        if Customer.query.filter_by(email=email).first():
            flash("Email used already, change email or Login!", "warning")
            return redirect(url_for("customer.register"))
        
        if len(zipcode) != 6:
            flash("Zip code must have 6 digits!", "warning")
            return redirect(url_for("customer.register"))


        cust = Customer(
            name=name,
            email=email,
            phone_number=phone,
            street_address=str_addr,
            city=city,
            state=state,
            zipcode=zipcode
        )

        cust.set_password(password)

        try:
            db.session.add(cust)
            db.session.commit()

            session['role'] = 'customer'
            session['id'] = cust.id

            flash("Registered Successfully!", 'success')
            return redirect(url_for("customer.dashboard"))
        
        except IntegrityError as i:
            flash('Input must be correct, check Details again!', 'warning')
            logging.error(f"IntegrityError: {i}")
            db.session.rollback()
            return redirect(url_for("customer.register"))

        except Exception as e:
            logging.error(e)
            db.session.rollback()

            flash("Something unusual happened!", 'danger')
            return redirect(url_for("customer.register"))


    return render_template('customer/register.html')


@customer.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        next = request.args.get('next') 
        print(request.form)

        data = request.form
        email = data['email']
        password = data['password']

        user = Customer.query.filter_by(email=email).first()

        if not user:
            flash('Email not found!', 'warning')
            return redirect(url_for('customer.login'))

        if user.check_password(password):
            session['role'] = 'customer'
            session['id'] = user.id

            flash('Logged in successfully!', 'success')
            return redirect(next if next else url_for("customer.dashboard"))
        
        flash("Incorrect credentials!", 'danger')
        return redirect(url_for('professional.login', next=next))


    return render_template('customer/login.html')


@customer.route('/')
@customer.route('/dashboard', methods=['GET', 'POST'])
@is_customer
def dashboard():
    print(request.args)
    service_id = request.args.get('service_id')
    search_service = request.args.get('search_service')
    search_professional = request.args.get('search_prof')
    search_req = request.args.get('search_req')

    user = Customer.query.get(session.get('id'))

    if service_id:
        professionals = Professional.query.filter_by(service_type_id=int(service_id))
    else:
        professionals = Professional.query.all()

    if search_service:
        services = Service.query.filter(Service.name.ilike(f'%{search_service}%')).all()
    else:
        services = Service.query.all()
    
    if search_professional:
        professionals = Professional.query.filter(Professional.name.ilike(f'%{search_professional}%')).all()

    if search_req:
        requests = ServiceRequest.query.filter_by(customer_id=user.id).filter(ServiceRequest.title.ilike(f'%{search_req}%')).all()
    else:
        requests = ServiceRequest.query.filter_by(customer_id=user.id).all()

    params = {
        'user' : user,
        'services' : services,
        'professionals' : professionals,
        'requests' : requests
    }

    return render_template("customer/dashboard.html", **params)



@customer.route('/summary')
@is_customer
def summary():
    return render_template("customer/summary.html")



@customer.route('/update_profile', methods=['POST'])
@is_customer
def update_profile():
    data = request.form
    user = Customer.query.get(int(session['id']))

    user.name = data.get('name')
    user.phone_number = data.get('phone')
    user.zipcode = data.get('zip')
    user.street_address = data.get('street_address')
    user.city = data.get('city')
    user.state = data.get('state')


    try:
        db.session.commit()
        flash("Profile updated successfully!", 'success')
        return redirect(url_for('customer.dashboard'))
    except Exception as e:
        db.session.rollback()
        flash("Some error occurred!", 'danger')
        return redirect(url_for('customer.dashboard'))


@customer.route('/logout')
@is_customer
def logout():
    session.pop('role')
    session.pop('id')

    return redirect(url_for("customer.login"))



@customer.route('/request-service/<int:prof_id>', methods=['POST'])
@is_customer
def req_service(prof_id):
    print(request.form)

    data = request.form

    user = Customer.query.get(session['id'])
    prof = Professional.query.get(prof_id)

    deadline = datetime.datetime.strptime(data.get('deadline'), '%Y-%m-%d')
    deadline = deadline.replace(tzinfo=datetime.timezone.utc)

    sr = ServiceRequest(
        customer_id = user.id,
        professional_id = prof.id,
        service_id = prof.service_type_id,
        title = data.get('title'),
        date_of_completion = deadline,
        remarks = data.get('remarks'),
        location_pin_code = data.get('zipcode')
    )

    try:
        db.session.add(sr)
        db.session.commit()
        flash('Service Requested Successfully!', 'success')
        return redirect(url_for('customer.dashboard'))
    except Exception as e:
        db.session.rollback()
        flash('Error Occurred!', 'danger')
        return redirect(url_for('customer.dashboard'))
    


@customer.route('/close-req/<int:req_id>')
@is_customer
def close_req(req_id):

    req = ServiceRequest.query.get(req_id)

    req.service_status = 'paid'

    try: 
        db.session.commit()
        flash('Service Payment Done successfully!', 'success')
        return redirect(url_for('customer.dashboard'))
    
    except Exception as e:
        db.session.rollback()
        flash('Error occurred!', 'danger')
        return redirect(url_for('customer.dashboard'))
    

    
@customer.route('/cancel-req/<int:req_id>')
@is_customer
def cancel_req(req_id):

    req = ServiceRequest.query.get(req_id)

    req.service_status = 'cancelled'

    try: 
        db.session.commit()
        flash('Service cancelled successfully!', 'success')
        return redirect(url_for('customer.dashboard'))
    
    except Exception as e:
        db.session.rollback()
        flash('Error occurred!', 'danger')
        return redirect(url_for('customer.dashboard'))
    

@customer.route('/update-req/<int:req_id>', methods=['POST'])
@is_customer
def update_req(req_id):
    data = request.form
    print(data)

    req = ServiceRequest.query.get(req_id)

    req.title = data.get('title')
    req.location_pin_code = data.get('zipcode')
    
    deadline = datetime.datetime.strptime(data.get('deadline'), "%Y-%m-%d")
    deadline = deadline.replace(tzinfo=datetime.timezone.utc)

    req.date_of_completion = deadline

    try:
        db.session.commit()
        flash("Service updated successfully!", 'success')
        return redirect(url_for('customer.dashboard'))
    except Exception as e:
        db.session.rollback()
        flash("Error Occurred", 'danger')
        return redirect(url_for('customer.dashboard'))


@customer.route('/review-req/<int:req_id>', methods=['POST'])
@is_customer
def review_req(req_id):
    data = request.form

    req = ServiceRequest.query.get(req_id)

    review = Reviews(
        prof_id=req.professional.id,
        cust_id=req.customer.id,
        service_req_id=req.id,
        rating=data.get('rating'),
        review=data.get('review')
    )

    try:
        db.session.add(review)
        db.session.commit()
        flash('Thanks for reivew!', 'success')
        return redirect(url_for('customer.dashboard'))

    except Exception as e:
        db.session.rollback()
        flash('Error Occurred', 'danger')
        return redirect(url_for('customer.dashboard'))

    


@customer.route('/payment')
@is_customer
def payment():
    req_id = request.args.get('req_id')

    req = ServiceRequest.query.get(req_id)

    return render_template('customer/payment.html', req=req)
