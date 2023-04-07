from typing import Union
import logging

import uvicorn
import secrets
from fastapi import FastAPI, UploadFile, File, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from model__prediction_and_evaluation.prediction import run_example
from pydantic import BaseModel

from auth.auth import AuthHandler
from auth.schemas import AuthDetails

app = FastAPI()

templates = Jinja2Templates(directory="./web/webapp")
app.mount("/web/static", StaticFiles(directory="./web/static"), name="static")

auth_handler = AuthHandler()
users = []

class value(BaseModel):
    digit : int

@app.get('/')
def landingPage():
    url = app.url_path_for("login")
    response = RedirectResponse(url=url)
    return response


@app.get('/login', response_class = HTMLResponse)
def logPage(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post('/login')
def login(request: Request, auth_details: AuthDetails =  Depends(AuthDetails.as_form)):
    user = None
    for x in users:
        if x['email'] == auth_details.email:
            user = x
            break
    
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        logging.exception('Invalid email and/or password')
        invalid = "Invalid email and/or password."
        return templates.TemplateResponse("falseInput.html", {"request": request, "value1": invalid})
    token = auth_handler.encode_token(user['email'])

    logging.info('Auth token : ' + token)
    return templates.TemplateResponse("token.html", {"request": request, "value1": token, "email": auth_details.email})
      #returns a token that is valid for sometime(time can be changed in auth.py). This token is to be used in header for auth to use the api
    # use this token as auth token with bearer

@app.get('/new-pass', response_class = HTMLResponse)
def logPage(request: Request):
    return templates.TemplateResponse("forgotPass.html", {"request": request})

@app.post('/new-pass')
def login(request: Request, email: str =  Form(...)):
    user = None
    for x in users:
        if x['email'] == email:
            user = x
            break
    
    if (user is None) :
        logging.exception('Invalid email')
        invalid = "Invalid email"
        return templates.TemplateResponse("falseInput.html", {"request": request, "value1": invalid})

    invalid = "Password reset link sent to your email"
    return templates.TemplateResponse("falseInput.html", {"request": request, "value1": invalid})

@app.get('/signup', response_class = HTMLResponse)
def logPage(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post('/signup', status_code=201)
def register(request: Request, auth_details: AuthDetails =  Depends(AuthDetails.as_form)):
    if any(x['email'] == auth_details.email for x in users):
        logging.exception('Email is already taken')
        invalid = "Email is already taken."
        return templates.TemplateResponse("falseInput.html", {"request": request, "value1": invalid})

    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.append({
        'email': auth_details.email,
        'password': hashed_password    
    })
    return templates.TemplateResponse("signupConfirmation.html", {"request": request,  "value1" : auth_details.email})

@app.post('/prediction')
async def get_digit(email=Depends(auth_handler.auth_wrapper), file: Union[UploadFile, None] = File(...)):
    if not file:
        return {'message': 'no file uploaded'}
    elif file.content_type == 'image/png':
        # storing file at a place
        file_path = './static/'
        new_file_name = secrets.token_hex(10)+".png"
        generated_name = file_path + new_file_name
        file_content = await file.read()

        with open(generated_name, "wb") as file:
            file.write(file_content)
            file.close()
        dig: int = run_example(new_file_name)
        print(dig)
        return value(digit= dig)
    else:
        return {'message': 'Invalid Image type'}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=4000, debug=True)
