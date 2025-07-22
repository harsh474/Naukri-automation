from sqlmodel import Session , SQLModel  
from sqlmodel import Field 


class User(SQLModel,table=True): 
    id :int = Field(primary_key=True)
    name:str 
    email:str 
    state:str   






   