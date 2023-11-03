from fastapi import APIRouter, Depends, HTTPException,status,Path
from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session 
from models import Contacts
from database import  SessionLocal
from .auth import get_current_user


router =APIRouter(
    prefix='/admin',
    tags=['admin']
)



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]
user_dependency = Annotated[dict,Depends(get_current_user)]



@router.get('/contacts',status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db:db_dependency):
    if user is None or user.get('user_role') !='admin':
        raise HTTPException(status_code=401,detail='Authentication is Failed')
    return db.query(Contacts).all()

@router.delete('/contacts/{contacts_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_contact(user: user_dependency, db:db_dependency,
                         contacts_id:int = Path(gt=0)):
     if user is None or user.get('user_role')!='admin':
        raise HTTPException(status_code=401,detail='Authentication Failed')
     
     contacts_model = db.query(Contacts).filter(Contacts.id==contacts_id).first()
     if contacts_model is None:
         raise HTTPException(status_code=404,detail='contact not found')
     db.query(Contacts).filter(Contacts.id == contacts_id).delete()
     db.commit()
    

         