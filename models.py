from sqlalchemy import Column, Integer, String,Float, TIMESTAMP, text, Table, ForeignKey,DateTime, Boolean, Time, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Define SQLAlchemy models
Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    balance = Column(Float, default=0.0)
    categories = relationship("Category", back_populates="user")
    expenses = relationship("Expense", back_populates="user")
    budgets = relationship("MonthlyBudget", back_populates="user")


class MonthlyBudget(Base):
    __tablename__ = "monthly_budget"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    month = Column(Integer)
    year = Column(Integer)
    budget = Column(Float)

    user = relationship("User", back_populates="budgets")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    budget = Column(Float)  # Add budget column
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="categories")
    expenses = relationship("Expense", back_populates="category")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    category_id = Column(Integer, ForeignKey('categories.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    category = relationship("Category", back_populates="expenses")
    user = relationship("User", back_populates="expenses")