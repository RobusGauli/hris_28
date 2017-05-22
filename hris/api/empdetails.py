from hris.utils import hash_password, gen_access_token, decode_access_token
from flask import request, abort, jsonify, g
from functools import wraps

from hris.api import api
from sqlalchemy.exc import IntegrityError #foreign key violation #this won't come up oftern
from sqlalchemy.orm.exc import NoResultFound
from hris import db_session

import itertools
#auth

###
from hris.models import (
    User, 
    CompanyDetail,
    Branch,
    EmployeeCategoryRank,
    EmployeeCategory,
    EmployeeType,
    Employee,
    EmployeeExtra,
    Qualification,
    Certification,
    Training,
    EmployeePosition,
    EmployeeRelativeType,
    EmployeeRelative,
    EmployementHistory,
    EmployeeReference,
    EmployeeBenifitType,
    EmployeeBenifit,
    EmployeeDisciplinaryType,
    EmployeeDisciplinary,
    EmployeeAppraisalType,
    EmployeeAppraisal


)


from hris.api.response_envelop import (
    records_json_envelop,
    record_exists_envelop,
    record_json_envelop,
    record_created_envelop,
    record_notfound_envelop,
    record_updated_envelop,
    record_not_updated_env,
    fatal_error_envelop,
    missing_keys_envelop, 
    length_require_envelop,
    extra_keys_envelop
)
from hris.api.auth import (
    allow_permission, 
    create_update_permission,
    read_permission
)



@api.route('/empreltypes', methods=['POST'])
@create_update_permission('agency_emp_perm')
def create_emp_relativetype():
 
    #lower case the facility name
    if not request.json:
        abort(400)
    if 'name' not in request.json:
        return missing_keys_envelop()
    #check if ther is empty fields
    if not all(len(val.strip())>=1 for key, val in request.json.items()):
        return length_require_envelop()

    request.json['display_name'] = request.json['name']
    request.json['name'] = request.json['name'].strip().lower()
    #insert into the database
    try:
        rel = EmployeeRelativeType(**request.json)
        db_session.add(rel)
        db_session.commit()
    except IntegrityError as ie:
        return record_exists_envelop()
    
    else:
        return record_created_envelop(request.json)

@api.route('/empreltypes')
def get_emp_relativetypes():
    try:
        q = db_session.query(EmployeeRelativeType).all()
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        
        return records_json_envelop(list(row.to_dict() for row in q))

@api.route('/empreltypes/<int:id>', methods=['PUT'])
@create_update_permission('agency_emp_perm')
def update_emp_relativetype(id):
    if not request.json:
        abort(400)
    #check to see if there is any empty values
    if not all(len(str(val).strip()) >=1 for val in request.json.values() if isinstance(val, str)):
        abort(411)
    #check to see if the request has the right type of keys
    
    #clearn up the values for string
    #generator expression
    cleaned_json = dict((key, val.strip()) if isinstance(val, str) else (key, val) for key, val in request.json.items())
    if 'name' in cleaned_json:
        cleaned_json['display_name'] = cleaned_json['name']
        cleaned_json['name'] = cleaned_json['name'].strip().lower()     
    

    #try to executre
  
    try:
        db_session.query(EmployeeRelativeType).filter(EmployeeRelativeType.id == id).update(cleaned_json)
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_updated_envelop(request.json)


@api.route('/empbentypes', methods=['POST'])
@create_update_permission('agency_emp_perm')
def create_emp_benifittype():
 
    #lower case the facility name
    if not request.json:
        abort(400)
    if 'name' not in request.json:
        return missing_keys_envelop()
    #check if ther is empty fields
    if not all(len(val.strip())>=1 for key, val in request.json.items()):
        return length_require_envelop()

    request.json['display_name'] = request.json['name']
    request.json['name'] = request.json['name'].strip().lower()
    #insert into the database
    try:
        rel = EmployeeBenifitType(**request.json)
        db_session.add(rel)
        db_session.commit()
    except IntegrityError as ie:
        return record_exists_envelop()
    
    else:
        return record_created_envelop(request.json)

@api.route('/empbentypes')
def get_emp_bentypes():
    try:
        q = db_session.query(EmployeeBenifitType).all()
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        
        return records_json_envelop(list(row.to_dict() for row in q))


@api.route('/empbentypes/<int:id>', methods=['PUT'])
@create_update_permission('agency_emp_perm')
def update_emp_bentype(id):
    if not request.json:
        abort(400)
    #check to see if there is any empty values
    if not all(len(str(val).strip()) >=1 for val in request.json.values() if isinstance(val, str)):
        abort(411)
    #check to see if the request has the right type of keys
    
    #clearn up the values for string
    #generator expression
    cleaned_json = dict((key, val.strip()) if isinstance(val, str) else (key, val) for key, val in request.json.items())
    if 'name' in cleaned_json:
        cleaned_json['display_name'] = cleaned_json['name']
        cleaned_json['name'] = cleaned_json['name'].strip().lower()     
    

    #try to executre
  
    try:
        db_session.query(EmployeeBenifitType).filter(EmployeeBenifitType.id == id).update(cleaned_json)
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_updated_envelop(request.json)


@api.route('/empdistypes', methods=['POST'])
@create_update_permission('agency_emp_perm')
def create_emp_distype():
 
    #lower case the facility name
    if not request.json:
        abort(400)
    if 'name' not in request.json:
        return missing_keys_envelop()
    #check if ther is empty fields
    if not all(len(val.strip())>=1 for key, val in request.json.items()):
        return length_require_envelop()

    request.json['display_name'] = request.json['name']
    request.json['name'] = request.json['name'].strip().lower()
    #insert into the database
    try:
        rel = EmployeeDisciplinaryType(**request.json)
        db_session.add(rel)
        db_session.commit()
    except IntegrityError as ie:
        return record_exists_envelop()
    
    else:
        return record_created_envelop(request.json)

@api.route('/empdistypes')
def get_emp_distypes():
    try:
        q = db_session.query(EmployeeDisciplinaryType).all()
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        
        return records_json_envelop(list(row.to_dict() for row in q))


@api.route('/empdistypes/<int:id>', methods=['PUT'])
@create_update_permission('agency_emp_perm')
def update_emp_distype(id):
    if not request.json:
        abort(400)
    #check to see if there is any empty values
    if not all(len(str(val).strip()) >=1 for val in request.json.values() if isinstance(val, str)):
        abort(411)
    #check to see if the request has the right type of keys
    
    #clearn up the values for string
    #generator expression
    cleaned_json = dict((key, val.strip()) if isinstance(val, str) else (key, val) for key, val in request.json.items())
    if 'name' in cleaned_json:
        cleaned_json['display_name'] = cleaned_json['name']
        cleaned_json['name'] = cleaned_json['name'].strip().lower()     
    

    #try to executre
  
    try:
        db_session.query(EmployeeDisciplinaryType).filter(EmployeeDisciplinaryType.id == id).update(cleaned_json)
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_updated_envelop(request.json)

@api.route('/empapptypes', methods=['POST'])
@create_update_permission('agency_emp_perm')
def create_emp_apptype():
 
    #lower case the facility name
    if not request.json:
        abort(400)
    if 'name' not in request.json:
        return missing_keys_envelop()
    #check if ther is empty fields
    if not all(len(val.strip())>=1 for key, val in request.json.items()):
        return length_require_envelop()

    request.json['display_name'] = request.json['name']
    request.json['name'] = request.json['name'].strip().lower()
    #insert into the database
    try:
        rel = EmployeeAppraisalType(**request.json)
        db_session.add(rel)
        db_session.commit()
    except IntegrityError as ie:
        return record_exists_envelop()
    
    else:
        return record_created_envelop(request.json)

@api.route('/empapptypes')
def get_emp_apptypes():
    try:
        q = db_session.query(EmployeeAppraisalType).all()
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        
        return records_json_envelop(list(row.to_dict() for row in q))


@api.route('/empapptypes/<int:id>', methods=['PUT'])
@create_update_permission('agency_emp_perm')
def update_emp_apptype(id):
    if not request.json:
        abort(400)
    #check to see if there is any empty values
    if not all(len(str(val).strip()) >=1 for val in request.json.values() if isinstance(val, str)):
        abort(411)
    #check to see if the request has the right type of keys
    
    #clearn up the values for string
    #generator expression
    cleaned_json = dict((key, val.strip()) if isinstance(val, str) else (key, val) for key, val in request.json.items())
    if 'name' in cleaned_json:
        cleaned_json['display_name'] = cleaned_json['name']
        cleaned_json['name'] = cleaned_json['name'].strip().lower()     
    

    #try to executre
  
    try:
        db_session.query(EmployeeAppraisalType).filter(EmployeeAppraisalType.id == id).update(cleaned_json)
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_updated_envelop(request.json)