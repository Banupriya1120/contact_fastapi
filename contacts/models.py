from database import base
from sqlalchemy import Column,Integer,String, Boolean,ForeignKey

class Users(base):
    __tablename__= 'users'
    id = Column(Integer, primary_key = True, index=True)
    email= Column(String, unique=True)
    username=Column(String, unique=True)
    first_name= Column(String)
    last_name =Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)



class Contacts(base):
    __tablename__='contacts'
    id = Column(Integer, primary_key = True, index=True)
    first_name=Column(String)
    last_name=Column(String)
    country_code=Column(String)
    phone_number=Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))


