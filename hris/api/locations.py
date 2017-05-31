from hris.utils import hash_password, gen_access_token, decode_access_token
from flask import request, abort, jsonify, g
from functools import wraps

from hris.api import api
from sqlalchemy.exc import IntegrityError #foreign key violation #this won't come up oftern
from sqlalchemy.orm.exc import NoResultFound
from hris import db_session

#auth


from hris.models import (
    FacilityType,
    LLG,
    District,
    Province,
    Region
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
    record_deleted_envelop
)
from hris.api.auth import (
    allow_permission, 
    create_update_permission,
    read_permission
)





@api.route('/facilitytypes/<int:f_id>', methods=['DELETE'])
@create_update_permission('company_management_perm')
def delete_facility_type(f_id):
    if not request.json:
        abort(401)
    
    try:
        db_session.query(FacilityType).filter(FacilityType.id == f_id).update({'del_flag' : True})
        db_session.commit()
    except NoResultFound as e:
        return record_notfound_envelop()
    else:
        return record_deleted_envelop()




@api.route('/districts', methods=['POST'])
@create_update_permission('company_management_perm')
def create_district():
    if not set(request.json.keys()) == {'name', 'district_code', 'province_id'}:
        return jsonify({'message' : 'missing keys'})
    
    if not len(request.json['name']) > 3:
        return jsonify({'message' : 'not adequate lenght'})
    
    #lower case the facility name
    display_name = request.json['name'].strip()
    name = request.json['name'].replace(' ','').lower().strip()
    district_code = request.json['district_code']
    province_id = request.json['province_id']


    #insert into the database
    try:
        dis = District(name=name, display_name=display_name, district_code=district_code, province_id=province_id)
        db_session.add(dis)
        db_session.commit()
    except IntegrityError as ie:
        raise
        return record_exists_envelop()
    
    else:
        return record_created_envelop(request.json)


@api.route('/llg', methods=['POST'])
@create_update_permission('company_management_perm')
def create_llg():
    print('This function was called')
    if not set(request.json.keys()) == {'name', 'llg_code', 'district_id'}:
        return jsonify({'message' : 'missing keys'})
    
    if not len(request.json['name']) > 3:
        return jsonify({'message' : 'not adequate length'})
    
    #lower case the facility name
    display_name = request.json['name'].strip()
    name = request.json['name'].replace(' ', '').lower().strip()
    llg_code = request.json['llg_code']
    district_id = request.json['district_id']
    #insert into the database
    try:
        dis = LLG(name=name, display_name=display_name, llg_code=llg_code, district_id=district_id)
        db_session.add(dis)
        db_session.commit()
    except IntegrityError as ie:
        return record_exists_envelop()
    
    else:
        return record_created_envelop(request.json)


@api.route('/provinces', methods=['POST'])
@create_update_permission('company_management_perm')
def create_province():
    if not set(request.json.keys()) == {'name', 'province_code', 'region_id'}:
        return jsonify({'message' : 'missing keys'})
    
    if not len(request.json['name']) > 3:
        return jsonify({'message' : 'not adequate length'})
    
    #lower case the facility name
    display_name = request.json['name'].strip()
    name = request.json['name'].replace(' ', '').lower().strip()
    province_code = request.json['province_code'].upper().strip()
    region_id = request.json['region_id']
    #insert into the database
    try:
        dis = Province(
            name=name,
            display_name=display_name,
            province_code=province_code,
            region_id=region_id)
        db_session.add(dis)
        db_session.commit()
    except IntegrityError as ie:
        return record_exists_envelop()
    except Exception as e:
        print(e)
        return fatal_error_envelop()
    
    else:
        return record_created_envelop(request.json)

@api.route('/regions', methods=['POST'])
@create_update_permission('company_management_perm')
def create_region():
    if not request.json:
        abort(400)
    if not all(len(val.strip()) >= 1 for val in request.json.values() if isinstance(val, str)):
        abort(404)
    
    if 'name' in request.json:
        request.json['display_name'] = request.json['name'].strip()
        request.json['name'] = request.json['name'].lower().strip()
    try:
        dis = Region(**request.json)
        db_session.add(dis)
        db_session.commit()
    except IntegrityError as ie:
        return record_exists_envelop()
    
    else:
        return record_created_envelop(request.json)
    

#...........................>#


@api.route('/llg', methods=['GET'])
@read_permission('read_management_perm')
def get_llg():
    
    try:
        llgs = db_session.query(LLG).order_by(LLG.name).all()
        gen_exp = (f.to_dict() for f in llgs)
        return records_json_envelop(list(gen_exp))
    except Exception as e:
        return fatal_error_envelop()


@api.route('/districts', methods=['GET'])
@read_permission('read_management_perm')
def get_districts():
    
    try:
        districts = db_session.query(District).order_by(District.name).all()
        gen_exp = (f.to_dict() for f in districts)
        return records_json_envelop(list(gen_exp))
    except Exception as e:
        return fatal_error_envelop()

@api.route('/provinces', methods=['GET'])
@read_permission('read_management_perm')
def get_provinces():
    
    try:
        provinces = db_session.query(Province).order_by(Province.name).all()
        gen_exp = (p.to_dict() for p in provinces)
        return records_json_envelop(list(gen_exp))
    except Exception as e:
        raise
        return fatal_error_envelop()


@api.route('/regions', methods=['GET'])
@read_permission('read_management_perm')
def get_regions():
    
    try:
        provinces = db_session.query(Region).order_by(Region.name).all()
        gen_exp = (dict(name = f.display_name, id=f.id, region_code=f.region_code if f.region_code else '', del_flag=f.del_flag) for f in provinces)
        return records_json_envelop(list(gen_exp))
    except Exception as e:
        return fatal_error_envelop()
#..............................
    




@api.route('/llg/<int:id>', methods=['PUT'])
@create_update_permission('company_management_perm')
def update_llg(id):
    if not request.json:
        abort(400)
    
    #clearn up the json_request
    _cleaner = lambda s : s.strip() if isinstance(s, str) else s
    _request = {key: _cleaner(val) for key, val in request.json.items()}

    if 'name' in _request:
        _request['display_name'] = _request['name']
        _request['name'] = _request['name'].lower().strip()

    #remove the id field
    if 'id' in _request:
        del _request['id']

    try:
        #for oracle
        #_bool_mapper = lambda s : 0 if s == 'false' else 1
        #for oracle
        _bool_mapper = lambda s : s
        _json = {key : _bool_mapper(val) if val in ('true', 'false') else val for key, val in _request.items()}
    
        db_session.query(LLG).filter(LLG.id == id).update(_json)
       
        db_session.commit()
    except NoResultFound as e:
        abort(404)
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        
        abort(500)
    else:
        return record_updated_envelop(request.json)
@api.route('/llg/<int:id>', methods=['DELETE'])
def delete_llg(id):
    try:
        p = db_session.query(LLG).filter(LLG.id == id).one()
        db_session.delete(p)
        db_session.commit()
    except NoResultFound as e:
        abort(404)
    except Exception as e:
        abort(500)
    else:
        return jsonify({'code' : 200, 'status' : 'success', 'message' : 'deleted successfully'})

@api.route('/districts/<int:id>', methods=['PUT'])
@create_update_permission('company_management_perm')
def update_district(id):
    if not request.json:
        abort(400)
    if 'name' in request.json:
        request.json['display_name'] = request.json['name']
        request.json['name'] = request.json['name'].lower().strip()
    
    #clearn up the json_request
    _cleaner = lambda s : s.strip() if isinstance(s, str) else s
    _request = {key: _cleaner(val) for key, val in request.json.items()}

    #remove the id field
    if 'id' in request.json:
        del request['id']
    

    try:
        #for oracle
        #_bool_mapper = lambda s : 0 if s == 'false' else 1
        #for oracle
        _bool_mapper = lambda s : s
        _json = {key : _bool_mapper(val) if val in ('true', 'false') else val for key, val in _request.items()}
    
        db_session.query(District).filter(District.id == id).update(_json)
       
        db_session.commit()
    except NoResultFound as e:
        abort(404)
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        abort(500)
    else:
        return record_updated_envelop(request.json)

@api.route('/districts/<int:id>', methods=['DELETE'])
def delete_district(id):
    try:
        p = db_session.query(District).filter(District.id == id).one()
        db_session.delete(p)
        db_session.commit()
    except NoResultFound as e:
        abort(404)
    except Exception as e:
        abort(500)
    else:
        return jsonify({'code' : 200, 'status' : 'success', 'message' : 'deleted successfully'}) 

@api.route('/provinces/<int:id>', methods=['PUT'])
@create_update_permission('company_management_perm')
def update_province(id):
    if not request.json:
        abort(400)
   #clearn up the json_request
    _cleaner = lambda s : s.strip() if isinstance(s, str) else s
    _request = {key: _cleaner(val) for key, val in request.json.items()}

    if 'name' in _request:
        _request['display_name'] = _request['name']
        _request['name'] = _request['name'].lower().strip()

    #remove the id field
    if 'id' in request.json:
        del request['id']

    try:
        #for oracle
        #_bool_mapper = lambda s : 0 if s == 'false' else 1
        #for oracle
        _bool_mapper = lambda s : s
        _json = {key : _bool_mapper(val) if val in ('true', 'false') else val for key, val in _request.items()}
    
        db_session.query(Province).filter(Province.id == id).update(_json)
       
        db_session.commit()
        
    except NoResultFound as e:
        abort(404)
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
         
        abort(500)
    else:
        return record_updated_envelop(request.json)

@api.route('/provinces/<int:id>', methods=['DELETE'])
def delete_province(id):
    try:
        p = db_session.query(Province).filter(Province.id == id).one()
        db_session.delete(p)
        db_session.commit()
    except NoResultFound as e:
        abort(404)
    except Exception as e:
        abort(500)
    else:
        return jsonify({'code' : 200, 'status' : 'success', 'message' : 'deleted successfully'})
    
@api.route('/regions/<int:id>', methods=['PUT'])
@create_update_permission('company_management_perm')
def update_region(id):
    if not request.json:
        abort(400)
    
    #clearn up the json_request
    _cleaner = lambda s : s.strip() if isinstance(s, str) else s
    _request = {key: _cleaner(val) for key, val in request.json.items()}
    if 'name' in _request:
        _request['display_name']  = _request['name']
        _request['name'] = _request['name'].lower().strip()

    #remove the id field
    if 'id' in request.json:
        del request['id']
    


    try:
        #for oracle
        #_bool_mapper = lambda s : 0 if s == 'false' else 1
        #for oracle
        _bool_mapper = lambda s : s
        _json = {key : _bool_mapper(val) if val in ('true', 'false') else val for key, val in _request.items()}
    
        db_session.query(Region).filter(Region.id == id).update(_json)
        #facility = db_session.query(Region).filter(Region.id==id).one()
        #facility.name = name
        #facility.display_name = display_name
        #db_session.add(facility)
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

    


    
@api.route('/regions/<int:id>', methods=['DELETE'])
def delete_region(id):
    try:
        p = db_session.query(Region).filter(Region.id == id).one()
        db_session.delete(p)
        db_session.commit()
    except NoResultFound as e:
        abort(404)
    except Exception as e:
        abort(500)
    else:
        return jsonify({'code' : 200, 'status' : 'success', 'message' : 'deleted successfully'})



@api.errorhandler(400)
def badrequest(error):
    return jsonify({'message' : 'Bad request'}), 400

@api.errorhandler(401)
def missingkeys(error):
    return jsonify({'message': 'Missing keys'}), 401

@api.errorhandler(404)
def notfound(error):
    return record_notfound_envelop(), 404

@api.errorhandler(500)
def servererror(error):
    return fatal_error_envelop(), 500

@api.errorhandler(411)
def lengthrequired(error):
    return length_require_envelop(), 411 

