
from decimal import Decimal

import pytest
from sqlalchemy import create_engine, event, select
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import User, Category, Expense
from app.expenses import (
    add_expense,
    create_category,
    get_expenses,
    get_total_spending,
)


@pytest.fixture
def session():
    test_engine = create_engine("sqlite://")

    @event.listens_for(test_engine, "connect")
    def enable_foreign_keys(connection, _record):
        connection.execute("PRAGMA foreign_keys=ON")

    Base.metadata.create_all(test_engine)

    TestSession = sessionmaker(
        bind=test_engine,
        expire_on_commit=False,
    )

    with TestSession() as test_session:
        yield test_session

    test_engine.dispose()


def create_test_user(session):
    user = User(
        name="Test User",
        email="test@example.com",
    )
    session.add(user)
    session.flush()

    category = create_category(
        session, user.id, "Food"
    )

    return user, category


def test_add_expense(session):
    with session.begin():
        user, category = create_test_user(session)

        expense = add_expense(
            session,
            user.id,
            category.id,
            "Lunch",
            "2500.00",
        )

        expense_id = expense.id

    saved_expense = session.get(Expense, expense_id)

    assert saved_expense.description == "Lunch"
    assert saved_expense.amount == Decimal("2500.00")


def test_calculate_total_spending(session):
    with session.begin():
        user, category = create_test_user(session)

        add_expense(
            session, user.id, category.id,
            "Lunch", "2500.00"
        )
        add_expense(
            session, user.id, category.id,
            "Dinner", "3500.00"
        )

        user_id = user.id

    assert get_total_spending(
        session, user_id
    ) == Decimal("6000.00")


def test_reject_invalid_amount(session):
    with session.begin():
        user, category = create_test_user(session)

        with pytest.raises(ValueError):
            add_expense(
                session,
                user.id,
                category.id,
                "Invalid expense",
                "-100",
            )

        # A caught validation error does not abort
        # the transaction because no database write occurred.


def test_user_cannot_use_another_users_category(session):
    with session.begin():
        user_a, _ = create_test_user(session)

        user_b = User(
            name="Another User",
            email="another@example.com",
        )
        session.add(user_b)
        session.flush()

        category_b = create_category(
            session, user_b.id, "Private"
        )

        user_a_id = user_a.id
        category_b_id = category_b.id

    with pytest.raises(ValueError):
        with session.begin():
            add_expense(
                session,
                user_a_id,
                category_b_id,
                "Not allowed",
                "500",
            )


def test_transaction_rolls_back(session):
    with pytest.raises(RuntimeError):
        with session.begin():
            user = User(
                name="Temporary User",
                email="temporary@example.com",
            )
            session.add(user)
            session.flush()

            raise RuntimeError("Simulated failure")

    saved_user = session.scalar(
        select(User).where(
            User.email == "temporary@example.com"
        )
    )

    assert saved_user is None


def test_get_expenses(session):
    with session.begin():
        user, category = create_test_user(session)

        add_expense(
            session, user.id, category.id,
            "Lunch", "2500"
        )
        user_id = user.id

    expenses = get_expenses(session, user_id)

    assert len(expenses) == 1
    assert expenses[0].description == "Lunch"
