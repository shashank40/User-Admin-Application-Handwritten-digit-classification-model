import logging

import uvicorn
import secrets
from fastapi import FastAPI, UploadFile, File, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from model__prediction_and_evaluation.prediction import run_example

from auth.schemas import AuthDetails, Email
from auth.firebase.login.login import log_in_with_email_and_password
from auth.firebase.signup.signup import sign_in_with_email_and_password
from auth.firebase.change_password.changePass import SendResetEmail

app = FastAPI(docs_url=None)

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
def logPage(request: Request):
    return templates.TemplateResponse("forgotPass.html", {"request": request})

@app.post('/new-pass')
def login(request: Request, email: Email =  Depends(Email.as_form)):
    message, status = SendResetEmail(email.email)
    return templates.TemplateResponse("falseInput.html", {"request": request, "value1": message})

@app.get('/signup', response_class = HTMLResponse)
def logPage(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post('/signup', status_code=201)
def register(request: Request, auth_details: AuthDetails =  Depends(AuthDetails.as_form)):
    message, status = sign_in_with_email_and_password(auth_details.email, auth_details.password)

    if status == False:
        logging.exception(message)
        return templates.TemplateResponse("falseInput.html", {"request": request, "value1": message})
    
    return templates.TemplateResponse("signupConfirmation.html", {"request": request,  "value1" : auth_details.email})

@app.get('/prediction', response_class = HTMLResponse)
def predictPage(request: Request):
    return templates.TemplateResponse("predict.html", {"request": request})

@app.post('/prediction')
async def get_digit(request: Request, file: UploadFile = File(...)):
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
def predictPage(request: Request):
    return templates.TemplateResponse("uploadUpdatedModel.html", {"request": request})

@app.post('/upload-updated-model')
async def get_digit(request: Request, file: UploadFile = File(...)):
    value = ''
    if not file:
        value = 'No file uploaded'
    elif file.filename.endswith('.h5'):
        # storing file in firebase bucket
        value = 'Model uploaded successfully'
    else:
        value = 'Invalid file type'
    return templates.TemplateResponse("falseInput.html", {"request": request, "value1": value})

@app.post('/base-model')
async def get_digit(request: Request):
    return {'message': 'Base model is being used'}

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=4000, debug=True)
