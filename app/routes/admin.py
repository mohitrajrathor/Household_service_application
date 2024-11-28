'''
admin.py

admin route file
'''

# imports
from flask import (Blueprint, render_template, request, session, flash, redirect, url_for, current_app, \
                   send_from_directory, abort)
from ..models import Admins, Service, Professional, Customer, ServiceRequest
from .. import db
from functools import wraps
import os
from ..utils import is_admin



# initializing blueprint
admin = Blueprint('admin', import_name=__name__, url_prefix='/admin')


# login route
@admin.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        next = request.args.get('next')

        username = request.form['username']
        password = request.form['password']

        admin = Admins.query.filter_by(username=username).first()

        if admin and admin.check_password(password):
            session['role'] = 'admin'
            session['id'] = admin.id

            flash('Login Successful!', 'success')

            return redirect(next if next else url_for('admin.dashboard'))

        else:
            flash("Incorrect credentials!", 'danger')
            return redirect(url_for('professional.login', next=next))
        
    if session.get('role') == 'admin':
        flash("Already logged in!", 'success')
        return redirect(url_for("admin.dashboard"))

    return render_template('admin/login.html')

@admin.route('/')
@admin.route("/dashboard")
@is_admin
def dashboard():
    search_service = request.args.get('search_service')
    search_prof = request.args.get('search_prof')
    search_cust = request.args.get('search_cust')
    search_req = request.args.get('search_req')

    user = Admins.query.get(session.get('id'))

    if search_service:
        services = Service.query.filter(Service.name.ilike(f'%{search_service}%'))
    else:
        services = Service.query.all()


    if search_prof:
        professionals = Professional.query.filter(Professional.name.ilike(f'%{search_prof}%'))
    else:
        professionals = Professional.query.all()


    if search_cust:
        customers = Customer.query.filter(Customer.name.ilike(f'%{search_cust}%'))
    else:
        customers = Customer.query.all()


    if search_req:
        requests = ServiceRequest.query.filter(ServiceRequest.title.ilike(f'%{search_req}%'))
    else:
        requests = ServiceRequest.query.all()


    params = {
        "user" : user,
        "services" : services,
        "professionals" : professionals,
        "customers" : customers,
        "requests" : requests
    }

    return render_template('admin/dashboard.html', **params)




@admin.route("/summary")
@is_admin
def summary():
    return render_template('admin/summary.html')


@admin.route("/logout")
@is_admin
def logout():
    session.pop('role')
    session.pop('id')

    return redirect(url_for('admin.login'))



# block professional
@admin.route('/block_prof/<int:prof_id>')
@is_admin
def block_prof(prof_id):
    next = request.args.get('next')
    user = Professional.query.get(prof_id)

    if not user:
        flash("Professional does not exist!", "warning")
        return redirect(next if next else url_for("admin.dashboard"))

    if user:
        user.is_active = False

        try:
            db.session.commit()
            flash(f"Professional {user.name} is blocked!", 'success')
            return redirect(next if next else url_for("admin.dashboard"))
        
        except Exception as e:
            db.session.rollback()
            flash(f"Some error occurred!", 'danger')
            return redirect(next if next else url_for("admin.dashboard"))


# unblock professional
@admin.route('/unblock_prof/<int:prof_id>')
@is_admin
def unblock_prof(prof_id):
    next = request.args.get('next')
    user = Professional.query.get(prof_id)

    if not user:
        flash("Professional does not exist!", "warning")
        return redirect(next if next else url_for("admin.dashboard"))

    if user:
        user.is_active = True

        try:
            db.session.commit()
            flash(f"Professional {user.name} is unblocked!", 'success')
            return redirect(next if next else url_for("admin.dashboard"))
        
        except Exception as e:
            db.session.rollback()
            flash(f"Some error occurred!", 'danger')
            return redirect(next if next else url_for("admin.dashboard"))
        


# verify professional
@admin.route('/verify_prof/<int:prof_id>')
@is_admin
def verify_prof(prof_id):
    next = request.args.get('next')
    user = Professional.query.get(prof_id)

    if not user:
        flash("Professional does not exist!", "warning")
        return redirect(next if next else url_for("admin.dashboard"))

    if user:
        user.verified = True

        try:
            db.session.commit()
            flash(f"Professional {user.name} is verified!", 'success')
            return redirect(next if next else url_for("admin.dashboard"))
        
        except Exception as e:
            db.session.rollback()
            flash(f"Some error occurred!", 'danger')
            return redirect(next if next else url_for("admin.dashboard"))
        


# block sustomer
@admin.route('/block_cust/<int:cust_id>')
@is_admin
def block_cust(cust_id):
    next = request.args.get('next')

    user = Customer.query.get(cust_id)

    if not user:
        flash("Customer does not exist!", "warning")
        return redirect(next if next else url_for("admin.dashboard"))

    if user:
        user.is_active = False

        try:
            db.session.commit()
            flash(f"Customer {user.name} is blocked!", 'success')
            return redirect(next if next else url_for("admin.dashboard"))
        
        except Exception as e:
            db.session.rollback()
            flash(f"Some error occurred!", 'danger')
            return redirect(next if next else url_for("admin.dashboard"))
        

# unblock sustomer
@admin.route('/unblock_cust/<int:cust_id>')
@is_admin
def unblock_cust(cust_id):
    next = request.args.get('next')

    user = Customer.query.get(cust_id)

    if not user:
        flash("Customer does not exist!", "warning")
        return redirect(next if next else url_for("admin.dashboard"))

    if user:
        user.is_active = True

        try:
            db.session.commit()
            flash(f"Customer {user.name} is unblocked!", 'success')
            return redirect(next if next else url_for("admin.dashboard"))
        
        except Exception as e:
            db.session.rollback()
            flash(f"Some error occurred!", 'danger')
            return redirect(next if next else url_for("admin.dashboard"))