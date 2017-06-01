import os

from flask import Flask, current_app
from flask_cors import CORS
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flasgger import Swagger

from psycopg2 import IntegrityError
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

from config import config



#flask extension
#start the engine
engine = create_engine('postgres://user:postgres@localhost:5432/euclidone')
#engine = create_engine('oracle+cx_oracle://euclid:euclid@127.0.0.1/XE')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()

from hris.models import Role
from hris.models import (
    User, 
    CompanyDetail,
    Facility,
    EmployeeCategoryRank,
    EmployeeCategory,
    EmployeeType,
    Employee,
    EmployeeExtra,
    Qualification,
    Certification,
    Training,
    AgencyType,
    Agency,
    FacilityType,
    Region,
    Province,
    District,
    LLG
)
ROLES_PERMISSION = {}

def update_role_permission():
    global ROLES_PERMISSION
    ROLES_PERMISSION = {}
    roles = db_session.query(Role).all()
    roles = [role.to_dict() for role in roles]
    for role in roles:
        ROLES_PERMISSION[role['id']] = role
    return ROLES_PERMISSION

# #







def shutdown_session(exception=None):
    print('Session closed')
    db_session.remove()

#import models so that they are registered with SQLalchemy
from hris import models


def create_app(config_name=None, main=True):
    #update the role and permission table
    #update_role_permission()

    if config_name is None:
        config_name = os.environ.get('FLACK_CONFIG', 'development')
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    #regster the teardown context function
    app.teardown_appcontext(shutdown_session)
    #register the blueprints
    from hris.api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    #initialize flask extension
    #with app.app_context():
     #   roles = db_session.query(Role).all()
      #  roles = [role.to_dict() for role in roles]
       # for role in roles:
        #    current_app.config[role['id']]= role
            
        
    

    #register the errohandler
    
    CORS(app)
    Swagger(app)
    admin = Admin(app, name='HRIS Control Panel', template_mode='bootstrap2')
    admin.add_view(ModelView(AgencyType, db_session))
    admin.add_view(ModelView(Agency, db_session))
    admin.add_view(ModelView(FacilityType, db_session))
    admin.add_view(ModelView(Facility, db_session))
    admin.add_view(ModelView(CompanyDetail, db_session))
    admin.add_view(ModelView(User, db_session))
    admin.add_view(ModelView(Region, db_session))
    admin.add_view(ModelView(Province, db_session))
    admin.add_view(ModelView(District, db_session))
    admin.add_view(ModelView(LLG, db_session))
    #admin.add_view(ModelView(EmployeeCategory, db_session))
    
    return app


def init_db():
    from hris import models
    Base.metadata.create_all(engine)

