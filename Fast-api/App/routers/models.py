from pydantic import BaseModel


class PaymentData(BaseModel):
    amount: float
    date: str
    count: int


class CustomerTotalRemain(BaseModel):
    total_remain: float
    branch_id: int
    branch_name: str


class WeeklyWage(BaseModel):
    week_number: int
    total_interest: float
    first_week_date: str


class UsableCredit(BaseModel):
    date: str
    branch_name: str
    sum_credit: float


class FinalCredit(BaseModel):
    branch_name: str
    final_credit: float
    tr_ge_date: str


class Transactions(BaseModel):
    branch_name: str
    is_a_purchase: bool
    total_amount: float
    date: str
    stock_code: str


class PortfoComposition(BaseModel):
    stock_code: str
    stock_price: float
    date_to_ge: str
    usable_credit: float


class CreditKPI(BaseModel):
    kpi: float
    tr_ge_date: str
    week_number: int

