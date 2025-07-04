from fastapi import APIRouter
from models.folio_model import Folio
from services import user_service
from services.folio_service import FolioService
from services.user_service import UserService
from models.user_model import  User



routes=APIRouter(prefix="/user", tags=["User"])
routes_f=APIRouter(prefix="/folio", tags=["Folio"])

user_service=UserService()
User_model=User
folio_service=FolioService()
Folio_model=Folio

@routes.get("/get-users/")
async def get_all_users(): 
        result= await user_service.get_users()
        return result

@routes.get("/get-users/{user_id}")
async def get_user(user_id: int):
        return await user_service.get_user_by_id(user_id)
        

@routes.post("/create-user/")
async def create_User(user: User):
        return await user_service.create_users(user)       

@routes.patch("/change-password/")
async def change_password(id: str,new_password: str):
        return await user_service.change_password(id, new_password)

@routes.patch("/inactivate/{user_id}")
async def inactivate_user(user_id: int):
    return await user_service.inactivate_user(user_id)

@routes.patch("/change-status/{user_id}")
async def change_user_status(user_id: int):
      return await user_service.toggle_user_status(user_id)

@routes.put("/update-user/{user_id}")
async def update_user(user_id: int, user_data: User):
    return await user_service.update_user(user_id, user_data)


@routes_f.get("/get-folios/")
async def get_all_folios():
        return await folio_service.get_folio()

@routes_f.get("/get-folio/{id_folio}")
async def get_folio(id_folio: int):
        return await folio_service.get_folio(id_folio)
        

@routes_f.post("/create-folio/")
async def create_folio(folio: Folio):
        return await folio_service.create_folio(folio) 


        