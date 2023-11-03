from fastapi import APIRouter, Depends, HTTPException,status,Path
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session 
from models import Contacts
from database import  SessionLocal
from .auth import get_current_user


router =APIRouter()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]


class ContactsRequest(BaseModel):
    first_name:str = Field(min_length=2)
    last_name:str = Field(min_length=2)
    country_code:str = Field (max_length=4)
    phone_number: str = Field(max_length=10)



@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency,db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Contacts).filter(Contacts.owner_id==user.get('id')).all()



@router.get("/contacts/{contacts_id}", status_code=status.HTTP_200_OK)
async def read_contacts(user: user_dependency,db: db_dependency,
                        contacts_id: int = Path(gt=0) ):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    contacts_model = db.query(Contacts).filter(Contacts.id==contacts_id)\
        .filter(Contacts.owner_id==user.get('id')).first()
    if contacts_model is not None:
        return contacts_model
    raise HTTPException(status_code=404, detail='cobtact not exist')




@router.post("/contacts", status_code=status.HTTP_201_CREATED)
async def create_contacts(user: user_dependency, db: db_dependency,
                          contacts_request: ContactsRequest):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    contacts_model=Contacts(**contacts_request.model_dump(), owner_id=user.get('id'))
    db.add(contacts_model)
    db.commit()




@router.put("/contacts/{contacts_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_contacts(user: user_dependency,db:db_dependency,
                          contacts_request:ContactsRequest,
                          contacts_id : int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    contacts_model = db.query(Contacts).filter(Contacts.id==contacts_id).\
        filter(Contacts.owner_id==user.get('id')).first()



    contacts_model.first_name=contacts_request.first_name
    contacts_model.last_name=contacts_request.last_name
    contacts_model.country_code=contacts_request.country_code
    contacts_model.phone_number=contacts_request.phone_number
    db.add(contacts_model)
    db.commit()
    
        
@router.delete("/contacts/{contacts_id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_contacts(user: user_dependency,db:db_dependency,contacts_id : int = Path(gt=0)):

    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')

    contacts_model = db.query(Contacts).filter(Contacts.id==contacts_id)\
        .filter(Contacts.owner_id==user.get('id')).first()
    if contacts_model is  None:
        raise HTTPException(status_code=404, detail='contact not found')
    
    db.query(Contacts).filter(Contacts.id==contacts_id).filter(Contacts.owner_id==user.get('id')).delete()
    db.commit()