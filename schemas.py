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

class MonthlyBudgetResponse(BaseModel):
    id: int
    month: int
    year: int
    budget: float
    balance: float

    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    balance: float
    monthly_budget: Optional[List[MonthlyBudgetResponse]] = []


class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass


class CategoryResponse(CategoryBase):
    id: int
    budget: float

    class Config:
        orm_mode = True



class Category(CategoryBase):
    id: int
    budget: float
    user_id: int
    remaining_budget: float  # Added field

    class Config:
        orm_mode = True

class CategoryBudget(BaseModel):
    id: int
    name: str
    budget: float
    user_id: int
    remaining_budget: float

    class Config:
        orm_mode = True


class ExpenseBase(BaseModel):
    amount: float


class ExpenseCreate(ExpenseBase):
    pass


class ExpenseResponse(ExpenseBase):
    id: int
    category_id: int

    class Config:
        orm_mode = True


class MonthlyBudget(BaseModel):
    budget: float



    
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: int





class MonthlyBudgetBase(BaseModel):
    month: int
    year: int
    budget: float


class MonthlyBudgetCreate(MonthlyBudgetBase):
    pass






class ExpenseCreate(ExpenseBase):
    pass


class Expense(ExpenseBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True