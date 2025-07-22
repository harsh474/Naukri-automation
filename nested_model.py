from typing import List, Optional
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    postal_code: str

class User(BaseModel):
    id: int
    name: str
    address: Address

class Comment(BaseModel):
    id: int
    content: str
    replies: Optional[List['Comment']] = None

Comment.model_rebuild()


address = Address(
    street="Delhi Highway", 
    city="Gurgaon",
    postal_code="12001"
)
user  = User(  
             id = 1, 
             name = "harsh", 
             address= address
        ) 
comment = Comment(  
              id=1, 
              content="Our first content" , 
              replies=[Comment(id=2,content="our 2nd comment"), Comment(id=3,content='our 3rd comment')]
            ) 


class Lesson(BaseModel): 
    id:int 
    name:str

class Module(BaseModel): 
    id:int
    name:str
    lesson:List[Lesson]

class Course(BaseModel): 
    id:int
    name:str
    module:List[Module]

lesson = Lesson(id=1,name="base_employee") 
module = Module(id=1,name="Employee",lesson=[lesson,Lesson(id=2,name="base2_emloyee")]) 
course = Course(id=1,name="Hr",module=[module])
print("lesson\n",lesson)
print("module\n",module)
print("course\n",course)
