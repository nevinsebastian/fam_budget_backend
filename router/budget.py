from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models, schemas, utils
from database import get_db
from datetime import datetime
from oauth2 import get_current_user
from sqlalchemy import func  # Add this line
from typing import List

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

@router.get("/monthly_budget", response_model=List[schemas.MonthlyBudgetResponse], status_code=status.HTTP_200_OK)
def get_user_monthly_budget(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    year = 2024  # Hardcoded year

    # Fetch monthly budgets for all months of the specified year
    monthly_budgets = db.query(models.MonthlyBudget).filter(models.MonthlyBudget.user_id == current_user.id, models.MonthlyBudget.year == year).order_by(models.MonthlyBudget.month).all()

    monthly_budget_responses = []

    # Loop through each month of the year
    for month in range(1, 13):
        # Check if budget is set for the current month
        monthly_budget = next((budget for budget in monthly_budgets if budget.month == month), None)
        
        # If budget is not set for the current month, set budget to 0
        if not monthly_budget:
            initial_budget = 0.0
            budget_id = None
        else:
            total_category_budget = db.query(func.sum(models.Category.budget)).join(models.User).filter(models.User.id == current_user.id).scalar()
            initial_budget = monthly_budget.budget + (total_category_budget or 0.0)
            budget_id = monthly_budget.id

        total_expenses = db.query(func.sum(models.Expense.amount)).join(models.User).filter(models.User.id == current_user.id).scalar() or 0.0
        # If the initial_budget is 0, then the balance should also be 0
        balance = initial_budget if initial_budget == 0 else (initial_budget - total_expenses)

        monthly_budget_response = schemas.MonthlyBudgetResponse(
            id=budget_id,
            month=month,
            year=year,
            budget=initial_budget,
            balance=balance
        )
        monthly_budget_responses.append(monthly_budget_response)
    
    return monthly_budget_responses
