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
    FacilityType,
    DivisionTypeSetup,
    Division,
    FacilityDivision,
    DivisionPosition
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


@api.route('/divisionpositions', methods=['POST'])
def create_division_position():
    '''This will create a new position for each individual division inside the facilitiy'''

    if not request.json:
        abort(400)
    
    if not all(len(val.strip()) >=1 for val in request.json.values() if 
                                            isinstance(val, unicode)):
        return length_require_envelop()
    #now make the request
    try:
        db_session.add(DivisionPosition(**request.json))
        db_session.commit()
    except IntegrityError:
        return records_exists_envelop()
    except Exception:
        raise
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)
    

@api.route('/divisionpositions', methods=['GET'])
def get_division_positions():
    try:
        dvs = db_session.query(DivisionPosition).all()
    except NoResultFound:
        return record_notfound_envelop()
    except Exception:
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(dv.to_dict() for dv in dvs))

@api.route('/divisionpositions/<int:id>', methods=['PUT'])
def update_division_position(id):
    if not request.json:
        abort(400)
    
    if not all(len(val.strip()) >= 1 for val in request.json.values()
                                                if isinstance(val, unicode)):
        return length_require_envelop()
    
    try:
        db_session.query(DivisionPosition).filter(DivisionPosition.id == id).update(request.json)
        db_session.commit()
    except IntegrityError:
        return record_exists_envelop()
    except Exception:
        return fatal_error_envelop()
    else:
        return record_updated_envelop(request.json)

@api.route('/divisionpositions/<int:id>', methods=['GET'])
def get_division_position(id):
    try:
        dv = db_session.query(DivisionPosition).filter(DivisionPosition.id == id).one()
    except NoResultFound:
        return record_notfound_envelop()
    except Exception:
        return fatal_error_envelop()
    else:
        return record_json_envelop(dv.to_dict())