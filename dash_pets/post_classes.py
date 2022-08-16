from pydantic import BaseModel

class AddPet(BaseModel):
    pet_name:str
    pet_type:str
    pet_age:int
    pet_owner:str
    