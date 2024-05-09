from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models, schemas
from database import get_db
from typing import List
from oauth2 import get_current_user

router = APIRouter(
    prefix="/budgets",
    tags=['Budgets']
)

@router.post("/create")
def create_monthly_budget(budget_create: schemas.BudgetCreate, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    existing_budget = db.query(models.Budget).filter(models.Budget.month == budget_create.month, models.Budget.user_id == user_id).first()
    if existing_budget:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="A budget already exists for this month")

    new_budget = models.Budget(month=budget_create.month, total_budget=budget_create.total_budget, user_id=user_id)
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    return {"message": "Monthly budget created successfully", "budget_id": new_budget.id}

@router.post("/category/{budget_id}")
def add_category_to_budget(budget_id: int, category_create: schemas.CategoryCreate, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    db_budget = db.query(models.Budget).filter(models.Budget.id == budget_id, models.Budget.user_id == user_id).first()
    if not db_budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    
    new_category = models.Category(name=category_create.name, amount=category_create.amount, budget_id=budget_id, user_id=user_id)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return {"message": "Category added successfully", "category_id": new_category.id}

@router.post("/expenditure/{category_id}")
def add_expenditure_to_category(category_id: int, expenditure_create: schemas.ExpenditureCreate, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == category_id, models.Category.user_id == user_id).first()
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    db_budget = db_category.budget
    if expenditure_create.amount > db_category.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Expenditure amount exceeds category budget")
    
    new_expense = models.Expense(amount=expenditure_create.amount, category_id=category_id, budget_id=db_category.budget_id, user_id=user_id)
    db.add(new_expense)
    db.commit()
    
    # Update category and budget balances
    db_category.amount -= expenditure_create.amount
    db_budget.total_budget -= expenditure_create.amount
    db.commit()
    
    return {"message": "Expenditure added successfully"}

@router.get("/category/balance/{category_id}")
def get_category_balance(category_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    db_category = db.query(models.Category).filter(models.Category.id == category_id, models.Category.user_id == user_id).first()
    if not db_category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
    return {"category_balance": db_category.amount}

@router.get("/budget/balance/{budget_id}")
def get_budget_balance(budget_id: int, user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    db_budget = db.query(models.Budget).filter(models.Budget.id == budget_id, models.Budget.user_id == user_id).first()
    if not db_budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Budget not found")
    
    return {"budget_balance": db_budget.total_budget}
