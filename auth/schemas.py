from typing import Union

from pydantic import BaseModel
from fastapi import Form
from fastapi import UploadFile, Form, File


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

class ClientUpload(BaseModel):
    email: str
    idToken: str
    file: UploadFile

    @classmethod
    def as_form(
        cls,
        email: str = Form(...),
        idToken: str = Form(...),
        file: UploadFile = Form(...),
    ):
        return cls(
            email=email,
            idToken=idToken,
            file=file,
        )
