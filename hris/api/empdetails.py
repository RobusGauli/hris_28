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
    if not all(len(val.strip()) >= 1 for key, val in request.json.items()):
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


@api.route('/employees/<int:id>/relatives', methods=['POST'])
def create_relative_bye_emp(id):
    if not request.json:
        abort(400)
    #check to see if there are any fields
    if not all(len(val.strip()) >= 1 for val in request.json.values() if isinstance(val, str)):
        abort(411)
    request.json['employee_id'] = id
    try:
        db_session.add(EmployeeRelative(**request.json))
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)

@api.route('/employees/<int:id>/relatives/<int:rel_id>', methods=['PUT'])
def update_relative_by_emp(id, rel_id):
    if not request.json:
        abort(400)
    
    if not all(len(val.strip())>=0 for val in request.json.values() if isinstance(val, str)):
        abort(411)
    
    #request.json['id'] = rel_id
    try:
        db_session.query(EmployeeRelative).filter(EmployeeRelative.id == rel_id).update(request.json)
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_updated_envelop(request.json)


@api.route('/employees/<int:id>/relatives', methods=['GET'])
def get_relatives_by_emp(id):

    
    #request.json['id'] = rel_id
    try:
        relatives = db_session.query(EmployeeRelative).filter(EmployeeRelative.employee_id == id).all()

        
    except NoResultFound as e:
        return result_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(r.to_dict() for r in relatives))

@api.route('/employees/<int:id>/histories', methods=['GET'])
def get_emphistories_by_emp(id):
    try:
        histories = db_session.query(EmployementHistory).\
                    filter(EmployementHistory.employee_id == id).all()
    except NoResultFound as e:
        return result_notfound_envelop()
    except Exception as e:
        raise
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(h.to_dict() for h in histories))

@api.route('/employees/<int:id>/histories', methods=['POST'])
def create_emphistory_by_emp(id):
    if not request.json:
        abort(400)
    if not all(len(val.strip()) >= 1 for val in request.json.values() if isinstance(val, str)):
        abort(411)
    request.json['employee_id'] = id
    try:
        db_session.add(EmployementHistory(**request.json))
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)

@api.route('/employees/<int:id>/histories/<int:e_id>', methods=['PUT'])
def update_emphistory_by_emp(id, e_id):
    if not request.json:
        abort(400)
    if not all(len(val.strip()) >= 1 for val in request.json.values() if isinstance(val, str)):
        abort(411)
    try:
        db_session.query(EmployementHistory).filter(EmployementHistory.id == e_id).\
                                            update(request.json)
        db_session.commit()
    except NoResultFound:
        return record_notfound_envelop()
    except IntegrityError:
        return record_exists_envelop()
    except Exception:
        return fatal_error_envelop()
    else:
        return record_updated_envelop(request.json)
    

@api.route('/employees/<int:id>/empreferences', methods=['POST'])
def create_emp_reference(id):
    if not request.json:
        abort(400)
    #check to see if there are any empty fields
    if not all(len(val.strip()) >= 1 for val in request.json.values()):
        abort(411)
    #now insert the shit down
    request.json['employee_id'] = id
    try:
        db_session.add(EmployeeReference(**request.json))
        db_session.commit()
    except IntegrityError: 
        return record_exists_envelop()
    except Exception:
        #raise
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)

@api.route('/employees/<int:id>/empreferences', methods=['GET'])
def get_emp_references(id):
    try:
        references = db_session.query(EmployeeReference)\
                        .filter(EmployeeReference.employee_id == id).all()
    except NoResultFound:
        return record_notfound_envelop()
    except Exception:
        raise
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(r.to_dict() for r in references))

@api.route('/employees/<int:e_id>/empreferences/<int:r_id>', methods=['PUT'])
def update_emp_references(e_id, r_id):
    if not request.json:
        abort(400)
    if not all(len(val.strip()) >= 1 for val in request.json.values() if isinstance(val, str)):
        abort(411)
    
    try:
        db_session.query(EmployeeReference).filter(EmployeeReference.id == r_id).\
                                                            update(request.json)
        db_session.commit()
    except IntegrityError:
        return record_notfound_envelop()
    except Exception:
        return fatal_error_envelop()
    else:
        return record_updated_envelop(request.json)


@api.route('/employees/<int:id>/empbenifits', methods=['POST'])
def create_emp_benifit(id):
    if not request.json:
        abort(400)
    #check to see if there are any empty fields
    if not all(len(val.strip()) >= 1 for val in request.json.values()):
        abort(411)
    #now insert the shit down
    request.json['employee_id'] = id
    try:
        db_session.add(EmployeeBenifit(**request.json))
        db_session.commit()
    except IntegrityError: 
        return record_exists_envelop()
    except Exception:
        #raise
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)

@api.route('/employees/<int:id>/empbenifits', methods=['GET'])
def get_emp_benifits(id):
    try:
        bns = db_session.query(EmployeeBenifit)\
                        .filter(EmployeeBenifit.employee_id == id).all()
    except NoResultFound:
        return record_notfound_envelop()
    except Exception:
        raise
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(r.to_dict() for r in bns))

@api.route('/employees/<int:e_id>/empbenifits/<int:b_id>', methods=['PUT'])
def update_emp_benifits(e_id, b_id):
    if not request.json:
        abort(400)
    if not all(len(val.strip()) >= 1 for val in request.json.values() if isinstance(val, str)):
        abort(411)
    
    try:
        db_session.query(EmployeeBenifit).filter(EmployeeBenifit.id == b_id).\
                                                            update(request.json)
        db_session.commit()
    except IntegrityError:
        return record_notfound_envelop()
    except Exception:
        return fatal_error_envelop()
    else:
        return record_updated_envelop(request.json)



@api.route('/employees/<int:id>/empdisc', methods=['POST'])
def create_emp_disciplinary(id):
    if not request.json:
        abort(400)
    #check to see if there are any empty fields
    if not all(len(val.strip()) >= 1 for val in request.json.values()):
        abort(411)
    #now insert the shit down
    request.json['employee_id'] = id
    try:
        db_session.add(EmployeeDisciplinary(**request.json))
        db_session.commit()
    except IntegrityError: 
        return record_exists_envelop()
    except Exception:
        #raise
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)

@api.route('/employees/<int:id>/empdisc', methods=['GET'])
def get_emp_disc(id):
    try:
        bns = db_session.query(EmployeeDisciplinary)\
                        .filter(EmployeeDisciplinary.employee_id == id).all()
    except NoResultFound:
        return record_notfound_envelop()
    except Exception:
        raise
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(r.to_dict() for r in bns))



@api.route('/employees/<int:e_id>/empdisc/<int:b_id>', methods=['PUT'])
def update_emp_disc(e_id, b_id):
    if not request.json:
        abort(400)
    if not all(len(val.strip()) >= 1 for val in request.json.values() if isinstance(val, str)):
        abort(411)
    
    try:
        db_session.query(EmployeeDisciplinary).filter(EmployeeDisciplinary.id == b_id).\
                                                            update(request.json)
        db_session.commit()
    except IntegrityError:
        return record_notfound_envelop()
    except Exception:
        return fatal_error_envelop()
    else:
        return record_updated_envelop(request.json)


@api.route('/employees/<int:id>/empappraisal', methods=['POST'])
def create_emp_appraisal(id):
    if not request.json:
        abort(400)
    #check to see if there are any empty fields
    if not all(len(val.strip()) >= 1 for val in request.json.values()):
        abort(411)
    #now insert the shit down
    request.json['employee_id'] = id
    try:
        db_session.add(EmployeeAppraisal(**request.json))
        db_session.commit()
    except IntegrityError: 
        return record_exists_envelop()
    except Exception:
        #raise
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)

@api.route('/employees/<int:id>/empappraisal', methods=['GET'])
def get_emp_appraisal(id):
    try:
        bns = db_session.query(EmployeeAppraisal)\
                        .filter(EmployeeAppraisal.employee_id == id).all()
    except NoResultFound:
        return record_notfound_envelop()
    except Exception:
        raise
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(r.to_dict() for r in bns))



@api.route('/employees/<int:e_id>/empappraisal/<int:b_id>', methods=['PUT'])
def update_emp_appraisal(e_id, b_id):
    if not request.json:
        abort(400)
    if not all(len(val.strip()) >= 1 for val in request.json.values() if isinstance(val, str)):
        abort(411)
    
    try:
        db_session.query(EmployeeAppraisal).filter(EmployeeAppraisal.id == b_id).\
                                                            update(request.json)
        db_session.commit()
    except IntegrityError:
        return record_notfound_envelop()
    except Exception:
        return fatal_error_envelop()
    else:
        return record_updated_envelop(request.json)

