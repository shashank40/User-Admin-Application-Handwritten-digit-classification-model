from typing import Union

from pydantic import BaseModel
from fastapi import Form
from fastapi import UploadFile, Form


class AuthDetails(BaseModel):
    email: str
    password: str

    @classmethod
    def as_form(
        cls,
        email: str = Form(...),
        password: str = Form(...),
    ):
        return cls(
            email=email,
            password=password,
        )
    
class Email(BaseModel):
    email: str

    @classmethod
    def as_form(
        cls,
        email: str = Form(...),
    ):
        return cls(
            email=email,
        )