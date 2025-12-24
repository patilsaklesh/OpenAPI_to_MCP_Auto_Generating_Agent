from dataclasses import dataclass
from typing import Dict


@dataclass
class OrderConfirmedMessage:
    order_id: str
    eta_minutes: int

    def to_dict(self) -> Dict:
        return {
            "type": "ORDER_CONFIRMED",
            "order_id": self.order_id,
            "eta_minutes": self.eta_minutes,
        }
