from pydantic import BaseModel, EmailStr

class usercreate(BaseModel):
    email: EmailStr #verif mail
    password: str

class userresponse(BaseModel):
    id: int
    email: EmailStr

class Config:
    from_attributes = True 