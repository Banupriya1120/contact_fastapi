from fastapi import FastAPI
import models
from database import engine
from routers import auth,contacts,admin,users

app =FastAPI()

models.base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(contacts.router)
app.include_router(admin.router)
app.include_router(users.router)






