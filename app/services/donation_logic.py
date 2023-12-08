from datetime import datetime
from typing import List, Tuple

from app.models.abstract import Investment


def allocate_donations(
    new_entry: Investment,
    pending_objects: List[Investment],
) -> Tuple[Investment, List[Investment]]:
    new_entry.invested_amount = (
        0 if new_entry.invested_amount is None else new_entry.invested_amount
    )
    updated_pending_objects = []
    for object in pending_objects:
        if new_entry.fully_invested:
            break
        transfer = min(
            new_entry.full_amount - new_entry.invested_amount,
            object.full_amount - object.invested_amount
        )
        for investment in [object, new_entry]:
            investment.invested_amount += transfer
            if investment.invested_amount == object.full_amount:
                investment.fully_invested = True
                investment.close_date = datetime.utcnow()
        updated_pending_objects.append(object)
    return updated_pending_objects
