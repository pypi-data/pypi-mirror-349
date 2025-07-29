import enum
import uuid
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import Enum as SqlEnum, PrimaryKeyConstraint

from sqlalchemy import Column
from sqlmodel import SQLModel, Field

from ..general.models import BillingModel


class CurrencyEnum(str, enum.Enum):
    USD = "USD"
    EUR = "EUR"
    GBP = "GBP"
    YPJ = "YPJ"


class BillingEvent(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    organization: uuid.UUID = Field(index=True)
    event_time: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    sku: uuid.UUID = Field(foreign_key="sku.id")

    __table_args__ = (
        PrimaryKeyConstraint("id", "event_time"),
    )


class SKU(SQLModel, table=True):
    id: int = Field(nullable=False, primary_key=True)
    name: str = Field(nullable=False)
    description: str = Field(nullable=False)
    amount: float
    currency: CurrencyEnum = Field(sa_column=Column(SqlEnum(CurrencyEnum)))
    created_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)}
    )