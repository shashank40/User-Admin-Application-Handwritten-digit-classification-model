from typing import Union

import uvicorn
import secrets
from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from model__prediction_and_evaluation.prediction import run_example
from pydantic import BaseModel

from auth.auth import AuthHandler
from auth.schemas import AuthDetails

app = FastAPI()

auth_handler = AuthHandler()
users = []

class value(BaseModel):
    digit : int


@app.get('/')
def register():
    return {'message': 'Head on to endpoint/docs to get all apis'}

@app.post('/register', status_code=201)
def register(auth_details: AuthDetails):
    if any(x['username'] == auth_details.username for x in users):
        raise HTTPException(status_code=400, detail='Username is taken')
    hashed_password = auth_handler.get_password_hash(auth_details.password)
    users.append({
        'username': auth_details.username,
        'password': hashed_password    
    })
    return {'message': 'user created with for given user. Save user and password for future'
            ,'username': auth_details.username,}

@app.post('/login')
def login(auth_details: AuthDetails):
    user = None
    for x in users:
        if x['username'] == auth_details.username:
            user = x
            break
    
    if (user is None) or (not auth_handler.verify_password(auth_details.password, user['password'])):
        raise HTTPException(status_code=401, detail='Invalid username and/or password')
    token = auth_handler.encode_token(user['username'])
    return {'message': 'Token created for the user. Save it for authorization while api utilization'
            ,'token': token }  #returns a token that is valid for sometime(time can be changed in auth.py). This token is to be used in header for auth to use the api
    # use this token as auth token with bearer

@app.post('/prediction')
async def get_digit(username=Depends(auth_handler.auth_wrapper), file: Union[UploadFile, None] = File(...)):
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
