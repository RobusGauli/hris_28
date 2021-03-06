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
    role_type = Column(String(30), unique=True, nullable=False)
    role_code = Column(String(10), unique=True, nullable=False)
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
    name = Column(String(50), unique=True, nullable=False)
    display_name = Column(String(50), nullable=False)
    company_code = Column(String(10), unique=True)
    company_code_desc = Column(String(100))
    address_one = Column(String(40))
    address_two = Column(String(40))
    district = Column(String(50))
    province = Column(String(50))
    region = Column(String(50))
    llg = Column(String(50))
    village = Column(String(50))
    web_address = Column(String(100))
    email = Column(String(50))
    contact_person_name = Column(String(50))
    contact_person_email = Column(String(50))
    contact_person_alt_email = Column(String(50))
    free_text_one = Column(String(100))
    free_text_two = Column(String(100))
    free_text_three = Column(String(100))
    free_text_four = Column(String(100))
    free_text_five = Column(String(100))
    description = Column(String(100))
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




class AgencyType(Base):
    __tablename__ = 'agencytypes'

    id = Column(Integer, Sequence('agencytypes_id'), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    display_name = Column(String(50), nullable=False)
    code = Column(String(10), unique=True)
    del_flag = Column(Boolean, default=False)
    #relationhsip
    agencies = relationship('Agency', back_populates='agency_type', cascade='all, delete, delete-orphan')
    
    _val_mapper = lambda self, item : item if item is not None else ''
    to_dict = lambda self : {key : self._val_mapper(val) for key, val in vars(self).items() if not key.startswith('_')}


    def __repr__(self):
        return '<AgencyType : %s id: %s>' % (self.display_name, self.id)

class Agency(Base):
    __tablename__ = 'agencies'

    id = Column(Integer, Sequence('agencies_id'), primary_key=True)
    code = Column(String(10), unique=True)
    name = Column(String(50), nullable=False, unique=True)
    display_name = Column(String(50), nullable=False)
    address_one = Column(String(50), nullable=False)
    address_two = Column(String(50), nullable=False)
    contact_number = Column(String(15), nullable=False)
    fax_number = Column(String(15), nullable=False)
    email = Column(String(50))
    con_person_name = Column(String(50))
    con_per_mob_num = Column(String(50))
    con_per_email = Column((String(50)))
    description = Column(String(100))
    district_id = Column(Integer, ForeignKey('districts.id'))
    province_id = Column(Integer, ForeignKey('provinces.id'))
    region_id = Column(Integer, ForeignKey('regions.id'))
    agency_type_id = Column(Integer, ForeignKey('agencytypes.id'))
    del_flag = Column(Boolean, default=False)

    
    
    #relationship
    district = relationship('District', back_populates='agencies')
    province = relationship('Province', back_populates='agencies')
    region = relationship('Region', back_populates='agencies')
    agency_type = relationship('AgencyType', back_populates='agencies')

    facilities = relationship('Facility', back_populates='agency', cascade='all, delete, delete-orphan')
    employees = relationship('Employee', back_populates = 'employee_agency', cascade='all, delete, delete-orphan')
    
    def to_dict(self):
        val_mapper  = lambda item : item if item else ''
        adict = {key : val_mapper(val) for key, val in vars(self).items() if not key.startswith('_')}
        adict['district'] = self.district.display_name if self.district else ''
        adict['province'] = self.province.display_name if self.district else ''
        adict['region'] = self.region.display_name if self.region else ''
        adict['agency_type'] = self.agency_type.display_name if self.agency_type else ''
        return adict
    
    def __repr__(self):
        return '<Agency : %s Id: %s>' % (self.display_name, self.id)

class Facility(Base):
    __tablename__ = 'facilities'

    id = Column(Integer, Sequence('facilties_id'), primary_key=True)
    under_ndoh = Column(Boolean, default=False)
    facility_name = Column(String(40), nullable=False, unique=True)
    facility_display_name = Column(String(40))
    acitivate = Column(Boolean, default=True)
    del_flag = Column(Boolean, default=False)

    facility_code = Column(String(10), unique=True)
    facility_code_desc = Column(String(100))
    address_one = Column(String(40))
    address_two = Column(String(40))
    web_address = Column(String(100))
    email = Column(String(50))
    contact_person_name = Column(String(50))
    contact_person_email = Column(String(50))
    contact_person_alt_email = Column(String(50))
    #foreignt keys
    facility_type_id = Column(Integer, ForeignKey('facilitytypes.id'))
    llg_id = Column(Integer, ForeignKey('llg.id'))
    district_id = Column(Integer, ForeignKey('districts.id'))
    province_id = Column(Integer, ForeignKey('provinces.id'))
    region_id = Column(Integer, ForeignKey('regions.id'))
    agency_id = Column(Integer, ForeignKey('agencies.id'))
    #relationship
    agency = relationship('Agency', back_populates='facilities')
    facility_type = relationship('FacilityType', back_populates='facilities')
    llg = relationship('LLG', back_populates='facilities')
    district = relationship('District', back_populates='facilities')
    province = relationship('Province', back_populates='facilities')
    region = relationship('Region', back_populates='facilities')

    gps_degree = Column(String(8))
    gps_minute = Column(String(8))
    gps_seconds = Column(String(8))
    gps_decimal_seconds = Column(String(8))

    #realiationhsip
    
    fac_divisions = relationship('FacilityDivision', back_populates = 'facility', cascade='all, delete, delete-orphan')

    _val_mapper = lambda self, item : item if item is not None else ''
    def to_dict(self):
        adict = {key : self._val_mapper(val) for key, val in vars(self).items() 
                                            if not key.startswith('_')}
        
        adict['agency'] = self.agency.display_name if self.agency else ''
        adict['facility_type'] = self.facility_type.display_name if self.facility_type else ''
        adict['district'] = self.district.display_name if self.district else ''
        adict['province'] = self.province.display_name if self.province else ''
        adict['region'] = self.region.display_name if self.region else ''
        adict['llg'] = self.llg.display_name if self.llg else ''
        
        return adict


    def __repr__(self):
        return '<Facility Name: %s Id: %s>' % (self.facility_display_name, self.id)



class FacilityType(Base):
    __tablename__ = 'facilitytypes'

    id = Column(Integer, Sequence('facility_type_id'), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    display_name = Column(String(50), nullable=False, unique=True)
    del_flag = Column(Boolean, default=False)

    facilities = relationship('Facility', back_populates='facility_type', cascade='all, delete, delete-orphan')

    _val_mapper = lambda self, item : item if item else ''
    to_dict = lambda self : {key : self._val_mapper(val) for key, val in vars(self).items() if not key.startswith('_')}


    def __repr__(self):
        return '<FacilityType Name: %s id: %s>' % (self.display_name, self.id)

class DivisionTypeSetup(Base):
    __tablename__ = 'divisiontypes'

    id = Column(Integer, Sequence('divisiontypes_id'), primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    display_name = Column(String(50))
    del_flag = Column(Boolean, default=False)

    #relationship
    divisions = relationship('Division', back_populates='division_type', cascade='all, delete, delete-orphan')
    _val_mapper = lambda self, item  : item if item else ''
    to_dict  = lambda self : {key : self._val_mapper(val) for key, val in vars(self).items()
                                                    if not key.startswith('_')}



class Division(Base):
    __tablename__ = 'divisions'

    id = Column(Integer, Sequence('divisions_id'), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    display_name = Column(String(50))
    code = Column(String(10), unique=True)
    division_type_id = Column(Integer, ForeignKey('divisiontypes.id'))
    del_flag = Column(Boolean, default=False)

    #realtionship
    division_type = relationship('DivisionTypeSetup', back_populates= 'divisions')

    _val_mapper = lambda self, item : item if item else ''

    def to_dict(self):
        adict = {key : self._val_mapper(val) for key, val in vars(self).items()
                                                if not key.startswith('_')}
        return adict
    
    def __repr___(self):
        return '<Division Name : %s Id : %s>' %(self.display_name, self.id)

class FacilityDivision(Base):
    __tablename__ = 'facility_divisions'

    id = Column(Integer, Sequence('fac_div_id'), primary_key=True)
    fac_div_name = Column(String(30), nullable=False)
    facility_id = Column(Integer, ForeignKey('facilities.id'), nullable=False)
    del_flag = Column(Boolean, default=False)
    #relationship
    facility = relationship('Facility', back_populates='fac_divisions')
    _val_mapper = lambda self, item : item if item else ''

    div_positions = relationship('DivisionPosition', back_populates='fac_div', cascade='all, delete, delete-orphan')


    def to_dict(self):
         return {
             'fac_div_name' : self.fac_div_name if self.fac_div_name else '',
             'del_flag' : self.del_flag if self.del_flag else '',
             'id' : self.id if self.id else ''
             
         }
    def __repr__(self):
        return '<FacilityDivision Name : %s Id : %s>' % (self.fac_div_name, self.id)

class DivisionPosition(Base):
    __tablename__ = 'division_positions'

    id = Column(Integer, Sequence('div_pos_id'), primary_key=True)
    div_pos_code = Column(String(9), unique=True, nullable=False)
    div_pos_name  = Column(String(20), unique=True, nullable=False)
    fac_div_id = Column(Integer, ForeignKey('facility_divisions.id'), nullable=False) #foreigne
    div_emp_id = Column(Integer, ForeignKey('employees.id'), unique=True, nullable=True) #foreign
    position_title = Column(String(50))
    description = Column(String(100))
    del_flag = Column(Boolean, default=False)
    #realtionship
    fac_div = relationship('FacilityDivision', back_populates='div_positions')
    div_emp = relationship('Employee', back_populates = 'div_position')

    def to_dict(self):
        #this is awesome
        adict = {key : val if val else '' for key, val in vars(self).items() if not key.startswith('_') }
        if self.div_emp:
            adict['fullname'] = self.div_emp.first_name + self.div_emp.last_name
            adict['employee_code'] = self.div_emp.employement_number
        else:
            adict['fullname'] = ''
        return adict
    
    def __repr__(self):
        return '<Division Position Code : %s Id : %s >' % (self.div_pos_code, self.id)


class DivisionPositionMeta(Base):
    __tablename__ = 'divposmeta'

    id = Column(Integer, Sequence('meta_id'), primary_key=True)
    fac_div_id = Column(Integer, ForeignKey('facility_divisions.id'), nullable=False)
    position_title = Column(String(50), nullable=False)
    position_capacity = Column(Integer, nullable=False)
    occupied_position = Column(Integer)

    _val_mapper = lambda self, item : item if item else ''
    to_dict = lambda self: {key: self._val_mapper(val) for key, val in 
                                         vars(self).items() if not key.startswith('_')}
                                

class LLG(Base):
    __tablename__ = 'llg'

    id = Column(Integer, Sequence('llg_id'),primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    llg_code = Column(String(3), unique=True, nullable=False)
    display_name = Column(String(50), unique=True, nullable=False)
    del_flag = Column(Boolean, default=False)
    facilities = relationship('Facility', back_populates='llg', cascade='all, delete, delete-orphan')
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
    def __repr__(self):
        return '<LLG : %s id: %s>' % (self.display_name, self.id)

class District(Base):
    __tablename__ = 'districts'
    
    id = Column(Integer, Sequence('districts_id'), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    district_code = Column(String(5), unique=True, nullable=False)
    display_name = Column(String(50), unique=True, nullable=False)
    del_flag = Column(Boolean, default=False)

    facilities = relationship('Facility', back_populates='district', cascade='all, delete, delete-orphan')
    province_id = Column(Integer, ForeignKey('provinces.id'), nullable=False)
    province = relationship('Province', back_populates='districtss')

    llgs = relationship('LLG', back_populates='district', cascade='all, delete, delete-orphan')

    agencies = relationship('Agency', back_populates='district', cascade='all, delete, delete-orphan')
    
    def to_dict(self):
        return {
            'id' : self.id,
            'name' : self.display_name if self.display_name else '',
            'del_flag' : self.del_flag if self.del_flag else False,
            'district_code' : self.district_code if self.district_code else '',
            'province' : self.province.display_name if self.province else '',
            'province_id' : self.province_id if self.province_id else ''
        
            
        }
    
    def __repr__(self):
        return '<District: %s id: %s>' % (self.display_name, self.id)

class Province(Base):
    __tablename__ = 'provinces'
    
    id = Column(Integer, Sequence('provinces_id'), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    province_code = Column(String(5), unique=True, nullable=False)
    display_name = Column(String(50), unique=True, nullable=False)
    del_flag = Column(Boolean, default=False)
    facilities = relationship('Facility', back_populates='province', cascade='all, delete, delete-orphan')

    region_id = Column(Integer, ForeignKey('regions.id'), nullable=False)
    region = relationship('Region', back_populates='provinceses')
    districtss = relationship('District', back_populates='province', cascade='all, delete, delete-orphan')
    agencies = relationship('Agency', back_populates='province', cascade='all, delete, delete-orphan')
    
    def to_dict(self):
        return {
            'id' : self.id,
            'province_code' : self.province_code if self.province_code else '',
            'del_flag' : self.del_flag if self.del_flag else False,
            'name' : self.display_name if self.display_name else '',
            'region_id' : self.region_id if self.region_id else '',
            'region' : self.region.display_name if self.region else ''
        }
    
    
    
    def __repr__(self):
        return '<Province: %s id: %s>' % (self.display_name, self.id)

class Region(Base):
    __tablename__ = 'regions'

    id = Column(Integer, Sequence('region_id'),primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    region_code = Column(String(5), unique=True, nullable=False)
    display_name = Column(String(50), unique=True, nullable=False)
    del_flag = Column(Boolean, default=False)

    facilities = relationship('Facility', back_populates='region', cascade='all, delete, delete-orphan')
    provinceses = relationship('Province', back_populates='region', cascade='all, delete, delete-orphan')

    agencies = relationship('Agency', back_populates='region', cascade='all, delete, delete-orphan')
    
    def __repr__(self):
        return '<Region: %s id: %s>' % (self.display_name, self.id)


#create an engine

#for employee
class EmployeeCategoryRank(Base):
    __tablename__ = 'emp_cat_ranks'

    id = Column(Integer, Sequence('emp_cat_rank_id'), primary_key=True)
    name = Column(String(50), nullable=False, unique=True)
    display_name = Column(String(50), nullable=False, unique=True)
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
    name = Column(String(50), nullable=False, unique=True)
    display_name = Column(String(50), nullable=False, unique=True)
    activate = Column(Boolean, default=True)
    del_flag = Column(Boolean, default=False)
    #relationship
    employees = relationship('Employee', back_populates='employee_type', cascade='all, delete, delete-orphan')

class EmployeeStatus(Base):
    __tablename__ = 'employeestatus'

    id = Column(Integer, Sequence('employeestatus_id'), primary_key=True)
    name = Column(String(30), nullable=False, unique=True)
    status_code = Column(String(3), unique=True, nullable=False)
    del_flag = Column(Boolean, default=False)

    _val_mapper = lambda self, item : item if item else ''
    to_dict = lambda self: {key: self._val_mapper(val) for key, val in vars(self).items()
                                                if not key.startswith('_')}

    employees = relationship('Employee', back_populates='employee_status', cascade='all, delete, delete-orphan')

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
    
    maiden_name  = Column(String(40))
    other_name_one = Column(String(40))
    other_name_two = Column(String(40))
    other_name_three = Column(String(40))
    sex_at_birth = Column(Enum('M', 'F', 'O', name='birthsex'))
    current_sex = Column(Enum('M', 'F', 'O', name='sex'), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    address_one = Column(String(50), nullable=False)
    address_two = Column(String(50))
    village = Column(String(50))
    llg = Column(String(50))
    district = Column(String(50))
    province = Column(String(50))
    region = Column(String(50))
    country = Column(String(50))
    email_address = Column(String(50), unique=True)
    contact_number = Column(String(30), unique=True)
    alt_contact_number = Column(String(30), unique=True)
    age = Column(Integer, nullable=False)
    retirement_age = Column(Integer, nullable=False, default=50)

    employement_number = Column(String(20), unique=True)
    salary_step = Column(String(6))
    date_of_commencement = Column(Date)
    contract_end_date = Column(Date)
    activate = Column(Boolean, default=True)
    salutation = Column(String(4))

    #about del flag
    del_flag = Column(Boolean, default=False)


    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(String(50))
    updated_by = Column(String(50))
    photo = Column(String(300), unique=True)
    document = Column(String(300), unique=True)

    under_ndoh = Column(Boolean, nullable=False, default=True)
    #branch_id_of_employee
    employee_agency_id = Column(Integer, ForeignKey('agencies.id'), nullable=False)
    #relationship

    employee_type_id = Column(Integer, ForeignKey('emp_types.id'), nullable=False)
    employee_category_id = Column(Integer, ForeignKey('emp_categories.id'), nullable=False)
    employee_position_id = Column(Integer, ForeignKey('employeespositions.id'), nullable=False)
    employee_status_id  = Column(Integer, ForeignKey('employeestatus.id'), nullable=False)
    #one to one with users table
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    user = relationship('User', back_populates='employee')

    #one to one with employeeextra table
    employee_extra = relationship('EmployeeExtra', uselist=False, back_populates='employee')
    div_position = relationship('DivisionPosition', uselist=False, back_populates='div_emp')
    employee_address = relationship('EmployeeAddress', uselist=False, back_populates='employee')

    #relationship 
    employee_type = relationship('EmployeeType', back_populates='employees')
    employee_category = relationship('EmployeeCategory', back_populates='employees')
    employee_position = relationship('EmployeePosition', back_populates='employees')
    employee_agency = relationship('Agency', back_populates='employees')
    employee_status = relationship('EmployeeStatus', back_populates='employees')

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
    employee_educations = relationship('EmployeeEducation', back_populates='employee', cascade='all, delete, delete-orphan')
    employee_languages = relationship('EmployeeLanguage', back_populates='employee', cascade='all, delete, delete-orphan')
    
    def to_dict(self):
        data = {
            'employement_number' : self.employement_number if self.employement_number else '',
            'first_name' : self.first_name if self.first_name else '',
            'middle_name' : self.middle_name if self.middle_name else '',
            'last_name' : self.last_name if self.last_name else '',
            'address_one' : self.address_one if self.address_one else '',
            'contact_number' : self.contact_number if self.contact_number else '',
            'country' : self.country if self.country else '',
            'id' : self.id if self.id else '',
            'fullname' : self.first_name + ' ' + self.last_name,
            'current_sex' : self.current_sex if self.current_sex else '',
            'sex_at_birth' : self.sex_at_birth if self.sex_at_birth else ''
        }
        return data
    adict = lambda self : vars(self)

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
# 
class EmployeeRelativeType(Base):
    __tablename__ = 'emp_relative_types'
    
    id = Column(Integer, Sequence('emp_rel_id'), primary_key=True)
    name = Column(String(50), nullable=False)
    display_name = Column(String(50), nullable=False)
    code = Column(String(30))
    del_flag = Column(Boolean, default=False)

    def to_dict(self):
        return {
            'id' : self.id,
            'name' : self.display_name if self.display_name else '',
            'code' : self.code if self.code else '',
            'del_flag' : self.del_flag
        }

class EmployeeRelative(Base):
    __tablename__ = 'emp_relatives'

    id = Column(Integer, Sequence('emp_rel'), primary_key=True)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50))
    last_name = Column(String(50))
    address_one = Column(String(50))
    address_two = Column(String(50))
    country = Column(String(50))
    contact_number = Column(String(20))
    email = Column(String(50))
    del_flag = Column(Boolean, default=False)
    approved = Column(Boolean, default=False)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee_type = Column(String(50))
    employee = relationship('Employee', back_populates='relatives')

    _val_mapper = lambda self, val : val if val is not None else ''
    to_dict = lambda self : {key: self._val_mapper(val) for key, val in vars(self).items()\
                             if not str(key).startswith('_')}

class EmployementHistory(Base):
    __tablename__ = 'emp_histories'

    id = Column(Integer, Sequence('emp_his_id'), primary_key=True)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    employer_name = Column(String(50))
    position = Column(String(50))
    reason_leaving = Column(String(50))
    description = Column(String(100))
    del_flag = Column(Boolean, default=False)
    approved = Column(Boolean, default=False)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    
    employee = relationship('Employee', back_populates='emp_histories')
    
    _val_mapper = lambda self, val : str(val) if val is not None else ''
    to_dict = lambda self : {key : self._val_mapper(val) for key, val in vars(self).items()\
                             if not str(key).startswith('_')}


class EmployeeReference(Base):
    __tablename__ = 'emp_references'

    id = Column(Integer, Sequence('emp_ref_id'), primary_key=True)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50))
    last_name = Column(String(50))
    company = Column(String(50))
    email = Column(String(50))
    address_one = Column(String(50))
    address_two = Column(String(50))
    contact_number = Column(String(20))
    country = Column(String(50))
    del_flag = Column(Boolean, default=False)
    description = Column(String(100))

    approved = Column(Boolean, default=False)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    
    employee = relationship('Employee', back_populates='emp_referenceses')

    _val_mapper = lambda self, item : item if item is not None else ''
    to_dict = lambda self : {key : self._val_mapper(val) for key, val
                             in vars(self).items() if not str(key).startswith('_')}


class EmployeeBenifitType(Base):
    __tablename__ = 'emp_benifit_types'
    
    id = Column(Integer, Sequence('emp_rel_id'), primary_key=True)
    name = Column(String(50), nullable=False)
    display_name = Column(String(50), nullable=False)
    code = Column(String(30))
    del_flag = Column(Boolean, default=False)

    def to_dict(self):
        return {
            'id' : self.id,
            'name' : self.display_name if self.display_name else '',
            'code' : self.code if self.code else '',
            'del_flag' : self.del_flag
        }

class EmployeeBenifit(Base):
    __tablename__ = 'emp_benifits'

    id = Column(Integer, Sequence('emp_ben_id'), primary_key=True)
    benifit_type = Column(String(50), nullable=False)
    amount = Column(String(10))
    date = Column(DateTime)
    comment = Column(String(100))
    approved = Column(Boolean, default=False)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    del_flag = Column(Boolean, default=False) 
    employee = relationship('Employee', back_populates='emp_benifits')

    _val_mapper = lambda self, item : item if item is not None else ''
    to_dict = lambda self : {key : self._val_mapper(val) for key, val in vars(self).items()
                            if not str(key).startswith('_')}

class EmployeeDisciplinaryType(Base):
    __tablename__ = 'emp_disciplinary_types'
    
    id = Column(Integer, Sequence('emp_distype_id'), primary_key=True)
    name = Column(String(50), nullable=False)
    display_name = Column(String(50), nullable=False)
    code = Column(String(30))
    del_flag = Column(Boolean, default=False)
    
    def to_dict(self):
        return {
            'id' : self.id,
            'name' : self.display_name if self.display_name else '',
            'code' : self.code if self.code else '',
            'del_flag' : self.del_flag
        }

class EmployeeDisciplinary(Base):
    __tablename__ = 'emp_disciplinary'
    
    id = Column(Integer, Sequence('emp_dis_id'), primary_key=True)
    disciplinary_type = Column(String(50), nullable=False)
    date = Column(DateTime)
    description = Column(String(200))
    approved = Column(Boolean, default=False)
    del_flag = Column(Boolean, default=False)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship('Employee', back_populates='emp_disciplinaries')

    _val_mapper = lambda self, item : item if item is not None else ''
    to_dict = lambda self : {key : self._val_mapper(val) for key, val in vars(self).items()
                            if not str(key).startswith('_')}

class EmployeeAppraisalType(Base):
    __tablename__ = 'emp_appraisal_types'
    
    id = Column(Integer, Sequence('emp_appraisaltype_id'), primary_key=True)
    name = Column(String(50), nullable=False)
    display_name = Column(String(50), nullable=False)
    code = Column(String(30))
    del_flag = Column(Boolean, default=False)

    def to_dict(self):
        return {
            'id' : self.id,
            'name' : self.display_name if self.display_name else '',
            'code' : self.code if self.code else '',
            'del_flag' : self.del_flag
        }

class EmployeeAppraisal(Base):
    __tablename__ = 'emp_appraisals'
    
    id = Column(Integer, Sequence('emp_appraisal_id'), primary_key=True)
    appraisal_type = Column(String(50), nullable=False)
    date = Column(DateTime)
    department = Column(String(50))
    comment = Column(String(50))
    approved = Column(Boolean, default=False)
    del_flag = Column(Boolean, default=False)
    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship('Employee', back_populates='emp_appraisals')
    
    _val_mapper = lambda self, item : item if item is not None else ''
    to_dict = lambda self : {key : self._val_mapper(val) for key, val in vars(self).items()
                            if not str(key).startswith('_')}

class Qualification(Base):
    __tablename__ = 'qualifications'

    id = Column(Integer, Sequence('qual_id'), primary_key=True)
    qualification_name_id = Column(Integer, ForeignKey('qualificationnames.id'))
    institute_name = Column(String(50))
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
    qualification_name = relationship('QualificationName', back_populates='qualifications')

class QualificationName(Base):
    __tablename__ = 'qualificationnames'
    id = Column(Integer, Sequence('qualification_name_id'), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    qualifications = relationship('Qualification', back_populates='qualification_name', cascade='all, delete, delete-orphan')

    _val_mapper = lambda self, item : item if item else ''
    to_dict = lambda self: {
        key: self._val_mapper(val) for key, val in vars(self).items() if not key.startswith('_')
    }


class Certification(Base):
    __tablename__ = 'certifications'

    id = Column(Integer, Sequence('cert_id'), primary_key=True)
    registration_number = Column(String(40), nullable=False, unique=True)
    regulatory_body_name_id = Column(Integer, ForeignKey('registrationbodynames.id'))
    issue_data = Column(Date)
    regulatory_body_address_one = Column(String(40))
    regulatory_body_address_two = Column(String(40))
    regulatory_body_address_three = Column(String(40))
    regulatory_body_address_country = Column(String(50))

    registration_type_name_id = Column(Integer, ForeignKey('registrationtypenames.id'))
    
    last_renewal_date = Column(Date)
    expiry_date = Column(Date)
    del_flag = Column(Boolean, default=False)
    
    employee_id = Column(Integer, ForeignKey('employees.id'))
    #relationship
    employee = relationship('Employee', back_populates='certifications')
    registration_type_name  = relationship('RegistrationTypeName', back_populates='certifications')
    registration_body_name = relationship('RegistrationBodyName', back_populates='certifications')

class RegistrationTypeName(Base):
    __tablename__ = 'registrationtypenames'
    id = Column(Integer, Sequence('registration_type_id'), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    certifications = relationship('Certification', back_populates='registration_type_name', cascade='all, delete, delete-orphan')

    _val_mapper = lambda self, item : item if item else ''
    to_dict = lambda self: {
        key: self._val_mapper(val) for key, val in vars(self).items() if not key.startswith('_')
    }

class RegistrationBodyName(Base):
    __tablename__ = 'registrationbodynames'

    id = Column(Integer, Sequence('registration_body_id'), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    certifications = relationship('Certification', back_populates='registration_body_name', cascade='all, delete, delete-orphan')

    _val_mapper = lambda self, item : item if item else ''
    to_dict = lambda self: {
        key: self._val_mapper(val) for key, val in vars(self).items() if not key.startswith('_')
    }

class Training(Base):
    __tablename__ = 'trainings'

    id = Column(Integer, Sequence('t_id'), primary_key=True)
    training_id = Column(Integer, ForeignKey('trainingsnames.id'))
    organizer_id = Column(Integer, ForeignKey('organizernames.id'))
    funding_source = Column(String(50))
    duration = Column(String(30))
    
    cost = Column(String(10))
    city = Column(String(50))
    state = Column(String(50))
    province = Column(String(50))
    country = Column(String(50))
    start_date = Column(Date)
    end_date = Column(Date)
    del_flag = Column(Boolean, default=False)
    institute_id = Column(Integer, ForeignKey('institutes.id'))
    employee_id = Column(Integer, ForeignKey('employees.id'))
    employee = relationship('Employee', back_populates='trainings')
    
    institute = relationship('Institute', back_populates='trainings')
    training_name = relationship('TrainingName', back_populates='trainings')
    organizer_name = relationship('OrganizerName', back_populates='trainings')

class TrainingName(Base):
    __tablename__ = 'trainingsnames'
    id = Column(Integer, Sequence('trainingnameid'), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    trainings = relationship('Training', back_populates='training_name', cascade='all, delete, delete-orphan')

    _val_mapper = lambda self, item : item if item else ''
    to_dict = lambda self: {
        key: self._val_mapper(val) for key, val in vars(self).items() if not key.startswith('_')
    }

class OrganizerName(Base):
    __tablename__ = 'organizernames'
    id = Column(Integer, Sequence('organizernamesid'), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    trainings = relationship('Training', back_populates='organizer_name', cascade='all, delete, delete-orphan')

    _val_mapper = lambda self, item : item if item else ''
    to_dict = lambda self: {
        key: self._val_mapper(val) for key, val in vars(self).items() if not key.startswith('_')
    }



class Institute(Base):
    __tablename__ = 'institutes'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False, unique=True)
    trainings = relationship('Training', back_populates='institute', cascade='all, delete, delete-orphan')

    _val_mapper = lambda self, item : item if item else ''
    to_dict = lambda self: {
        key: self._val_mapper(val) for key, val in vars(self).items() if not key.startswith('_')
    }

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




class EmployeeAddress(Base):
    __tablename__ = 'employeeaddresses'

    id = Column(Integer, Sequence('emp_address_id'), primary_key=True)
    perm_street_addr = Column(String(32))
    perm_city_town = Column(String(32))
    perm_postal_code = Column(String(32))
    perm_country_code = Column(String(32))

    business_street_addr = Column(String(32))
    business_city_town = Column(String(32))
    business_postal_code = Column(String(32))
    business_country_code = Column(String(32))
    
    residential_street_addr = Column(String(32))
    residential_city_addr = Column(String(32))
    residential_postal_code = Column(String(32))
    residential_country_code = Column(String(32))

    professional_email_address = Column(String(50))
    personal_email_address = Column(String(50))

    country_birth = Column(String(20))
    country_citizenship_at_birth = Column(String(20))
    country_present_citizenship = Column(String(20))
    multiple_citizenship = Column(Boolean, default=False)
    country_second_citizenship = Column(String(20))

    employee_id = Column(Integer, ForeignKey('employees.id'), unique=True, nullable=False)
    employee = relationship('Employee', back_populates='employee_address')

    _val_mapper = lambda self, item : item if item else ''
    to_dict = lambda self: {
        key: self._val_mapper(val) for key, val in vars(self).items() if not key.startswith('_')
    }


class EmployeeEducation(Base):
    __tablename__ = 'employeeeducations'

    id = Column(Integer, Sequence('emplpoyeeeducation_id'), primary_key=True)

    institute_name = Column(String(50))
    country = Column(String(20))
    city_town = Column(String(20))
    degree = Column(String(50))
    certificate = Column(String(50))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    major_study = Column(String(50))
    minor_study = Column(String(50))

    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    employee = relationship('Employee', back_populates='employee_educations')

    _val_mapper = lambda self, item : item if item else ''
    to_dict = lambda self: {key : self._val_mapper(val) for key, val in vars(self).items()
                                                if not key.startswith('_')}


class Language(Base):
    __tablename__ = 'languages'

    id = Column(Integer, Sequence('language_id'), primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    employee_languages = relationship('EmployeeLanguage', back_populates='language', cascade='all, delete, delete-orphan')

    _val_mapper = lambda self, item: item if item else ''
    to_dict = lambda self: {key: self._val_mapper(val) for key, val in vars(self).items()
                                                                if not key.startswith('_')}

class EmployeeLanguage(Base):
    __tablename__ = 'employeelanguages'

    id = Column(Integer, Sequence('emplang_id'), primary_key=True)
    read = Column(Boolean, default=False)
    write = Column(Boolean, default=False)
    speak = Column(Boolean, default=False)

    language_id  = Column(Integer, ForeignKey('languages.id'), nullable=False)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)

    employee = relationship('Employee', back_populates='employee_languages')
    language = relationship('Language', back_populates= 'employee_languages')

    def to_dict(self):
        return {
            'id' : self.id,
            'read' : self.read,
            'write': self.write,
            'speak': self.speak,
            'employee' : self.employee.first_name + ' ' + self.employee.last_name,
            'language' : self.language.name if self.language else '',
            'language_id' : self.language_id if self.language_id else '',
            'employee_id' : self.employee_id if self.employee_id else ''
        }

