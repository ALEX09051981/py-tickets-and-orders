from typing import List, Dict, Optional
from datetime import datetime
from django.db import transaction
from django.utils import timezone
from django.db.models import QuerySet
from db.models import Order, Ticket, User


@transaction.atomic
def create_order(
    tickets: List[Dict],
    username: str,
    date: Optional[str] = None,
) -> Order:
    user = User.objects.get(username=username)

    if date:
        # Parse date string without timezone info
        created_at = datetime.strptime(date, "%Y-%m-%d %H:%M")
    else:
        created_at = timezone.now().replace(tzinfo=None)

    order = Order(user=user, created_at=created_at)
    order.save()

    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session_id=ticket_data["movie_session"],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"],
        )

    return order


def get_orders(username: Optional[str] = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
