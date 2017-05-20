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
    EmployeePosition

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


@api.route('/empcategoryranks', methods=['POST'])
@create_update_permission('config_management_perm')
def create_emp_cat_ranks():
    if not request.json:
        abort(400)
    if not 'name' in request.json.keys():
        abort(401)
    
    if len(request.json['name'].strip()) < 2:
        abort(411)
    

    #if everything is fine
    name = request.json['name'].replace(' ', '').lower().strip()
    display_name = request.json['name'].strip()

    #put to db
    try:
        rank = EmployeeCategoryRank(name=name, display_name=display_name)
        db_session.add(rank)
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)


@api.route('/empcategoryranks', methods=['GET'])
@read_permission('read_management_perm')
def get_emp_cat_ranks():

    try:
        ranks = db_session.query(EmployeeCategoryRank).order_by(EmployeeCategoryRank.name).all()
        ranks = (dict(id=rank.id,
                      name = rank.display_name, del_flag=rank.del_flag) for rank in ranks)
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(ranks))

@api.route('/empcategoryranks/<int:id>', methods=['PUT'])
@create_update_permission('config_management_perm')
def update_rank(id):
    if not request.json:
        abort(400)
    
    if 'name' in request.json:
        request.json['display_name'] = request.json['name']
        request.json['name'] = request.json['name'].lower().strip()
    
    #now try to update the facilty name
    

    try:
        db_session.query(EmployeeCategoryRank).filter(EmployeeCategoryRank.id==id).update(request.json)
        
        db_session.commit()
    except NoResultFound as e:
        abort(404)
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        raise
        abort(500)

    else:
        return record_updated_envelop(request.json)


@api.route('/empcategoryranks/<int:rank_id>/empcategories', methods=['POST'])
@create_update_permission('config_management_perm')
def create_emp_cat(rank_id):
    if not request.json:
        abort(400)
    if not 'name' in request.json.keys():
        abort(401)
    
    if len(request.json['name'].strip()) < 2:
        abort(411)
    
    #strip down the values
    display_name = request.json['name'].strip()
    name = display_name.lower().replace(' ', '')
    emp_cat_rank_id = None
    if not emp_cat_rank_id == 0:
        emp_cat_rank_id = rank_id

    
    #try to put onto databas
    try:
        cat = EmployeeCategory(name=name, display_name=display_name, emp_cat_rank_id=emp_cat_rank_id)
        db_session.add(cat)
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)


@api.route('/empcategories', methods=['GET'])
@read_permission('read_management_perm')
def get_emp_categories():

    try:
        ranks = db_session.query(EmployeeCategory).order_by(EmployeeCategory.name).all()
        rks = (dict(id=rank.id, name=rank.display_name,
         emp_cat_rank=rank.emp_cat_rank.display_name,
         emp_cat_rank_id=rank.emp_cat_rank.id,
         del_flag=rank.del_flag) for rank in ranks)
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(rks))
        

@api.route('/empcategories/<int:id>', methods=['PUT'])
@create_update_permission('config_management_perm')
def update_emp_category(id):
    if not request.json:
        abort(400)
    if not all(len(val.strip())>=1 for key, val in request.json.items() if isinstance(val, str)):
        abort(411)
    
    if 'name' in request.json:
        request.json['display_name'] = request.json['name']
        request.json['name'] = request.json['name'].strip().lower()

    try:
        db_session.query(EmployeeCategory).filter(EmployeeCategory.id==id).update(request.json)
        
        db_session.commit()
    except NoResultFound as e:
        abort(404)
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        
        abort(500)
    else:
        return record_updated_envelop(request.json)



@api.route('/employeetypes', methods=['POST'])
@create_update_permission('config_management_perm')
def create_employee_type():

    if not request.json:
        abort(400)
    
    if not 'name' in request.json.keys():
        abort(401)
    
    if len(request.json['name'].strip()) < 2:
        abort(411)
    
    #clear up the values
    display_name = request.json['name'].strip()
    name = display_name.lower().replace(' ', '')

    try:
        e_type = EmployeeType(name=name, display_name=display_name)
        db_session.add(e_type)
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json) 
    

@api.route('/employeetypes', methods=['GET'])
@read_permission('read_management_perm')
def get_employee_types():

    try:
        types = db_session.query(EmployeeType).all()
        tys = (dict(id=ty.id, name=ty.display_name, del_flag=ty.del_flag) for ty in types)
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(tys))
    


@api.route('/employeetypes/<int:id>', methods=['PUT'])
@create_update_permission('config_management_perm')
def update_emp_type(id):
    if not request.json:
        abort(400)
    
    if not all(len(val.strip())>=1 for key, val in request.json.items() if isinstance(val, str)):
        abort(411)
    #now try to update the facilty name
    if 'name' in request.json:
        request.json['display_name'] = request.json['name'] 
        request.json['name'] = request.json['name'].strip().lower()   
    try:
        db_session.query(EmployeeType).filter(EmployeeType.id==id).update(request.json)
      
        db_session.commit()
    except NoResultFound as e:
        abort(404)
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        
        abort(500)
    else:
        return record_updated_envelop(request.json)


#get the employees by ranks

@api.route('/empcategoryranks/<r_id>/employees', methods=['GET'])
@read_permission('read_management_perm')
def get_employees_by_rank(r_id):
    try:
        rank = db_session.query(EmployeeCategoryRank).filter(EmployeeCategoryRank.id==r_id).one()
        #flatten out the list
        employees = itertools.chain.from_iterable(cat.employees for cat in rank.emp_categories)
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(emp.to_dict() for emp in employees))


#get the employees by categories
@api.route('/empcategories/<int:c_id>/employees')
@read_permission('read_management_perm')
def get_employees_by_category(c_id):
    try:
        cat = db_session.query(EmployeeCategory).filter(EmployeeCategory.id==c_id).one()
        if cat is None:
            raise NoResultFound()
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        employees = cat.employees
        return records_json_envelop(list(emp.to_dict() for emp in employees))
    


@api.route('/emppositions', methods=['POST'])
def create_emp_position():
    if not request.json:
        abort(401)
    required_fields = set(col.name for col in EmployeePosition.__mapper__.columns) - {'id', 'emp_pos_title_display_name'}
    
    extra_fields = set(request.json) - required_fields
    if extra_fields:
        return extra_keys_envelop('Unknown Keys : %s' % ', '.join(key for key in extra_fields))
    
    _required = required_fields - set(request.json)

    if _required:
       return missing_keys_envelop('Required Keys : %s' % ', '.join(key for key in _required))
    
    #check to see if there is any blank 

    if not all(len(val.strip()) >= 1 for key, val in request.json.items() if isinstance(val, str)):
        return length_require_envelop()
    #inject 
    
    request.json['emp_pos_title_display_name'] = request.json['emp_pos_title']
    request.json['emp_pos_title'] = request.json['emp_pos_title'].lower().strip()
    #initiate the dession
    try:
        e_type = EmployeePosition(**request.json)
        db_session.add(e_type)
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)


@api.route('/emppositions', methods=['GET'])
def get_emp_positions():
    try:
        ps = db_session.query(EmployeePosition).all()
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return records_json_envelop([p.to_dict() for p in ps])

@api.route('/emppositions/<int:p_id>', methods=['PUT'])
def update_emp_positions(p_id):
    #should do the error handling later
    if not request.json:
        abort(401)
    
    if not all(len(val.strip())>=1 for key, val in request.json.items() if isinstance(val, str)):
        abort(411)
        
    if 'emp_pos_title' in request.json:
        request.json['emp_pos_title_display_name'] = request.json['emp_pos_title']
        request.json['emp_pos_title'] = request.json['emp_pos_title'].lower().strip()
    try:
        db_session.query(EmployeePosition).filter(EmployeePosition.id == p_id).update(request.json)
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_updated_envelop(request.json)