from typing import List, Dict, Optional
from django.db import transaction
from django.utils.dateparse import parse_datetime
from django.db.models import QuerySet

from db.models import Order, Ticket, User


@transaction.atomic
def create_order(
        tickets: List[Dict],
        username: str,
        date: Optional[str] = None,
) -> Order:
    user = User.objects.get(username=username)

    order = Order(user=user)
    if date:
        order.created_at = parse_datetime(date)
    order.save()

    for ticket_data in tickets:
        Ticket.objects.create(
            movie_session_id=ticket_data["movie_session"],
            order=order,
            row=ticket_data["row"],
            seat=ticket_data["seat"]
        )

    return order


def get_orders(username: Optional[str] = None) -> QuerySet:
    if username:
        return Order.objects.filter(user__username=username)
    return Order.objects.all()
