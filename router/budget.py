from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models, schemas, utils
from database import get_db
from datetime import datetime
from oauth2 import get_current_user
from sqlalchemy import func  # Add this line


router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/set_budget", status_code=status.HTTP_200_OK)
def create_monthly_budget(
    budget: schemas.MonthlyBudgetCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):

    # Check if the total budget for all categories exceeds the user's total budget
    # total_category_budget = sum(cat.budget for cat in current_user.categories)
    # if total_category_budget + budget.budget > current_user.balance:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Total category budgets cannot exceed total budget")

    db_budget = models.MonthlyBudget(**budget.dict(), user_id=current_user.id)
    db.add(db_budget)
    db.commit()
    db.refresh(db_budget)
    return db_budget


@router.get("/monthly_budget", response_model=schemas.MonthlyBudgetResponse, status_code=status.HTTP_200_OK)
def get_user_monthly_budget(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    monthly_budget = db.query(models.MonthlyBudget).filter(models.MonthlyBudget.user_id == current_user.id).first()
    if not monthly_budget:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Monthly budget not found")
    
    total_category_budget = db.query(func.sum(models.Category.budget)).join(models.User).filter(models.User.id == current_user.id).scalar()
    initial_budget = monthly_budget.budget + (total_category_budget or 0.0)

    total_expenses = db.query(func.sum(models.Expense.amount)).join(models.User).filter(models.User.id == current_user.id).scalar()
    balance = initial_budget - (total_expenses or 0.0)

    monthly_budget_response = schemas.MonthlyBudgetResponse(
        id=monthly_budget.id,
        month=monthly_budget.month,
        year=monthly_budget.year,
        budget=initial_budget,
        balance=balance
    )
    return monthly_budget_response


