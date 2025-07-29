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
    id: Optional[int] = Field(nullable=False)
    organization: uuid.UUID = Field(index=True)
    event_time: Optional[datetime] = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    sku: uuid.UUID = Field(foreign_key="sku.id")
    amount: float

    __table_args__ = (
        PrimaryKeyConstraint("id", "event_time"),
    )


class SKU(BillingModel, table=True):
    amount: float
    currency: CurrencyEnum = Field(sa_column=Column(SqlEnum(CurrencyEnum)))


