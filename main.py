import logging

import uvicorn
import secrets
import requests

from fastapi import FastAPI, UploadFile, File, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from model__prediction_and_evaluation.prediction import run_example

from auth.schemas import AuthDetails, Email, ClientUpload
from auth.firebase.login.login import log_in_with_email_and_password
from auth.firebase.signup.signup import sign_in_with_email_and_password
from auth.firebase.change_password.changePass import SendResetEmail
from auth.base64_encode.encode import encode
from auth.firebase.admin_base_upload.admin_base_upload import baseUpload
from auth.firebase.client_model_upload.model_upload import uploadClientModel
from auth.firebase.all_client_model_download.client_model_download import downloadClientModels, cleanFolder

app = FastAPI()

templates = Jinja2Templates(directory="./templates")
app.mount("/static", StaticFiles(directory="./static"), name="static")


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
    
    message, status = log_in_with_email_and_password(auth_details.email, auth_details.password)
    
    if status == False:
        logging.exception(message)
        return templates.TemplateResponse("falseInput.html", {"request": request, "value1": message})

    logging.info(message)
    return templates.TemplateResponse("token.html", {"request": request, "value1": message, "email": auth_details.email})

@app.get('/new-pass', response_class = HTMLResponse)
def newPassGet(request: Request):
    return templates.TemplateResponse("forgotPass.html", {"request": request})

@app.post('/new-pass')
def newPassPost(request: Request, email: Email =  Depends(Email.as_form)):
    message, status = SendResetEmail(email.email)
    return templates.TemplateResponse("falseInput.html", {"request": request, "value1": message})

@app.get('/signup', response_class = HTMLResponse)
def registerGet(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post('/signup', status_code=201)
def registerPost(request: Request, auth_details: AuthDetails =  Depends(AuthDetails.as_form)):
    message, status = sign_in_with_email_and_password(auth_details.email, auth_details.password)

    if status == False:
        logging.exception(message)
        return templates.TemplateResponse("falseInput.html", {"request": request, "value1": message})
    
    return templates.TemplateResponse("signupConfirmation.html", {"request": request,  "value1" : auth_details.email})

@app.get('/prediction', response_class = HTMLResponse)
def predictPageGet(request: Request):
    return templates.TemplateResponse("predict.html", {"request": request})

@app.post('/prediction')
async def predictPagePost(request: Request, file: UploadFile = File(...)):
    value = ''
    if not file:
        value = 'No file uploaded'
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
        value = f'Predicted number is : {dig}'
    else:
        value = 'Invalid Image type'
    return templates.TemplateResponse("falseInput.html", {"request": request, "value1": value})


@app.get('/upload-updated-model', response_class = HTMLResponse)
def uploadUpdatedModelGet(request: Request):
    return templates.TemplateResponse("uploadUpdatedModel.html", {"request": request})

@app.post('/upload-updated-model')
async def uploadUpdatedModelPost(request: Request, clientUpload: ClientUpload = Depends(ClientUpload.as_form)):
    value = ''
    if not clientUpload.file:
        value = 'No file uploaded'
    elif clientUpload.file.filename.endswith('.h5'):
        message, status = await uploadClientModel(clientUpload.email, clientUpload.idToken, clientUpload.file)
        value = message
    else:
        value = 'Invalid file type'
    return templates.TemplateResponse("falseInput.html", {"request": request, "value1": value})

@app.post('/admin')
async def adminBaseUpload(request: Request, token: str):
    if(encode() == token):
        await baseUpload()
        return {'message': 'Base model uploaded successfully'}
    else: 
        return {'message': 'Not authenticated to access this endpoint'}

@app.get('/admin/download-all-client-models')
async def adminBaseUpload(request: Request, token: str):
    if(encode() == token):
        message, status = await downloadClientModels()
        if status:
            # code doing averaging of models called here
            await cleanFolder()
            return {'message': 'Downloaded successfully'}
        else:
            return {'message': message}
    else: 
        return {'message': 'Not authenticated to access this endpoint'}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=4000, debug=True)
