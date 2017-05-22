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


# @api.route('', methods=['POST'])
# @create_update_permission('agency_emp_perm')
# def create_qualification_by_emp(id):
#     if not request.json:
#         abort(400)
#     #check if there is empty field comming up
#     if not all(len(str(val).strip()) >= 1 for key, val in request.json.items()):
#         abort(411)
#     #clean up the values
#     qual = {key : val.strip() if isinstance(val, str) else val for key, val in request.json.items()}
#     #insert
#     print(qual)
#     qual['employee_id'] = id
#     #######################
#     qual['start_date'] = '03-jan-2018'
#     qual['end_date'] = '05-jan-2020'
#     ###############
#     try:
#         print(id)
#         db_session.add(Qualification(**qual))
#         db_session.commit()
#     except IntegrityError as e:
#         return fatal_error_envelop()
#     except Exception as e:
#         return fatal_error_envelop()t
#     else:
#         return record_created_envelop(request.json)

