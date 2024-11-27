from flask import Flask, render_template, request, g
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from dotenv import load_dotenv
import logging
from sqlalchemy import func


db = SQLAlchemy()

def create_app(test_config=None):

    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('secret-key'),
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'database.db')}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,

        UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')  # dir to save upload files.
    )

    if test_config == None:
        app.config.from_pyfile('config.py', silent=True)

    else:
        app.config.from_mapping(test_config)


    try:
        os.makedirs(app.instance_path, exist_ok=True)
        os.makedirs(os.path.join(app.instance_path, 'uploads'), exist_ok=True)
    except OSError:
        pass


    # database instance initialization
    db.init_app(app)
    migrate = Migrate(app, db)


    with app.app_context():
        from .models import Admins, Service, ServiceRequest, Professional, Customer, Reviews
        db.create_all()

        if not Admins.query.filter_by(username='admin').first():
            admin = Admins(
                username='admin'
            )
            admin.set_password('admin')

            db.session.add(admin)
            db.session.commit()



    # registering routes
    from .routes import admin, professional, customer
    app.register_blueprint(admin.admin)
    app.register_blueprint(professional.prof)
    app.register_blueprint(customer.customer)

    # registering apis
    from .apis import api
    app.register_blueprint(api)


    @app.errorhandler(404)
    def error(e):
        return render_template('404.html')

    
    @app.route('/')
    def home():

        top_services = db.session.query(
        Service.id,
        Service.name,
        Service.description,
        Service.price,
        func.avg(Reviews.rating).label('avg_rating')
        ).join(Reviews, Reviews.service_req_id == Service.id)\
        .group_by(Service.id)\
        .order_by(func.avg(Reviews.rating).desc())\
        .limit(3).all()

        # Convert query results to a dictionary for easier handling in templates
        top_services = [
            {
                'id': service.id,
                'name': service.name,
                'description': service.description,
                'price': service.price,
                'avg_rating': service.avg_rating or 0
            }
            for service in top_services
        ]

        return render_template('home.html', top_services=top_services)
    
    return app