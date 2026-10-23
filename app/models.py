
from datetime import date
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(
        String(150), unique=True, nullable=False
    )

    categories: Mapped[list["Category"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )
    expenses: Mapped[list["Expense"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )


class Category(Base):
    __tablename__ = "categories"
    __table_args__ = (
        UniqueConstraint("user_id", "name"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="categories"
    )
    expenses: Mapped[list["Expense"]] = relationship(
        back_populates="category"
    )


class Expense(Base):
    __tablename__ = "expenses"
    __table_args__ = (
        CheckConstraint("amount > 0", name="positive_amount"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    description: Mapped[str] = mapped_column(
        String(200), nullable=False
    )
    amount: Mapped[Decimal] = mapped_column(
        Numeric(10, 2), nullable=False
    )
    expense_date: Mapped[date] = mapped_column(
        Date, default=date.today, nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False,
    )

    user: Mapped["User"] = relationship(
        back_populates="expenses"
    )
    category: Mapped["Category"] = relationship(
        back_populates="expenses"
    )
