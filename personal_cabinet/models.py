from dataclasses import dataclass, field
from typing import List
from enum import StrEnum


class PurchaseType(StrEnum):
    masterclass = "masterclass"
    videocourse = "videocourse"
    pattern = "pattern"


@dataclass
class Purchase:
    id: str
    purchase_type: PurchaseType
    title: str
    description: str
    link: str
    category: str
    purchase_date: str
    photo_url: str = ""


@dataclass
class UserProfile:
    user_id: int
    username: str = ""
    first_name: str = ""
    last_name: str = ""
    purchases: List[Purchase] = field(default_factory=list)

    def get_purchases_by_type(self, purchase_type: PurchaseType) -> List[Purchase]:
        return [p for p in self.purchases if p.purchase_type == purchase_type]

    def get_purchases_by_category(self, category: str) -> List[Purchase]:
        return [p for p in self.purchases if p.category == category]

    def has_purchase(self, item_id: str) -> bool:
        return any(p.id == item_id for p in self.purchases)
