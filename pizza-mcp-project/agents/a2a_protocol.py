from dataclasses import dataclass

@dataclass
class OrderConfirmed:
    order_id: str
    eta_minutes: int
    pizza: str
    size: str
    quantity: int

@dataclass
class SchedulingComplete:
    order_id: str
    event_id: str
    scheduled_time: str
    status: str
