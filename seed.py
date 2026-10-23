
from decimal import Decimal

from sqlalchemy import select

from app.database import create_tables, SessionLocal
from app.models import User, Category, Expense
from app.expenses import add_expense, create_category


def seed_database():
    create_tables()

    with SessionLocal.begin() as session:
        user = session.scalar(
            select(User).where(
                User.email == "demo@example.com"
            )
        )

        if user is None:
            user = User(
                name="Demo User",
                email="demo@example.com",
            )
            session.add(user)
            session.flush()

        category_names = ["Food", "Transport", "Bills"]
        categories = {}

        for name in category_names:
            category = session.scalar(
                select(Category).where(
                    Category.user_id == user.id,
                    Category.name == name,
                )
            )

            if category is None:
                category = create_category(
                    session, user.id, name
                )

            categories[name] = category

        samples = [
            ("Lunch", "2500.00", "Food"),
            ("Bus fare", "800.00", "Transport"),
            ("Electricity", "5000.00", "Bills"),
        ]

        for description, amount, category_name in samples:
            existing = session.scalar(
                select(Expense.id).where(
                    Expense.user_id == user.id,
                    Expense.description == description,
                    Expense.category_id
                    == categories[category_name].id,
                )
            )

            if existing is None:
                add_expense(
                    session=session,
                    user_id=user.id,
                    category_id=categories[category_name].id,
                    description=description,
                    amount=Decimal(amount),
                )

    print("Sample expense data created successfully.")


if __name__ == "__main__":
    seed_database()
