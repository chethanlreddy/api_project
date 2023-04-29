from fastapi import Depends, FastAPI, Response, status, HTTPException, APIRouter, File,UploadFile
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import shutil
from .. import schemas

from .. import models, database, schemas, utils, oauth2
router = APIRouter(
    prefix='/fileinsert',
    tags=['upload file']
)
@router.post('/',status_code=status.HTTP_201_CREATED)
def insert_image(file_in : UploadFile = File(...)):
    with open(f'{file_in.filename}', 'wb') as buffer:
        shutil.copyfileobj(file_in.file,buffer)
    return {'message' : file_in.filename}