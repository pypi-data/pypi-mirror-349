from datetime import datetime
from enum import StrEnum

from ed_domain.core.entities.base_entity import BaseEntity
from ed_domain.core.value_objects.money import Money


class BillStatus(StrEnum):
    PENDING = "pending"
    WITH_DRIVER = "with_driver"
    DONE = "done"


class Bill(BaseEntity):
    amount: Money
    bill_status: BillStatus
    due_date: datetime
