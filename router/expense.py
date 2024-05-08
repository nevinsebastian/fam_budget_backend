from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
import models, schemas, utils
from database import get_db
from datetime import datetime
from oauth2 import get_current_user
from sqlalchemy import func
from typing import List
from sqlalchemy import desc



router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(
    category: schemas.CategoryCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Check if the total budget for all categories exceeds the user's monthly budget
    monthly_budget = db.query(models.MonthlyBudget).filter(models.MonthlyBudget.user_id == current_user.id).first()
    total_category_budget = db.query(func.sum(models.Category.budget)).filter(models.Category.user_id == current_user.id).scalar()
    
    if monthly_budget and total_category_budget is not None and total_category_budget + category.budget > monthly_budget.budget:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Total category budgets cannot exceed the user's monthly budget")

    db_category = models.Category(name=category.name, budget=category.budget, user_id=current_user.id)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)

    return db_category


@router.get("/categories", response_model=List[schemas.CategoryBudget])
def get_categories_budget(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    categories = (
        db.query(models.Category)
        .filter(models.Category.user_id == current_user.id)
        .all()
    )
    category_budgets = []
    for category in categories:
        total_expense = (
            db.query(func.sum(models.Expense.amount))
            .filter(models.Expense.category_id == category.id)
            .scalar() or 0
        )
        remaining_budget = category.budget - total_expense
        category_with_budget = schemas.CategoryBudget(
            id=category.id,
            name=category.name,
            budget=category.budget,
            user_id=category.user_id,
            remaining_budget=remaining_budget,
        )
        category_budgets.append(category_with_budget)
    return category_budgets




@router.get("/top_categories", response_model=List[schemas.CategoryBudget])
def get_top_categories(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    categories = (
        db.query(models.Category)
        .filter(models.Category.user_id == current_user.id)
        .all()
    )
    category_budgets = []
    for category in categories:
        total_expense = (
            db.query(func.sum(models.Expense.amount))
            .filter(models.Expense.category_id == category.id)
            .scalar() or 0
        )
        remaining_budget = category.budget - total_expense
        category_with_budget = schemas.CategoryBudget(
            id=category.id,
            name=category.name,
            budget=category.budget,
            user_id=category.user_id,
            remaining_budget=remaining_budget,
        )
        category_budgets.append(category_with_budget)
    
    # Sort the categories based on their spending
    sorted_categories = sorted(category_budgets, key=lambda x: x.budget - x.remaining_budget, reverse=True)
    # Return the top 4 categories
    return sorted_categories[:4]




@router.post("/expenses", status_code=status.HTTP_201_CREATED)
def create_expense(
    expense: schemas.ExpenseCreate,
    category_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    # Check if the category belongs to the current user
    category = db.query(models.Category).filter(models.Category.id == category_id, models.Category.user_id == current_user.id).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    # Check if the expense amount exceeds the category budget
    if expense.amount > category.budget:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Expense amount cannot exceed category budget")

    # Update category budget
    category.budget -= expense.amount
    db.commit()

    # Update user's total balance
    current_user.balance -= expense.amount
    db.commit()

    # Add expense
    db_expense = models.Expense(amount=expense.amount, category_id=category_id, user_id=current_user.id)
    db.add(db_expense)
    db.commit()
    db.refresh(db_expense)

    return db_expense
