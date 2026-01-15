from pydantic import BaseModel, Field, field_validator
from typing import List, Optional
from datetime import date

class Item(BaseModel):
    name : str
    fee: Optional[float] = 0

class Appointment(BaseModel):
    appointment : int
    consultation : float = Field(..., ge=0)
    medicines : Optional[List[Item]] = None
    therapies : List[Item] = Field(default_factory=list)

class Fee(BaseModel):
    data: List[Appointment] = Field(default_factory=list)

class Patient(BaseModel):
    name: str = Field(...,min_length=1)
    age: int = Field(..., ge=0, le=120)
    gender : str
    dob : date
    phone : str = Field(..., max_length=10, min_length=10,default_factory=None)
    address : Optional[str] = None
    first_appointment: date
    followup_date: Optional[date] = None
    total_followups: int = Field(0, ge=0)
    major_complain: Optional[str] = None
    fees : Fee
