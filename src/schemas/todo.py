from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import date



class ContactSchema(BaseModel):
    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    email: EmailStr
    phone_number: str = Field(min_length=3, max_length=20)
    birthday: Optional[date]
    additional_data: Optional[date]


class ContactUpdateSchema(ContactSchema):
    pass


class ContactResponse(BaseModel):
    id: int = 1
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
    birthday: Optional[date]
    additional_data: Optional[date]

    class Config:
        from_attributes = True