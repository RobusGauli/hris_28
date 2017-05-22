from sqlalchemy import (
    Column, 
    String, 
    Integer,
    ForeignKey,
    Text, 
    Enum, 
    CheckConstraint, 
    DateTime,
    func, 
    Date,
    Float,
    Boolean,
    Sequence
)



#default
#onupdate


from psycopg2 import IntegrityError

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Sequence

from hris import Base
##little hack to work in postgres
#################################
#should e deleted in oracle db
def dummy_sequence(name):
    return None

Sequence = dummy_sequence
##########################################
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, Sequence('user_id'),primary_key=True,  )
    user_name = Column(String(20), nullable=False, unique=True)
    password = Column(String(1000), nullable=False)
    access_token = Column(String(1000))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(String(20))
    updated_by = Column(String(20))
    role_id  = Column(Integer, ForeignKey('roles.id'))
    activate = Column(Boolean, default=True)
    del_flag = Column(Boolean, default=False)

    #employee_id
    password_changed = Column(Boolean, default=False)

    #relationship
    role = relationship('Role', back_populates='users')

    #one to one with employees
    employee = relationship('Employee', uselist=False, back_populates='user')


    def to_dict(self):
        data = {
            'user_name' : self.user_name if self.user_name else '',
            
            'role_id' : self.role_id if self.role_id else '',
            'employee_data' : self.employee.to_dict() if self.employee else {},
            'del_flag' : self.del_flag if self.del_flag else '',
            'id' : self.id if self.id else '',
            'role_name' : self.role.role_type
        }
        return data




class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, Sequence('rx_id'), primary_key=True)
    role_type = Column(String(100), unique=True, nullable=False)
    role_code = Column(String(20), unique=True, nullable=False)
    role_type_display_name = Column(String(200), nullable=False)
    activate = Column(Boolean, default=True)
    del_flag = Column(Boolean, default=False)
    agency_management_perm = Column(Enum('N', 'R', 'W', 'E',  name='amp'), default='N') 

    division_management_perm = Column(Enum('N', 'R', 'W', 'E',  name='dmp'), default='N') 
    agency_emp_perm = Column(Enum('N', 'R', 'W', 'E',  name='aep'), default='N') 

    division_emp_perm = Column(Enum('N', 'R', 'W', 'E',  name='dep'), default='N') 
    company_management_perm = Column(Enum('N', 'R', 'W', 'E',  name='cmp'), default='N') 
    config_management_perm = Column(Enum('N', 'R', 'W', 'E',  name='comp'), default='N')
    read_management_perm = Column(Enum('N', 'A', 'B', 'D', 'O',  name='rmp'), default='N')
    user_management_perm = Column(Enum('N', 'R', 'W', 'E', name='ump'), default='N')

    

    permission_eight = Column(Boolean, default=False)
    permission_nine = Column(Boolean, default=False)
    permission_ten = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(String(20))
    updated_by = Column(String(20))
    #relationship
    users = relationship('User', back_populates='role', cascade = 'all, delete, delete-orphan')
    
    
    def to_dict(self):
        role = {
            'role_type' : self.role_type,
            'id' : self.id,
            'agency_management_perm' : self.agency_management_perm if self.agency_management_perm else 'N',
            'activate' : self.activate if self.activate else True,
            'division_management_perm' : self.division_management_perm if self.division_management_perm else 'N',
            'agency_emp_perm' : self.agency_emp_perm if self.agency_emp_perm else 'N',
            'division_emp_perm' : self.division_emp_perm if self.division_emp_perm else 'N',
            'company_management_perm': self.company_management_perm if self.company_management_perm else 'N',
            'config_management_perm': self.config_management_perm if self.config_management_perm else 'N',
            'read_management_perm' : self.read_management_perm if self.read_management_perm else 'N',
            'user_management_perm' : self.user_management_perm if self.user_management_perm else 'O',
            'del_flag' : self.del_flag if self.del_flag else ''
            

            
        }
        return role
    
    



class CompanyDetail(Base):
    __tablename__ = 'companydetail'

    id = Column(Integer, Sequence('company_detail_id'), primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    display_name = Column(String(100), nullable=False)
    company_code = Column(String(10), unique=True)
    company_code_desc = Column(String(700))
    address_one = Column(String(40))
    address_two = Column(String(40))
    district = Column(String(100))
    province = Column(String(100))
    region = Column(String(100))
    llg = Column(String(100))
    village = Column(String(100))
    web_address = Column(String(100))
    email = Column(String(100))
    contact_person_name = Column(String(100))
    contact_person_email = Column(String(100))
    contact_person_alt_email = Column(String(100))
    free_text_one = Column(String(400))
    free_text_two = Column(String(400))
    free_text_three = Column(String(400))
    free_text_four = Column(String(400))
    free_text_five = Column(String(400))
    description = Column(String(700))
    currency_symbol = Column(String(2), unique=True)
    is_prefix = Column(Boolean, default=False)
    country = Column(String(30), nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    def to_dict(self):
        data = {
            'name' : self.name if self.name else '',
            'display_name' : self.display_name if self.display_name else '',
            'company_code' : self.company_code if self.company_code else '',
            'company_code_desc' : self.company_code_desc if self.company_code_desc else '',
            'address_one' : self.address_one if self.address_one else '',
            'address_two' : self.address_two if self.address_two else '',
            'district': self.district if self.district else '',
            'province' : self.province if self.province else '',
            'region' : self.region if self.region else '',
            'llg' : self.llg if self.llg else '',
            'village' : self.village if self.village else '',
            'web_address' : self.web_address if self.web_address else '',
            'email' : self.email if self.email else '',
            'contact_person_name' : self.contact_person_name if self.contact_person_name else '',
            'contact_person_email' : self.contact_person_email if self.contact_person_email else '',
            'contact_person_alt_email' : self.contact_person_alt_email if self.contact_person_alt_email else '',
            'free_text_one' : self.free_text_one if self.free_text_one else '',
            'free_text_two' : self.free_text_two if self.free_text_two else '',
            'free_text_three' : self.free_text_three if self.free_text_three else '',
            'free_text_four' : self.free_text_four if self.free_text_four else '',
            'free_text_five' : self.free_text_five if self.free_text_five else '',
            'country' : self.country if self.country else '' ,
            'description' : self.description if self.description else ''
        }
        return data






class Branch(Base):
    __tablename__ = 'branches'

    id = Column(Integer, Sequence('branches_id'), primary_key=True)
    is_branch = Column(Boolean, default=False)
    facility_name = Column(String(40), nullable=False, unique=True)
    facility_display_name = Column(String(40))
    acitivate = Column(Boolean, default=True)
    del_flag = Column(Boolean, default=False)

    branch_code = Column(String(10), unique=True)
    branch_code_desc = Column(String(700))
    address_one = Column(String(40))
    address_two = Column(String(40))
    web_address = Column(String(100))
    email = Column(String(100))
    contact_person_name = Column(String(100))
    contact_person_email = Column(String(100))
    contact_person_alt_email = Column(String(100))
    #foreignt keys
    facility_type_id = Column(Integer, ForeignKey('facilitytypes.id'))
    llg_id = Column(Integer, ForeignKey('llg.id'))
    district_id = Column(Integer, ForeignKey('districts.id'))
    province_id = Column(Integer, ForeignKey('provinces.id'))
    region_id = Column(Integer, ForeignKey('regions.id'))

    #relationship
    facility_type = relationship('FacilityType', back_populates='branches')
    llg = relationship('LLG', back_populates='branches')
    district = relationship('District', back_populates='branches')
    province = relationship('Province', back_populates='branches')
    region = relationship('Region', back_populates='branches')

    #realiationhsip
    employees = relationship('Employee', back_populates='employee_branch', cascade='all, delete, delete-orphan')






class FacilityType(Base):
    __tablename__ = 'facilitytypes'

    id = Column(Integer, Sequence('facility_type_id'), primary_key=True)
    name = Column(String(200), unique=True, nullable=False)
    display_name = Column(String(200), nullable=False, unique=True)
    del_flag = Column(Boolean, default=False)

    branches = relationship('Branch', back_populates='facility_type', cascade='all, delete, delete-orphan')



class LLG(Base):
    __tablename__ = 'llg'

    id = Column(Integer, Sequence('llg_id'),primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    llg_code = Column(String(3), unique=True, nullable=False)
    display_name = Column(String(200), unique=True, nullable=False)
    del_flag = Column(Boolean, default=False)
    branches = relationship('Branch', back_populates='llg', cascade='all, delete, delete-orphan')
    district_id = Column(Integer, ForeignKey('districts.id'))
    district = relationship('District', back_populates='llgs')

    def to_dict(self):
        return {
            'id' : self.id,
            'name' : self.display_name if self.display_name else '',
            'del_flag' : self.del_flag if self.del_flag else False,
            'llg_code' : self.llg_code if self.llg_code else '',
            'district' : self.district.display_name if self.district.display_name else '',
            'district_id' : self.district_id if self.district_id else '',
            
        }


class District(Base):
    __tablename__ = 'districts'
    
    id = Column(Integer, Sequence('districts_id'), primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    district_code = Column(String(5), unique=True, nullable=False)
    display_name = Column(String(200), unique=True, nullable=False)
    del_flag = Column(Boolean, default=False)

    branches = relationship('Branch', back_populates='district', cascade='all, delete, delete-orphan')
    province_id = Column(Integer, ForeignKey('provinces.id'), nullable=False)
    province = relationship('Province', back_populates='districtss')

    llgs = relationship('LLG', back_populates='district', cascade='all, delete, delete-orphan')

    def to_dict(self):
        return {
            'id' : self.id,
            'name' : self.display_name if self.display_name else '',
            'del_flag' : self.del_flag if self.del_flag else False,
            'district_code' : self.district_code if self.district_code else '',
            'province' : self.province.display_name if self.province.display_name else '',
            'province_id' : self.province_id if self.province_id else '',
            'llgs' : [
                { 'name' : l.display_name if l.display_name else ''} for l in self.llgs
            ]
            
        }

class Province(Base):
    __tablename__ = 'provinces'
    
    id = Column(Integer, Sequence('provinces_id'), primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    province_code = Column(String(5), unique=True, nullable=False)
    display_name = Column(String(200), unique=True, nullable=False)
    del_flag = Column(Boolean, default=False)
    branches = relationship('Branch', back_populates='province', cascade='all, delete, delete-orphan')

    region_id = Column(Integer, ForeignKey('regions.id'), nullable=False)
    region = relationship('Region', back_populates='provinceses')
    districtss = relationship('District', back_populates='province', cascade='all, delete, delete-orphan')

    def to_dict(self):
        return {
            'id' : self.id,
            'province_code' : self.province_code if self.province_code else '',
            'del_flag' : self.del_flag if self.del_flag else False,
            'name' : self.display_name if self.display_name else '',
            'region' : self.region.display_name if self.region.display_name else '',
            'region_id' : self.region_id if self.region_id else '',
            'districts' : [
                {'name' : d.display_name if d.display_name else ''} for d in self.districtss
            ] 
        }

class Region(Base):
    __tablename__ = 'regions'

    id = Column(Integer, Sequence('region_id'),primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    region_code = Column(String(5), unique=True, nullable=False)
    display_name = Column(String(200), unique=True, nullable=False)
    del_flag = Column(Boolean, default=False)

    branches = relationship('Branch', back_populates='region', cascade='all, delete, delete-orphan')
    provinceses = relationship('Province', back_populates='region', cascade='all, delete, delete-orphan')



#create an engine

#for employee
class EmployeeCategoryRank(Base):
    __tablename__ = 'emp_cat_ranks'

    id = Column(Integer, Sequence('emp_cat_rank_id'), primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    display_name = Column(String(100), nullable=False, unique=True)
    activate = Column(Boolean, default=True)
    del_flag = Column(Boolean, default=False)

    #realtionship 
    emp_categories = relationship('EmployeeCategory', back_populates='emp_cat_rank', cascade='all, delete, delete-orphan')

class EmployeeCategory(Base):
    __tablename__ = 'emp_categories'

    id = Column(Integer, Sequence('emp_cat_id'), primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    display_name = Column(String(50), nullable=False, unique=True)
    activate = Column(Boolean, default=True)
    emp_cat_rank_id = Column(Integer, ForeignKey('emp_cat_ranks.id'))
    del_flag = Column(Boolean, default=False)

    #realationship
    emp_cat_rank = relationship('EmployeeCategoryRank', back_populates='emp_categories')
    #relationship
    employees = relationship('Employee', back_populates='employee_category', cascade='all, delete, delete-orphan')


#lets hardcord the grade of the employee

class EmployeePosition(Base):
    __tablename__  = 'employeespositions'

    id = Column(Integer, Sequence('emp_pos_id'), primary_key=True)
    emp_pos_code = Column(String(10), unique=True, nullable=False)
    emp_pos_title = Column(String(40), unique=True, nullable=False)
    emp_pos_title_display_name = Column(String(40), nullable=False)
    emp_pos_sequence = Column(Integer, nullable=False)
    del_flag = Column(Boolean, default=False)
    #relationship
    employees = relationship('Employee', back_populates='employee_position', cascade='all, delete, delete-orphan')

    def to_dict(self):
        return {
            'id' : self.id,
            'emp_pos_code' : self.emp_pos_code if self.emp_pos_code else '',
            'emp_pos_title' : self.emp_pos_title_display_name if self.emp_pos_title_display_name else '',
            'emp_pos_sequence': self.emp_pos_sequence if self.emp_pos_sequence else '',
            'del_flag' : self.del_flag if self.del_flag else ''
        }


class EmployeeType(Base):
    __tablename__ = 'emp_types'

    id = Column(Integer, Sequence('emp_type_id'), primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    display_name = Column(String(100), nullable=False, unique=True)
    activate = Column(Boolean, default=True)
    del_flag = Column(Boolean, default=False)
    #relationship
    employees = relationship('Employee', back_populates='employee_type', cascade='all, delete, delete-orphan')

class SalaryStep(Base):
    __tablename__ = 'salarysteps'

    id = Column(Integer, Sequence('salary_step_id'), primary_key=True)
    val = Column(String(4), nullable=False, unique=True)
    activate = Column(Boolean, default=True)


class Employee(Base):
    __tablename__ = 'employees'

    id = Column(Integer, Sequence('employee_id'), primary_key=True)
    first_name = Column(String(40), nullable=False)
    middle_name = Column(String(40))
    last_name = Column(String(40), nullable=False)
    sex = Column(Enum('M', 'F', 'O', name='sex'), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    address_one = Column(String(50), nullable=False)
    address_two = Column(String(50))
    village = Column(String(100))
    llg = Column(String(100))
    district = Column(String(100))
    province = Column(String(100))
    region = Column(String(100))
    country = Column(String(40))
    email_address = Column(String(100), unique=True)
    contact_number = Column(String(30), unique=True)
    alt_contact_number = Column(String(30), unique=True)
    age = Column(Integer, nullable=False)
    retirement_age = Column(Integer, nullable=False, default=50)

    employement_number = Column(String(20), unique=True)
    salary_step = Column(String(6))
    date_of_commencement = Column(Date)
    contract_end_date = Column(Date)
    activate = Column(Boolean, default=True)
    salutation = Column(String(4), default='Mr')

    #about del flag
    del_flag = Column(Boolean, default=False)


    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(String(50))
    updated_by = Column(String(50))
    photo = Column(String(500), unique=True)
    document = Column(String(500), unique=True)

    is_branch = Column(Boolean, nullable=False, default=True)
    #branch_id_of_employee
    employee_branch_id = Column(Integer, ForeignKey('branches.id'), nullable=False)
    #relationship
    employee_branch = relationship('Branch', back_populates='employees')

    employee_type_id = Column(Integer, ForeignKey('emp_types.id'), nullable=False)
    employee_category_id = Column(Integer, ForeignKey('emp_categories.id'), nullable=False)
    employee_position_id = Column(Integer, ForeignKey('employeespositions.id'), nullable=False)
    #one to one with users table
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    user = relationship('User', back_populates='employee')

    #one to one with employeeextra table
    employee_extra = relationship('EmployeeExtra', uselist=False, back_populates='employee')

    #relationship 
    employee_type = relationship('EmployeeType', back_populates='employees')
    employee_category = relationship('EmployeeCategory', back_populates='employees')
    employee_position = relationship('EmployeePosition', back_populates='employees')
    #other relationship
    qualifications = relationship('Qualification', back_populates='employee', cascade='all, delete, delete-orphan')
    certifications = relationship('Certification', back_populates='employee', cascade='all, delete, delete-orphan')
    trainings = relationship('Training', back_populates='employee', cascade='all, delete, delete-orphan')
    relatives = relationship('EmployeeRelative', back_populates='employee', cascade='all, delete, delete-orphan')
    emp_histories =  relationship('EmployementHistory', back_populates='employee', cascade='all, delete, delete-orphan')
    emp_referenceses = relationship('EmployeeReference', back_populates='employee', cascade='all, delete, delete-orphan')
    emp_benifits = relationship('EmployeeBenifit', back_populates='employee', cascade='all, delete, delete-orphan')
    emp_disciplinaries = relationship('EmployeeDisciplinary', back_populates='employee', cascade='all, delete, delete-orphan')
    emp_appraisals = relationship('EmployeeAppraisal', back_populates='employee', cascade='all, delete, delete-orphan')
    
    def to_dict(self):
        data = {
            'employement_number' : self.employement_number if self.employement_number else '',
            'first_name' : self.first_name if self.first_name else '',
            'middle_name' : self.middle_name if self.middle_name else '',
            'last_name' : self.last_name if self.last_name else '',
            'address_one' : self.address_one if self.address_one else '',
            'contact_number' : self.contact_number if self.contact_number else '',
            'country' : self.country if self.country else '',
            'id' : self.id if self.id else ''
        }
        return data

class EmployeeExtra(Base):
    __tablename__ = 'employee_extra'

    id = Column(Integer, Sequence('emp_extra_id'), primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), unique=True)

    ref_name = Column(String(40))
    ref_address = Column(String(40))
    ref_contact_number = Column(String(20))
    emp_father_name = Column(String(40))
    emp_mother_name = Column(String(40))
    emp_single = Column(Boolean, default=True)
    emp_wife_name = Column(String(40))
    emp_num_of_children = Column(Integer)
    del_flag = Column(Boolean, default=False)

    #relationship
    employee = relationship('Employee', back_populates='employee_extra')

class EmployeeRelativeType(Base):
    __tablename__ = 'emp_relative_types'
    
    id = Column(Integer, Sequence('emp_rel_id'), primary_key=True)
    name = Column(String(100), nullable=False)
    display_name = Column(String(100), nullable=False)
    code = Column(String(30))
    del_flag = Column(Boolean, default=False)

    def to_dict(self):
        return {
            'name' : self.display_name if self.display_name else '',
            'code' : self.code if self.code else '',
            'del_flag' : self.del_flag
        }

class EmployeeRelative(Base):
    __tablename__ = 'emp_relatives'

    id = Column(Integer, Sequence('emp_rel'), primary_key=True)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    last_name = Column(String(100))
    address_one = Column(String(100))
    address_two = Column(String(100))
    country = Column(String(100))
    contact_number = Column(String(20))
    email = Column(String(50))
    del_flag = Column(Boolean, default=False)
    approved = Column(Boolean, default=False)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee_type = Column(String(100))
    employee = relationship('Employee', back_populates='relatives')


class EmployementHistory(Base):
    __tablename__ = 'emp_histories'

    id = Column(Integer, Sequence('emp_his_id'), primary_key=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    position = Column(String(100))
    reason_leaving = Column(String(100))
    description = Column(String(600))
    del_flag = Column(Boolean, default=False)
    approved = Column(Boolean, default=False)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    
    employee = relationship('Employee', back_populates='emp_histories')


class EmployeeReference(Base):
    __tablename__ = 'emp_references'

    id = Column(Integer, Sequence('emp_ref_id'), primary_key=True)
    first_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    last_name = Column(String(100))
    company = Column(String(100))
    email = Column(String(100))
    address_one = Column(String(100))
    address_two = Column(String(100))
    contact_number = Column(String(20))
    country = Column(String(100))
    del_flag = Column(Boolean, default=False)
    description = Column(String(600))

    approved = Column(Boolean, default=False)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    
    employee = relationship('Employee', back_populates='emp_referenceses')



class EmployeeBenifitType(Base):
    __tablename__ = 'emp_benifit_types'
    
    id = Column(Integer, Sequence('emp_rel_id'), primary_key=True)
    name = Column(String(100), nullable=False)
    display_name = Column(String(100), nullable=False)
    code = Column(String(30))
    del_flag = Column(Boolean, default=False)

class EmployeeBenifit(Base):
    __tablename__ = 'emp_benifits'

    id = Column(Integer, Sequence('emp_ben_id'), primary_key=True)
    benifit_type = Column(String(100), nullable=False)
    amount = Column(String(10))
    date = Column(DateTime)
    comment = Column(String(800))
    approved = Column(Boolean, default=False)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    del_flag = Column(Boolean, default=False) 
    employee = relationship('Employee', back_populates='emp_benifits')


class EmployeeDisciplinaryType(Base):
    __tablename__ = 'emp_disciplinary_types'
    
    id = Column(Integer, Sequence('emp_distype_id'), primary_key=True)
    name = Column(String(100), nullable=False)
    display_name = Column(String(100), nullable=False)
    code = Column(String(30))
    del_flag = Column(Boolean, default=False)

class EmployeeDisciplinary(Base):
    __tablename__ = 'emp_disciplinary'
    
    id = Column(Integer, Sequence('emp_dis_id'), primary_key=True)
    disciplinary_type = Column(String(100), nullable=False)
    date = Column(DateTime)
    department = Column(String(100))
    warning = Column(String(100))
    comment = Column(String(100))
    approved = Column(Boolean, default=False)
    del_flag = Column(Boolean, default=False)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship('Employee', back_populates='emp_disciplinaries')

class EmployeeAppraisalType(Base):
    __tablename__ = 'emp_appraisal_types'
    
    id = Column(Integer, Sequence('emp_appraisaltype_id'), primary_key=True)
    name = Column(String(100), nullable=False)
    display_name = Column(String(100), nullable=False)
    code = Column(String(30))
    del_flag = Column(Boolean, default=False)

class EmployeeAppraisal(Base):
    __tablename__ = 'emp_appraisals'
    
    id = Column(Integer, Sequence('emp_appraisal_id'), primary_key=True)
    appraisal_type = Column(String(100), nullable=False)
    date = Column(DateTime)
    department = Column(String(100))
    comment = Column(String(100))
    approved = Column(Boolean, default=False)
    del_flag = Column(Boolean, default=False)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship('Employee', back_populates='emp_appraisals')
    


class Qualification(Base):
    __tablename__ = 'qualifications'

    id = Column(Integer, Sequence('qual_id'), primary_key=True)
    name = Column(String(60))
    institute_name = Column(String(100))
    city = Column(String(30))
    state = Column(String(30))
    province = Column(String(30))
    country = Column(String(40))
    start_date = Column(Date)
    end_date = Column(Date)
    del_flag = Column(Boolean, default=False)

    employee_id = Column(Integer, ForeignKey('employees.id'))
    #relationship
    employee = relationship('Employee', back_populates='qualifications')


class Certification(Base):
    __tablename__ = 'certifications'

    id = Column(Integer, Sequence('cert_id'), primary_key=True)
    registration_number = Column(String(40), nullable=False, unique=True)
    regulatory_body = Column(String(40), nullable=False)
    issue_data = Column(Date)
    regulatory_body_address_one = Column(String(40))
    regulatory_body_address_two = Column(String(40))
    regulatory_body_address_three = Column(String(40))
    regulatory_body_address_country = Column(String(50))
    registration_type = Column(String(40))
    last_renewal_date = Column(Date)
    expiry_date = Column(Date)
    del_flag = Column(Boolean, default=False)
    
    employee_id = Column(Integer, ForeignKey('employees.id'))
    #relationship
    employee = relationship('Employee', back_populates='certifications')


class Training(Base):
    __tablename__ = 'trainings'

    id = Column(Integer, Sequence('t_id'), primary_key=True)
    name = Column(String(200), nullable=False)
    organiser_name = Column(String(200))
    funding_source = Column(String(200))
    duration = Column(String(30))
    institue = Column(String(50))
    
    city = Column(String(50))
    state = Column(String(50))
    province = Column(String(50))
    country = Column(String(50))
    start_date = Column(Date)
    end_date = Column(Date)
    del_flag = Column(Boolean, default=False)

    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship('Employee', back_populates='trainings')




class PasswordPolicy(Base):
    __tablename__ = 'passwordpolicy'

    id = Column(Integer, Sequence('policy_id'), primary_key=True)
    max_len = Column(Integer, nullable=False)
    min_len = Column(Integer, nullable=False)
    special_character = Column(Boolean, nullable=False, default=False)
    upper_case = Column(Boolean, nullable=False, default=False)
    similar_username = Column(Boolean, nullable=False, default=False)
    password_prompt = Column(Boolean, nullable=False, default=False)

    def to_dict(self):
        return {
            'max_len' : self.max_len if self.max_len else '',
            'min_len' : self.min_len if self.min_len else '',
            'special_character' : self.special_character if self.special_character is not None else '',
            'upper_case' : self.upper_case if self.upper_case is not None else '',
            'password_prompt' : self.password_prompt if self.password_prompt is not None else '',
            'similar_username' : self.similar_username if self.similar_username is not None else ''
        }

