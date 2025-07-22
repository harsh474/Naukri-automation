from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Union

class Employee(BaseModel): 
    id: int
    name: str = Field(default="Harsh Rajput", min_length=3, max_length=10)
    department: Optional[str] = Field(default="General") 
    salary: float = Field(gt=1000) 
    projects: List[Union[int, str, float]] 
    address: Dict[Union[str, int, float], Union[int, float]]
 
 
 