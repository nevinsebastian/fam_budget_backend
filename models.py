# models.py

from sqlalchemy import Column, Integer, String, Float, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    
    budgets = relationship("Budget", back_populates="owner")
    expenses = relationship("Expense", back_populates="owner")

class Budget(Base):
    __tablename__ = "budgets"

    id = Column(Integer, primary_key=True, index=True)
    month = Column(Integer, unique=True, index=True)
    total_budget = Column(Float)
    categories = relationship("Category", back_populates="budget")
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="budgets")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    amount = Column(Float)
    budget_id = Column(Integer, ForeignKey("budgets.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    budget = relationship("Budget", back_populates="categories")
    expenses = relationship("Expense", back_populates="category")

class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))
    budget_id = Column(Integer, ForeignKey("budgets.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")
