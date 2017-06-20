from hris.utils import hash_password, gen_access_token, decode_access_token
from flask import request, abort, jsonify, g
from functools import wraps

from hris.api import api
from sqlalchemy.exc import IntegrityError #foreign key violation #this won't come up oftern
from sqlalchemy.orm.exc import NoResultFound
from hris import db_session
from hris import engine

#auth
######this is me and that i
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
    Training
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
    extra_keys_envelop,
    keys_require_envelop
)

from hris.api.auth import (
    allow_permission, 
    create_update_permission,
    read_permission
)


@api.route('/employees', methods=['POST'])
@create_update_permission('agency_emp_perm')
def create_employee():
    
    if not request.json:
        abort(400)
    
    req_fields = {'first_name',
                  'last_name', 
                  'current_sex', 
                  'address_one', 
                  'age', 
                  'retirement_age', 
                  'employee_type_id', 
                  'employee_category_id',
                  'date_of_birth',
                  'employee_position_id',
                  'employement_number',
                  'employee_agency_id'}
    result = req_fields  - set(request.json.keys())

    #if there is some value then abort
    if result:
        
        return keys_require_envelop('Key required %s' % ', '.join(result))
       
    
    #if everything is included, check to see if there is any empty values
    # if not all(len(str(val).strip()) >= 1 for key, val in request.json.items()):
    #     abort(411)
    
    #now clean up the data to insert into database(onyl for strin)
    data = {key : val.strip() if isinstance(val, str) else val for key, val in request.json.items()}
    
    #for oracle
        #data['date_of_birth'] = '01-feb-2017'
        #data['date_of_commencement'] = '02-feb-2011'
    #now try to insert
    #for raocle
 
    try:
        
        emp = Employee(**data)
        db_session.add(emp)
        db_session.commit()
    except IntegrityError as e:
        
        return record_exists_envelop()
    except Exception as e:
        print(e)
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)

    

@api.route('/employees/<int:id>', methods=['PUT'])
@create_update_permission('agency_emp_perm')
def update_employee(id):
    '''This i iwill user the raw sql query because this would be easier to reason about'''

    if not request.json:
        abort(400)
    
    # if not all(len(str(val).strip()) >= 1 for key, val in request.json.items()):
    #     abort(411)

    if 'age' not in request.json or 'retirement_age' not in request.json:
        return jsonify({'message' : 'please send both the age and retirement_age'})
        abort(400)
    age = request.json['age']
    retirement_age = request.json['retirement_age']
    #first check about the age
    if int(age) > int(retirement_age) or int(age) < 18:
        return record_not_updated_env('Age cannot be more than retirement age or less than 18')
    
    #clean up the data
    data = {key : val.strip() if isinstance(val, str) else val for key, val in request.json.items()}

   
    try:
        db_session.query(Employee).filter(Employee.id == id).update(request.json)
        db_session.commit()

    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_updated_envelop(request.json)



@api.route('/employees', methods=['GET'])
@read_permission('agency_emp_perm')
def get_employees():
    
    try:
        employees = db_session.query(Employee).filter(Employee.del_flag==False).all()
        emps = ({ 'first_name' : emp.first_name if emp.first_name else '',
                  'middle_name' : emp.middle_name if emp.middle_name else '',
                  'last_name' : emp.last_name if emp.last_name else '',
                  'current_sex' : emp.current_sex if emp.current_sex else '',
                  'date_of_birth' : str(emp.date_of_birth) if emp.date_of_birth else '',
                  'address_one' : emp.address_one if emp.address_one else '',
                  'address_two' : emp.address_two if emp.address_two else '',
                  'village' : emp.village if emp.village else '',
                  'llg' : emp.llg if emp.llg else '',
                  'district' : emp.district if emp.district else '',
                  'province' : emp.province if emp.province else '',
                  'region' : emp.region if emp.region else '',
                  'country' : emp.country if emp.country else '',
                  'email_address' : emp.email_address if emp.email_address else '',
                  'contact_number' : emp.contact_number if emp.contact_number else '',
                  'alt_contact_number' : emp.alt_contact_number if emp.alt_contact_number else '',
                  'age' : emp.age if emp.age else '',
                  'retirement_age' : emp.retirement_age if emp.retirement_age else '',
                  'employement_number' : emp.employement_number if emp.employement_number else '',
                  'salary_step' : emp.salary_step if emp.salary_step else '',
                  'date_of_commencement' : str(emp.date_of_commencement) if emp.date_of_commencement else '',
                  'contract_end_date' : emp.contract_end_date if emp.contract_end_date else '',
                  'id' : emp.id if emp.id else '',
                  'user_id' : emp.user_id if emp.user_id else '',
                  'employee_agency_id' : emp.employee_agency_id if emp.employee_agency_id else '',
                  'role_id' : emp.user.role_id if emp.user else '',
                  'salutation' : emp.salutation if emp.salutation else '',
                  'fullname' : emp.first_name + ' ' + emp.last_name,
                  'sex_at_birth' : emp.sex_at_birth if emp.sex_at_birth else ''
                                    

        } for emp in employees)
    except Exception as e:
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(emps))


@api.route('/employees/<int:id>')
@read_permission('read_management_perm')
def get_employee(id):
    try:
        emp  = db_session.query(Employee).filter(Employee.id==id).one()
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_json_envelop({ 'first_name' : emp.first_name if emp.first_name else '',
                  'middle_name' : emp.middle_name if emp.middle_name else '',
                  'last_name' : emp.last_name if emp.last_name else '',
                  ##this is asdas
                  'current_sex' : emp.current_sex if emp.current_sex else '',
                  'date_of_birth' : str(emp.date_of_birth) if emp.date_of_birth else '',
                  'address_one' : emp.address_one if emp.address_one else '',
                  'address_two' : emp.address_two if emp.address_two else '',
                  'village' : emp.village if emp.village else '',
                  'llg' : emp.llg if emp.llg else '',
                  'district' : emp.district if emp.district else '',
                  'province' : emp.province if emp.province else '',
                  'region' : emp.region if emp.region else '',
                  'country' : emp.country if emp.country else '',
                  'email_address' : emp.email_address if emp.email_address else '',
                  'contact_number' : emp.contact_number if emp.contact_number else '',
                  'alt_contact_number' : emp.alt_contact_number if emp.alt_contact_number else '',
                  'age' : emp.age if emp.age else '',
                  'retirement_age' : emp.retirement_age if emp.retirement_age else '',
                  'employement_number' : emp.employement_number if emp.employement_number else '',
                  'salary_step' : emp.salary_step if emp.salary_step else '',
                  'date_of_commencement' : str(emp.date_of_commencement) if emp.date_of_commencement else '',
                  'contract_end_date' : emp.contract_end_date if emp.contract_end_date else '',
                  'id' : emp.id if emp.id else '',
                  'user_id' : emp.user_id if emp.user_id else '',
                  'sex_at_birth' : emp.sex_at_birth if emp.sex_at_birth else '',
                  
                  
                  'employee_type' : emp.employee_type.display_name if emp.employee_type.display_name else '',
                  'employee_category' : emp.employee_category.name if emp.employee_category.name else '',
                  'employee_position' : emp.employee_position.emp_pos_title_display_name if emp.employee_position.emp_pos_title_display_name else '',
                  'employee_agency_id' : emp.employee_agency_id if emp.employee_agency_id else '',
                  'employee_agency' : emp.employee_agency.display_name if emp.employee_agency else '',
                  'employee_type_id' : emp.employee_type_id if emp.employee_type_id else '',
                  'employee_position_id' : emp.employee_position_id if emp.employee_position_id else '',
                  'employee_category_id' : emp.employee_category_id if emp.employee_category_id else '',
                  'salutation' : emp.salutation if emp.salutation else '',
                  'other_name_one' : emp.other_name_one if emp.other_name_one else '',
                  'other_name_two' : emp.other_name_two if emp.other_name_two else '',
                  'other_name_three' : emp.other_name_three if emp.other_name_three else '',
                  'maiden_name' : emp.maiden_name if emp.maiden_name else ''

        })


@api.route('/employees/<int:id>/qualifications', methods=['POST'])
@create_update_permission('agency_emp_perm')
def create_qualification_by_emp(id):
    if not request.json:
        abort(400)
    #check if there is empty field comming up
    if not all(len(str(val).strip()) >= 1 for key, val in request.json.items()):
        abort(411)
    #clean up the values
    qual = {key : val.strip() if isinstance(val, str) else val for key, val in request.json.items()}
    #insert
    print(qual)
    qual['employee_id'] = id
    #######################
    qual['start_date'] = '03-jan-2018'
    qual['end_date'] = '05-jan-2020'
    ###############
    try:
        print(id)
        db_session.add(Qualification(**qual))
        db_session.commit()
    except IntegrityError as e:
        return fatal_error_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)


@api.route('/employees/<int:id>/qualifications', methods=['GET'])
@read_permission('read_management_perm')
def get_qualifications_by_emp(id):
    try:
        qls = db_session.query(Qualification).filter(Qualification.employee_id==id).all()
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        quals = ({
            'id' : q.id,
            'name' : q.name if q.name else '',
            'institute_name' : q.institute_name if q.institute_name else '',
            'city' : q.city if q.city else '',
            'state' : q.state if q.state else '',
            'province' : q.province if q.province else '',
            'country' : q.country if q.country else '',
            'start_date' : str(q.start_date) if q.start_date else '',
            'end_date' : str(q.end_date) if q.end_date else ''
        } for q in qls)
        return records_json_envelop(list(quals))


@api.route('/employees/<int:emp_id>/qualifications/<int:q_id>', methods=['PUT'])
@create_update_permission('agency_emp_perm')
def update_qualification_by_emp(emp_id, q_id):
    if not request.json:
        abort(400)
    try:
        db_session.query(Qualification).filter(Qualification.id == q_id).update(request.json)
        eb_session.commit()
    except IntegrityError:
        return record_exists_envelop()
    except Exception:
        return fatal_error_envelop()
    else:
        return record_updated_envelop(request.json)
        

############@@@@############

@api.route('/employees/<int:id>/certifications', methods=['POST'])
@create_update_permission('agency_emp_perm')
def create_certification_by_emp(id):
    if not request.json:
        abort(400)
    #check if there is empty field comming up
    if not all(len(str(val).strip()) >= 1 for key, val in request.json.items()):
        abort(411)
    
    #check if there is no registration number and registration body
    result = {'regulatory_body', 'registration_number'} - set(request.json.keys())
    if result:
        return keys_require_envelop('"regulatory_body" and "regstration_number" is required')
    #clean up the values
    cert = {key : val.strip() if isinstance(val, str) else val for key, val in request.json.items()}
    #insert
    cert['employee_id'] = id
    ###################################
    #cert['expiry_date'] = '04-mar-2012'
    #cert['last_renewal_date'] = '03-mar-2017'
    ################################
    try:
        
        db_session.add(Certification(**cert))
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)

@api.route('/employees/<int:id>/certifications', methods=['GET'])
@read_permission('read_management_perm')
def get_certifications_by_emp(id):
    try:
        certs = db_session.query(Certification).filter(Certification.employee_id==id).all()
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        certs = ({
            'id' : q.id,
            'registration_number' : q.registration_number if q.registration_number else '',
            'regulatory_body' : q.regulatory_body if q.regulatory_body else '',
            'registration_type' : q.registration_type if q.registration_type else '',
            'last_renewal_date' : str(q.last_renewal_date) if q.last_renewal_date else '',
            'expiry_date' : str(q.expiry_date) if q.expiry_date else '',
            'issue_date' : str(q.issue_data) if q.issue_data else '',
            'regulatory_body_address_one' : q.regulatory_body_address_one if q.regulatory_body_address_one else '',
            'regulatory_body_address_two' : q.regulatory_body_address_two if q.regulatory_body_address_two else '',
            'regulatory_body_address_country' : q.regulatory_body_address_country if q.regulatory_body_address_country else ''
            
            
        } for q in certs)
        return records_json_envelop(list(certs))


@api.route('/employees/<int:emp_id>/certifications/<int:c_id>', methods=['PUT'])
@create_update_permission('agency_emp_perm')
def update_certification_by_emp(emp_id, c_id):
    if not request.json:
        abort(400)
    #check to see if there is any empty values
    if not all(len(str(val).strip()) for val in request.json.values()):
        abort(411)
    #check to see if the request has the right type of keys
    result = set(request.json.keys()) - set(col.name for col in Certification.__mapper__.columns)
    if result:
        
        return extra_keys_envelop('Keys: {!r} not accepted'.format(', '.join(r for r in result)))
    
    #clearn up the values for string
    #generator expression
    cleaned_json = ((key, val.strip()) if isinstance(val, str) else (key, val) for key, val in request.json.items())
        #this means that it has extra set of keys that is not necessary
    #make the custom query
    
    

    #try to executre
  
    try:
        db_session.query(Certification).filter(Certification.id == c_id).update(dict(cleaned_json))
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_updated_envelop(request.json)


#######------------------__##########################

@api.route('/employees/<int:id>/trainings', methods=['POST'])
@create_update_permission('agency_emp_perm')
def create_training_by_emp(id):
    if not request.json:
        abort(400)
    #check if there is empty field comming up
    if not all(len(str(val).strip()) >= 1 for key, val in request.json.items()):
        abort(411)
    
    #check if there is no registration number and registration body
    result = {'name'} - set(request.json.keys())
    if result:
        return keys_require_envelop('key : "name" is required')
    #clean up the values
    trs = {key : val.strip() if isinstance(val, str) else val for key, val in request.json.items()}
    #insert
    ###################################
    trs['start_date'] = '01-feb-2012'
    trs['end_date'] = '03-feb-2005'
    ##########################
    print(id)
    trs['employee_id'] = id
    try:
        print(id)
        db_session.add(Training(**trs))
        db_session.commit()
    except IntegrityError as e:
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json)

@api.route('/employees/<int:id>/trainings', methods=['GET'])
@read_permission('read_management_perm')
def get_trainings_by_emp(id):
    try:
        trs = db_session.query(Training).filter(Training.employee_id==id).all()
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        trs = ({
            'id' : q.id,
            'name' : q.name if q.name else '',
            'organiser_name' : q.organiser_name if q.organiser_name else '',
            'funding_source' : q.funding_source if q.funding_source else '',
            'duration' : q.duration if q.duration else '',
            'institute' : q.institue if q.institue else '',
            'duration' : q.duration if q.duration else '',
            'city' : q.city if q.city else '',
            'state' : q.state if q.state else '',
            'province' : q.province if q.province else ''            
        } for q in trs)
        return records_json_envelop(list(trs))


@api.route('/employees/<int:emp_id>/trainings/<int:t_id>', methods=['PUT'])
@create_update_permission('agency_emp_perm')
def update_training_by_emp(emp_id, t_id):
    if not request.json:
        abort(400)
    #check to see if there is any empty values
    if not all(len(str(val).strip()) for val in request.json.values()):
        abort(411)
    #check to see if the request has the right type of keys
    result = request.json.keys() - set(col.name for col in Training.__mapper__.columns)
    if result:
        
        return extra_keys_envelop('Keys: {!r} not accepted'.format(', '.join(r for r in result)))
    
    #clearn up the values for string
    #generator expression
    cleaned_json = ((key, val.strip()) if isinstance(val, str) else (key, val) for key, val in request.json.items())
        #this means that it has extra set of keys that is not necessary
    #make the custom query
    inner = ', '.join('{:s} = {!r}'.format(key, val) for key, val in cleaned_json)
    query = '''UPDATE trainings SET {:s} WHERE id = {:d}'''.format(inner, t_id)
    

    #try to executre
    with engine.connect() as con:
        try:
            con.execute(query)
        except IntegrityError as e:
            return record_exists_envelop()
        except Exception as e:
            return fatal_error_envelop()
        else:
            return record_updated_envelop(request.json)


#####employee extra details endpoints

@api.route('/employees/<int:id>/empextras', methods=['POST'])
def create_employee_extra(id):
    #cheek to see if ther is json
    if not request.json:
        abort(400)
    #if there is json,  if there are required fields
    required_keys = set(col.name for col in EmployeeExtra.__mapper__.columns) - {'id', 'employee_id'}
    
    
    #keys from the rquest object
    result = set(request.json.keys()) - required_keys
    
    #if there is extra remaining keys , abort
    if result:
        return extra_keys_envelop('keys not accepeted %r' % result)
    
    #check to see if there are any valuekjdhflkjadsfaklsdhfkajsds less than 1
    if not all(len(str(val).strip())>=1 for val in request.json.values()):
        return length_require_envelop()
    #clearn up the dictionary
    json_vals = {key : val.strip() if isinstance(val, str) else val for key, val in request.json.items()}
    
    #try to insert to database
    json_vals['employee_id'] = id
    try:
        db_session.add(EmployeeExtra(**json_vals))
        db_session.commit()
    except IntegrityError as e:
        
        return record_exists_envelop()
    except Exception as e:
        raise e
        return fatal_error_envelop()
    else:
        return record_created_envelop(request.json) 


@api.route('/employees/<int:id>/empextras', methods=['GET'])
def get_empextras_by_emp(id):
    try:
        q = db_session.query(EmployeeExtra).filter(EmployeeExtra.employee_id==id).one()
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        tr = {
            'id' : q.id,
            'ref_name' : q.ref_name if q.ref_name else '',
            'ref_address' : q.ref_address if q.ref_address else '',
            'ref_contact_number' : q.ref_contact_number if q.ref_contact_number else '',
            'emp_father_name' : q.emp_father_name if q.emp_father_name else '',
            'emp_mother_name' : q.emp_mother_name if q.emp_mother_name else '',
            'emp_single' : q.emp_single if q.emp_single else '',
            'emp_wife_name' : q.emp_wife_name if q.emp_wife_name else '',
            'emp_num_of_children' : q.emp_num_of_children if q.emp_num_of_children else ''
                       
        }
        return record_json_envelop(tr)


@api.route('/employees/<int:emp_id>/empextras', methods=['PUT'])
def update_empextra_by_emp(emp_id):
    if not request.json:
        abort(400)
    #check to see if there is any empty values
    if not all(len(str(val).strip()) for val in request.json.values()):
        abort(411)
    #check to see if the request has the right type of keys
    result = set(request.json.keys()) - set(col.name for col in EmployeeExtra.__mapper__.columns)
    if result:
        
        return extra_keys_envelop('Keys: {!r} not accepted'.format(', '.join(r for r in result)))
    
    #clearn up the values for string
    #generator expression
    cleaned_json = ((key, val.strip()) if isinstance(val, str) else (key, val) for key, val in request.json.items())
        #this means that it has extra set of keys that is not necessary
    #make the custom query
    
    cleaned_json = dict(cleaned_json)
    cleaned_json['employee_id'] = emp_id

    #try to executre
    
    try:
        
        nr = db_session.query(EmployeeExtra).filter(EmployeeExtra.employee_id==emp_id).update(dict(cleaned_json))
        print(nr)
        if nr == 0:
            #that means there is no data for that employee so add the data
            db_session.add(EmployeeExtra(**cleaned_json))
            #db_session.commit()
            
        db_session.commit()
    except NoResultFound as e:

        return record_notfound_envelop()
    except IntegrityError as e:
        raise
        return record_exists_envelop()
    except Exception as e:
        return fatal_error_envelop()
    else:
        return record_updated_envelop(request.json)

#listing of emplloyees by branches, agencies, by individual branch and individual agencies

#all the employee of divisions
@api.route('/employees/division', methods=['GET'])
@read_permission('read_management_perm')
def get_employees_of_divisions():
    
    try:
        employees = db_session.query(Employee).filter(Employee.is_branch==True).all()
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(employee.to_dict() for employee in employees))



@api.route('/employees/agency', methods=['GET'])
@read_permission('read_management_perm')
def get_employees_of_agencies():
    try:
        employees = db_session.query(Employee).filter(Employee.is_branch==False).all()
    except NoResultFound as e:
        return record_notfound_envelop()
    except Exception as e:
        
        return fatal_error_envelop()
    else:
        return records_json_envelop(list(employee.to_dict() for employee in employees))



