from pydantic import BaseModel
from typing import Optional


class Transaction(BaseModel):
    id:       int
    address:  str
    date:     str
    amount:   Optional[float]
    category: str


class Analytics(BaseModel):
    total:        int
    total_amount: float
    by_category:  dict[str, int]
