
from datetime import date
from decimal import Decimal

from sqlalchemy import select, func
from sqlalchemy.orm import Session

from app.models import User, Category, Expense


def create_category(
    session: Session,
    user_id: int,
    name: str,
) -> Category:
    name = name.strip()

    if not name:
        raise ValueError("Category name cannot be empty.")

    user = session.get(User, user_id)
    if user is None:
        raise ValueError("User does not exist.")

    category = Category(user_id=user_id, name=name)
    session.add(category)
    session.flush()

    return category


def add_expense(
    session: Session,
    user_id: int,
    category_id: int,
    description: str,
    amount: Decimal | str | int,
    expense_date: date | None = None,
) -> Expense:
    amount = Decimal(str(amount))
    description = description.strip()

    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")

    if not description:
        raise ValueError("Description cannot be empty.")

    category = session.scalar(
        select(Category).where(
            Category.id == category_id,
            Category.user_id == user_id,
        )
    )

    if category is None:
        raise ValueError(
            "Category does not exist or belongs to another user."
        )

    expense = Expense(
        user_id=user_id,
        category_id=category_id,
        description=description,
        amount=amount,
        expense_date=expense_date or date.today(),
    )

    session.add(expense)
    session.flush()

    return expense


def get_expenses(session: Session, user_id: int) -> list[Expense]:
    statement = (
        select(Expense)
        .where(Expense.user_id == user_id)
        .order_by(Expense.expense_date.desc())
    )

    return list(session.scalars(statement).all())


def get_total_spending(session: Session, user_id: int) -> Decimal:
    statement = select(
        func.coalesce(func.sum(Expense.amount), 0)
    ).where(Expense.user_id == user_id)

    total = session.scalar(statement)

    return Decimal(str(total or 0))
