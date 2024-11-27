'''
utils.py

module to store utility functions and classes
'''

# imports 
from functools import wraps
from flask import session, flash, redirect, request, url_for


# decorator to check whether logged in as admin or not
def is_admin(f):
    '''
    decorator to check whether logged in as admin or not
    '''
    @wraps(f)
    def check_admin(*args, **kwargs):
        if session.get('role') != 'admin':
            flash("You must be logged in  as an admin to access this page.", "danger")
            return redirect(url_for('admin.login', next=request.url))
        
        return f(*args, **kwargs)
    
    return check_admin


# decorator to check whether logged in as professional or not
def is_prof(f):
    '''
    decorator to check whether logged in as professional or not
    '''
    @wraps(f)
    def check_prof(*args, **kwargs):
        if session.get('role') != 'professional':
            flash("You must be logged in  as an professional to access this page.", "danger")
            return redirect(url_for('professional.login', next=request.url))
        
        return f(*args, **kwargs)
    
    return check_prof


# decorator to check whether logged in as customer or not
def is_customer(f):
    '''
    Decorator function to check whether user logged in as customer or not.
    '''
    @wraps(f)
    def check_customer(*args, **kwargs):
        if session.get('role') != 'customer':
            flash("You must be logged in as customer to access this page!", "warning")
            return redirect(url_for("customer.login", next=request.url))
        
        return f(*args, **kwargs)
    
    return check_customer