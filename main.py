from typing import Union

import uvicorn
import secrets
from fastapi import FastAPI, UploadFile, File
from model__prediction_and_evaluation.prediction import run_example
from pydantic import BaseModel

app = FastAPI()

class value(BaseModel):
    digit : int


@app.post('/prediction')
async def get_digit(file: Union[UploadFile, None] = File(...)):
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
