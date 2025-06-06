"""
Модели для токенов
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Float, DateTime, JSON
from sqlalchemy.orm import relationship
from app.models.base import BaseModel, HistoryModel
from datetime import datetime


class TokenBalance:
    def __init__(self, address: str, balance: float):
        self.address = address
        self.balance = balance


class Token(BaseModel):
    __tablename__ = 'tokens'

    address = Column(String(42), unique=True, nullable=False)
    balance = Column(Float, nullable=False, default=0.0)
    symbol = Column(String(32), nullable=True)
    name = Column(String(128), nullable=True)
    total_supply = Column(Float, nullable=True)
    last_transaction = Column(DateTime, nullable=True)

