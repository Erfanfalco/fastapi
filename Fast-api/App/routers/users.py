import sqlalchemy as db
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends

from . functions import format_date

from . models import (
    PaymentData,
    CustomerTotalRemain,
    WeeklyWage,
    UsableCredit,
    Transactions,
    FinalCredit,
    PortfoComposition,
    CreditKPI
)

from . Database.dependencies import get_sql_db_session, get_postgres_db_session

from . Database.commands import (
    future_settlements_cmd,
    customer_remain_cmd,
    weekly_wage_cmd,
    daily_usable_credit_cmd,
    daily_transactions_cmd,
    daily_final_credit_cmd,
    daily_portfo_composition,
    credit_kpi_cmd
)


router = APIRouter()


@router.get("/Future-settlements", response_model=list[PaymentData], tags=['General'])
async def read_future_settlements(db_session: Session = Depends(get_sql_db_session)):
    """
        Fetches future settlement data.
        Returns:
            List[PaymentData]: Future settlement data.
        """
    result = db_session.execute(db.text(future_settlements_cmd))
    data_dicts = [PaymentData(amount=float(row[0]), count=int(row[1]), date=str(row[2])) for row in result]
    return data_dicts


@router.get("/Customer-Total-Remain", response_model=list[CustomerTotalRemain], tags=['General'])
async def read_customer_remain_data(db_session: Session = Depends(get_postgres_db_session)):
    """
        Fetches total remain data for customers.
        Returns:
            List[CustomerTotalRemain]: Total remain data for customers.
        """
    result = db_session.execute(db.text(customer_remain_cmd))
    data_dicts = [CustomerTotalRemain(
        total_remain=float(row[0]), branch_id=int(row[1]), branch_name=str(row[2])) for row in result]
    return data_dicts


@router.get("/Weekly-Wage", response_model=list[WeeklyWage], tags=['Weekly'])
async def read_weekly_wage_data(date: str | None = 'CURRENT_DATE', db_session: Session = Depends(get_postgres_db_session)):
    """
        Fetches weekly wage data.
        Returns:
            List[WeeklyWage]: Weekly wage data.
        """
    result = db_session.execute(db.text(weekly_wage_cmd.format(date)))
    data_dicts = [WeeklyWage(week_number=int(row[0]), total_interest=float(row[1]),
                             first_week_date=str(row[2])) for row in result]
    return data_dicts


@router.get("/Daily-Usable-Credit", response_model=list[UsableCredit], tags=['Daily'])
async def read_daily_usable_credit_data(date: str | None = 'CURRENT_DATE', db_session: Session = Depends(get_postgres_db_session)):
    """
       Fetches daily usable credit data.
       Returns:
           List[UsableCredit]: Daily usable credit data.
       """
    result = db_session.execute(db.text(daily_usable_credit_cmd.format(format_date(date))))
    data_dicts = [UsableCredit(date=str(row[0]), branch_name=str(row[1]),
                               sum_credit=float(row[2])) for row in result]
    return data_dicts


@router.get("/Daily-Final-Credit", response_model=list[FinalCredit], tags=['Daily'])
async def read_daily_usable_credit_data(date: str | None = 'CURRENT_DATE', db_session: Session = Depends(get_postgres_db_session)):
    """
        Fetches daily final credit data.
        Returns:
            List[FinalCredit]: Daily final credit data.
        """
    result = db_session.execute(db.text(daily_final_credit_cmd.format(date)))
    data_dicts = [FinalCredit(branch_name=str(row[0]), final_credit=float(row[1]),
                              tr_ge_date=str(row[2])) for row in result]
    return data_dicts


@router.get("/Daily-Transactions", response_model=list[Transactions], tags=['Daily'])
async def read_daily_final_credit_data(date: str | None = 'CURRENT_DATE', db_session: Session = Depends(get_postgres_db_session)):
    """
        Fetches daily transactions data.
        Returns:
            List[Transactions]: Daily transactions data.
        """
    result = db_session.execute(db.text(daily_transactions_cmd.format(date)))
    data_dicts = [Transactions(branch_name=str(row[0]), is_a_purchase=bool(row[1]),
                               total_amount=float(row[2]), date=str(row[3]), stock_code=str(row[4])) for row in result]
    return data_dicts


@router.get("/Daily-Portfo-Composition", response_model=list[PortfoComposition], tags=['Daily'])
async def read_daily_portfo_composition_data(date: str | None = 'CURRENT_DATE', db_session: Session = Depends(get_postgres_db_session)):
    """
        Fetches daily portfolio composition data.
        Returns:
            List[PortfoComposition]: Daily portfolio composition data.
        """
    result = db_session.execute(db.text(daily_portfo_composition.format(date)))
    data_dicts = [PortfoComposition(stock_code=str(row[0]), stock_price=bool(row[1]),
                                    date_to_ge=float(row[2]), usable_credit=str(row[3])) for row in result]
    return data_dicts


@router.get("/Weekly-Credit-KPI", response_model=list[CreditKPI], tags=['Weekly'])
async def calculate_credit_kpi(date: str | None = 'CURRENT_DATE', db_session: Session = Depends(get_postgres_db_session)):
    """
        Calculates credit KPI.
        Returns:
            List[CreditKPI]: Calculated credit KPI.
        """
    result = db_session.execute(db.text(credit_kpi_cmd.format(date)))
    data_dicts = [CreditKPI(kpi=str(row[0]), tr_ge_date=bool(row[1]),
                            week_number=float(row[2])) for row in result]
    return data_dicts
