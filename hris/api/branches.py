from hris.utils import hash_password, gen_access_token, decode_access_token
from flask import request, abort, jsonify, g
from functools import wraps

from hris.api import api
from sqlalchemy.exc import IntegrityError #foreign key violation #this won't come up oftern
from sqlalchemy.orm.exc import NoResultFound
from hris import db_session, ROLES_PERMISSION, engine
import copy

#auth

###
#auth
from hris.utils import (
    handle_keys_for_update_request,
    handle_keys_for_post_request
)

from hris.api.auth import (
    allow_permission, 
    create_update_permission,
    read_permission
)
###
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
    FacilityType
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
    unauthorized_envelop,
    extra_keys_envelop, 
    keys_require_envelop
)









    

def handle_update_division_keys(model, exclude=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not request.json:
                abort(400)
            
            db_fields = set(col.name for col in model.__mapper__.columns)
            required_fields = db_fields - set(exclude) if exclude is not None else set()

            result = set(request.json.keys()) - required_fields
            if result:
                return extra_keys_envelop('Keys not accepted : {!r}'.format(',  '.join(key for key in result)))
            
            #now check if there are empty fieldsc

            #if not all(len(str(val).strip()) >=1 for val in request.json.values()):
             #   return length_require_envelop()

            #if everythin is fine then return the function
            return func(*args, **kwargs)
        return wrapper
    return decorator



@api.route('/agencytypes', methods=['POST'])
@create_update_permission('division_management_perm')
def create_agencytypes():
    if not request.json:
        abort(400)
    #check for the empty fields
    if not all(len(val.strip()) >= 1 for val in request.json.values()):
        return length_require_envelop()
    #now check if there is any extra keys
    from_db =  set(request.json.keys()) - {'name', 'code', 'del_flag'} 
    if from_db:
        return extra_keys_envelop('Extra keys : %s' % ', '.join(from_db))
    
    required_keys = {'name',  'code'} - set(request.json.keys())
    if required_keys:
        return keys_require_envelop('Keys required : %s' % ', '.join(required_keys))
    
    #if everythin is fine
    if 'name' in request.json:
        request.json['display_name'] = request.json['name'].strip()
        request.json['name'] = request.json['name'].lower().strip()
    
    if 'code' in request.json:
        request.json['code'] = request.json['code'].strip()
    
    try:
        db_session.add(AgencyType(**request.json))
        db_session.commit()
    except IntegrityError:
        return record_exists_envelop()
    except Exception:
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)

    
@api.route('/agencytypes', methods=['GET'])
def get_agencytypes():
    try:
        ats = db_session.query(AgencyType).all()
    except NoResultFound:
        return record_notfound_envelop()
    else:
        return records_json_envelop(list(a.to_dict() for a in ats))

@api.route('/agencytypes/<int:id>', methods=['PUT'])
@create_update_permission('division_management_perm')
def update_agencytype(id):
    if not request.json:
        abort(400)
    #check to see if ther eis empty field
    if not all(len(val.strip()) >= 1 for val in request.json.values()):
        return length_require_envelop()

    if 'name' in request.json:
        request.json['display_name'] = request.json['name'].strip()
        request.json['name'] = request.json['name'].lower().strip()
    
    if 'code' in request.json:
        request.json['code'] = request.json['code'].strip()
    
    try:
        db_session.query(AgencyType).filter(AgencyType.id == id).update(request.json)
        db_session.commit()
    except IntegrityError:
        return record_exists_envelop()
    except Exception:
        return fatal_error_envelop()
    else:
        return record_updated_envelop(request.json)


@api.route('/agencies', methods=['POST'])
@create_update_permission('division_management_perm')
def create_agency():
    if not request.json:
        abort(400)
    #check to see if there is empty fields
    if not all(len(val.strip()) >= 1 for val in request.json.values()):
        return length_require_envelop()
    
    if 'name' in request.json:
        request.json['display_name'] = request.json['name'].strip()
        request.json['name'] = request.json['name'].lower().strip()
    
    try:
        db_session.add(Agency(**request.json))
        db_session.commit()
    except IntegrityError:
        return record_exists_envelop()
    except Exception:
        return fatal_envelop_envelop()
    else:
        return record_created_envelop(request.json)

@api.route('/agencies', methods=['GET'])
def get_agencies():
    try:
        agencies = db_session.query(Agency).all()
    except NoResultFound:
        return record_notfound_envelop()
    except Exception:
        raise
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(a.to_dict() for a in agencies))


@api.route('/agencies/<int:id>', methods=['PUT'])
@create_update_permission('division_management_perm')
def update_agency(id):
    if not request.json:
        abort(400)
    
    if not all(len(val.strip()) >= 1 for val in request.json.values()):
        return length_require_envelop()
    
    if 'name' in request.json:
        request.json['display_name'] = request.json['name'].strip()
        request.json['name'] = request.json['name'].lower().strip()
    
    if 'code' in request.json:
        request.json['code'] = request.json['code'].strip()
    
    try:
        db_session.query(Agency).filter(Agency.id == id).update(request.json)
        db_session.commit()
    except IntegrityError:
        return record_exists_envelop()
    except Exception:
        return fatal_error_envelop()
    else:
        return record_updated_envelop(request.json)


@api.route('/agencies/<int:id>', methods=['GET'])
@read_permission('read_management_perm')
def get_agency(id):
    try:
        agency = db_session.query(Agency).filter(Agency.id == id).one()
    except NoResultFound:
        return record_notfound_envelop()
    except Exception:
        return fatal_envelop_error()
    else:
        return record_json_envelop(agency.to_dict())

    
@api.route('/facilities', methods=['POST'])
@create_update_permission('division_management_perm')
def create_facilities():
    if not request.json:
        abort(400)
    #check to see if the incoming values are not null
    if not all(len(val.strip()) >= 1 for val in request.json.values() if isinstance(val, str)):
        return length_require_envelop()
    
    if 'facility_name' not in request.json:
        return keys_require_envelop(message="'facility_name' key is missing.")
    
    try:
        db_session.add(Facility(**request.json))
        db_session.commit()
    except IntegrityError:
        return record_exists_envelop()
    except Exception:
        raise
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)





@api.route('/facilities', methods=['GET'])
@read_permission('read_management_perm')
def get_facilities():
    try:
        facilities = db_session.query(Facility).all()
    except NoResultFound:
        return record_notfound_envelop()
    except Exception:
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(f.to_dict() for f in facilities))

@api.route('/facilities/<int:id>', methods=['PUT'])
@create_update_permission('division_management_perm')
def update_facility(id):
    if not request.json:
        abort(400)
    if not all(len(val.strip()) >= 1 for val in request.json.values()):
        return length_require_envelop()
    if 'facility_name' in request.json:
        request.json['facility_display_name'] = request.json['facility_name'].strip()
        request.json['facility_name'] = request.json['facility_name'].lower().strip()
    
    try:
        db_session.query(Facility).filter(Facility.id == id).update(request.json)
        db_session.commit()
    except IntegrityError:
        return record_exists_envelop()
    except Exception:
        raise
        return fatal_error_envelop()
    else:
        return record_updated_envelop(request.json)


@api.route('/facilitytypes', methods=['POST'])
@create_update_permission('division_management_perm')
def create_facility_type():
    if not request.json:
        abort(400)
    if not all(len(val.strip()) >= 1 for val in request.json.values()):
        return length_require_envelop()
    
    if 'name' in request.json:
        request.json['display_name'] = request.json['name'].strip()
        request.json['name'] = request.json['name'].strip().lower()
    
    try:
        db_session.add(FacilityType(**request.json))
        db_session.commit()
    except IntegrityError:
        return record_exists_envelop()
    except Exception:
        raise
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)


@api.route('/facilitytypes/<int:id>', methods=['PUT'])
@create_update_permission('company_management_perm')
def update_facility_type(id):
    if not request.json:
        abort(400)
    
    
    
    #now try to update the facilty name
    if 'name' in request.json:
        request.json['display_name'] = request.json['name']
        request.json['name'] = request.json['name'].lower().strip()

    try:
        facility = db_session.query(FacilityType).filter(FacilityType.id==id).update(request.json)
        
        db_session.commit()
    except NoResultFound as e:
        abort(404)
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
         
        abort(500)
    else:
        return record_updated_envelop(request.json)


@api.route('/facilitytypes', methods=['GET'])
def get_facilitytypes():
    try:
        fts = db_session.query(FacilityType).all()
    except NoResultFound:
        return record_notfound_envelop()
    else:
        return records_json_envelop(list(ft.to_dict() for ft in fts))

@api.route('/facilitytypes/<int:id>', methods=['GET'])
def get_facilitytype(id):
    try:
        ft = db_session.query(FacilityType).filter(FacilityType.id == id).one()
    except NoResultFound:
        return record_notfound_envelop()
    else:
        return record_json_envelop(ft.to_dict())


@api.route('/facilitytypes/<int:f_id>/facilities', methods=['POST'])
@create_update_permission('division_management_perm')
def create_facilities_by_facility_type(f_id):
    if not request.json

@api.route('/branches/<int:b_id>/employees')
@read_permission('read_management_perm')
def get_employees_by_branch(b_id):
    try:
        employees = db_session.query(Employee).filter(Employee.employee_branch_id==b_id).filter(Employee.is_branch==True).all()
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(emp.to_dict() for emp in employees))



@api.route('/agencies/<int:a_id>/employees')
@read_permission('read_management_perm')
def get_employees_by_agency(a_id):
    try:
        employees = db_session.query(Employee).filter(Employee.employee_branch_id==a_id).filter(Employee.is_branch==False).all()
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(emp.to_dict() for emp in employees))


