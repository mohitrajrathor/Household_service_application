'''
general_api.py


file to handle general api
'''

# imports 
from flask import Blueprint, current_app, send_from_directory, abort
from ..models import Professional
import os


gen_api = Blueprint('gen_api', __name__, url_prefix='/')


# view view-doc
@gen_api.route('/view-doc/<int:prof_id>')
def view_doc(prof_id):
    user = Professional.query.get(int(prof_id))
    if user:
        try:
            filename = user.doc_path
            dir_path = os.path.join(current_app.instance_path, 'uploads')
            return send_from_directory(dir_path, filename)
        except:
            abort(404)