from pydantic import BaseModel, EmailStr
from datetime import datetime,time as Time, date
from typing import Dict, Optional, Union
from enum import Enum

from fastapi import UploadFile
from fastapi import Form, File
from typing import List


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class BudgetCreate(BaseModel):
    month: int
    total_budget: float

class CategoryCreate(BaseModel):
    name: str
    amount: float

class ExpenseCreate(BaseModel):
    category: str
    amount: float
    
class CategoryBase(BaseModel):
    name: str
    amount: float

class CategoryCreate(CategoryBase):
    pass

class ExpenditureCreate(BaseModel):
    amount: float

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int