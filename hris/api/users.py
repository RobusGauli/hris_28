from hris.utils import hash_password, gen_access_token, decode_access_token
from flask import request, abort, jsonify, g, current_app
from functools import wraps
#this is me and that i need you

from hris.api import api
from sqlalchemy.exc import IntegrityError #foreign key violation #this won't come up oftern
from sqlalchemy.orm.exc import NoResultFound
from hris import db_session

#auth
import re
###
from hris.models import (
    User, 
    CompanyDetail,
    Employee,
    PasswordPolicy
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
    length_require_envelop
)

from hris.api.auth import (
    allow_permission, 
    create_update_permission,
    read_permission
)


def validate_password(password, user_name):
    '''This is to be validated'''
    print(password, user_name)
    validated = True
    message = ''
    password = password.strip()
    policy = db_session.query(PasswordPolicy).filter(PasswordPolicy.id == 1).one()
    policy = policy.to_dict()
    print(policy)
    max_len = policy.get('max_len', None)
    if max_len is not None:
        if len(password) > int(max_len):
            message = 'Password length should be less than %d' % int(max_len)
            
            return False, message 
    min_len = policy.get('min_len', None)
    if min_len is not None:
        if len(password) <= int(min_len):
            message = 'Password length should be more than %d' % min_len
            
            return False, message
    if policy.get('upper_case', False):
        if not re.search(r'[A-Z]', password):
            message = 'Password must contain atleast on Uppercase character'
            validated = False
            return validated, message
    if policy.get('special_character', False):
        if not re.search(r'[^A-Za-z0-9]', password):
            message = 'Password must contain atleast one special character Eg: #$&*@'
            return False, message
    if policy.get('similar_username', False):
        if password == user_name:
            message = 'Password cannot be same as your username'
            return False, message
    return validated, message


@api.route('/users', methods=['POST'])
def register_user():
    '''This view register the user by generating ht access token with the given role'''
    if request.args and request.args['action'] == 'register':
    
    #check if all key existst
        if not set(request.json.keys()) == {'user_name', 'password', 'role_id'}:
            return jsonify({'message' : 'missing keys'})
        #check for the password policy
        #validate_password(request.json)
    #lower case the user_name
        if any(len(val.strip()) < 5 for val in request.json.values() if isinstance(val, str)):
            return jsonify({'message' : 'Not adequate length of values'})

    #lower case the user_name
        user_name = request.json['user_name'].strip().lower()
        role_id = request.json['role_id']
        hashed_pass = hash_password(request.json['password'].encode())
    #get the user access_token
        user_access_token = gen_access_token(role_id, user_name)
        user = User(user_name=user_name, password=hashed_pass, role_id=role_id, access_token=user_access_token.decode('utf-8'))
        try:
            db_session.add(user)

            db_session.commit()
        except IntegrityError as ie:
        #hadle the error heres
            
            return record_exists_envelop()
        

        else:
            return jsonify({'message' : 'user_added_successfully', 'access_token' : user_access_token.decode('utf-8')})

    elif request.args['action'] == 'login':
        if request.json:
            if not set(request.json.keys()) == {'user_name', 'password'}:
                return jsonify({'message' : 'missing keys'})
        else:
            return jsonify({'message': 'json object'})

        user_name = request.json['user_name']
        password = request.json['password']

        #now hass the password
        hashed_pass = hash_password(password)
        
        #get the user from the users for the password and user name
        try:
            user = db_session.query(User).filter(User.user_name==user_name).one()
            if not user:
                return record_notfound_envelop('User doesn\'t exists')
            #check to see if del_flag is true
            if user.del_flag and user.del_flag == True:
                return record_notfound_envelop('User not found' )
            #if there is user check for the password
            if hashed_pass == user.password:
                return record_json_envelop({'access_token' : user.access_token, 'activate' : user.activate, 'role_id' : user.role_id, 'permissions' : user.role.to_dict(), 'password_changed' : user.password_changed})
            else:
                return record_notfound_envelop('Password doesn\'t match')
        except NoResultFound as e:
            return record_notfound_envelop('User doesn\'t exists')
    ###to register the user with the employee


    elif request.args['action'] == 'registeruserforemployee':
        if not request.args.get('e_id', None):
            return 'please  send the e_id'
        e_id = int(request.args['e_id'])

        if not set(request.json.keys()) == {'user_name', 'password', 'role_id'}:
            return jsonify({'message' : 'missing keys'})
    
    #lower case the user_name
        if any(len(val.strip()) < 5 for val in request.json.values() if isinstance(val, str)):
            return jsonify({'message' : 'Not adequate length of values'})

    #lower case the user_name
        user_name = request.json['user_name'].strip().lower()

        role_id = request.json['role_id']
        result, err = validate_password(request.json.get('password'), user_name)
        
        if result == False:
            return jsonify({'message' : err, 'status': 'fail'})
        hashed_pass = hash_password(request.json['password'].strip().encode())
    #get the user access_token
        user_access_token = gen_access_token(role_id, user_name)
        user = User(user_name=user_name, password=hashed_pass, role_id=role_id, access_token=user_access_token.decode('utf-8'))
        try:
            emp = db_session.query(Employee).filter(Employee.id==e_id).one()

            db_session.add(user)
            emp.user = user
            db_session.add(emp)
            db_session.commit()
        except IntegrityError as ie:
        #hadle the error here
            return record_exists_envelop()
        
        except NoResultFound as e:
            return record_notfound_envelop()
        

        else:
            return jsonify({'message' : 'user_added_successfully', 'access_token' : user_access_token.decode('utf-8'), 'status': 'success'})


@api.route('/company', methods=['PUT'])
def add_company_detail():

    if not request.json:
        abort(400)
    
    db_fields = set(col.name for col in CompanyDetail.__mapper__.columns)
    
    extra_keys = set(request.json.keys()) - (db_fields - {'id'})
    if extra_keys:
        return jsonify({'Message' : 'Extra keys : %r' % ', '.join(col for col in extra_keys)})
    try:
        
        db_session.query(CompanyDetail).filter(CompanyDetail.id == 1).update(request.json)
        db_session.commit()
    except NoResultFound as e:
        abort(404)
    except Exception as e:
        abort(500)
    else:
        return record_updated_envelop(request.json)



@api.route('/passwordpolicy', methods=['PUT'])
def add_password_policy():
    if not request.json:
        return abort(400)
    
    db_fields = set(col.name for col in PasswordPolicy.__mapper__.columns)

    extra_keys = set(request.json.keys()) - (db_fields - {'id'})
    if extra_keys:
        return jsonify({'Message' : 'Extra Keys : %r' % ', '.join(col for col in extra_keys)})
    
    try:
        _bool_mapper = lambda s : 0 if s == 'false' else 1
        _json = {key : _bool_mapper(val) if val in ('true', 'false') else val for key, val in request.json.items()}
        db_session.query(PasswordPolicy).filter(PasswordPolicy.id == 1).update(_json)
        db_session.commit()
    except NoResultFound as e:
        abort(404)
    except Exception as e:
        abort(500)
    else:
        return record_updated_envelop(request.json)


@api.route('/passwordpolicy', methods =['GET'])
def get_password_policy():
    try:
        pol = db_session.query(PasswordPolicy).filter(PasswordPolicy.id == 1).one()
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_json_envelop(pol.to_dict())



@api.route('/company', methods=['GET'])
def get_company_detail():
    try:
        company = db_session.query(CompanyDetail).filter(CompanyDetail.id == 1).one()
        adict = company.to_dict()
        district = db_session.query(District).filter(District.id == int(company.district)).one()
        adict['district_name'] = district.display_name
        adict['province_name'] = district.province.display_name
        adict['region_name'] = district.province.region.display_name

    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_json_envelop(adict)
    

@api.route('/users', methods = ['GET'])
@read_permission('read_management_perm')
def get_users():
    try:
        users = db_session.query(User).filter(User.user_name != 'admin').all()
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(user.to_dict() for user in users))



@api.route('/users/<int:u_id>', methods=['PUT'])
@create_update_permission('user_management_perm')
def update_user(u_id):
    if not request.json:
        abort(400)
    
    if request.args.get('action') == 'update_activation':
        try:
            db_session.query(User).filter(User.id==u_id).update(request.json)
            db_session.commit()
        except NoResultFound as e:
            return result_notfound_envelop()
        except Exception as e:
            return fatal_error_envelop()
        else:
            return record_updated_envelop(request.json)

    if not request.args.get('action') == 'update_role':

    
        if 'password' not in request.json.keys():
            return missing_keys_envelop()
        try:
            
            user = db_session.query(User).filter(User.id==u_id).one()
            if user is None:
                return record_notfound_envelop()
            result, err = validate_password(request.json.get('password'), user.user_name)
            print(result)
            if result == False:
                return jsonify({'message' : err, 'status': 'fail' })
            print('GOt here ----------')

            hashed_pass = hash_password(request.json['password'].strip().encode())
            old_hashed_pass = user.password
            if old_hashed_pass == hashed_pass:
                return jsonify({'message' : 'Please dont\'t use old password', 'status': 'fail'})
            else:
                user.password = hashed_pass
                if request.args.get('by') == 'user':
                    user.password_changed = True
                db_session.add(user)
                db_session.commit()

        except NoResultFound as e:
            return record_notfound_envelop()
        except Exception as e:
            return fatal_error_envelop()
        else:
            return record_updated_envelop('Password updated Successfully.')

    #update the role

    if 'role_id' not in request.json:
        return missing_keys_envelop()
    try:
        user = db_session.query(User).filter(User.id==u_id).one()
        if user is None:
            return record_notfound_envelop()
        user.role_id = int(request.json['role_id'])
        db_session.add(user)
        db_session.commit()
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        raise
        return fatal_error_envelop()
        
    else:
        return record_updated_envelop('Role updated successfully.')   
        



