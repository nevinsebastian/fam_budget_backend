from fastapi import status, HTTPException,Depends, APIRouter
from sqlalchemy.orm import Session
import models, schemas, utils
from database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)

def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if user.password != user.confirm_password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Passwords do not match")
    
    hashed_password = utils.hash(user.password)
    user_dict = user.dict()
    user_dict.pop("confirm_password")  
    user_dict["password"] = hashed_password
    
    new_user = models.User(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user