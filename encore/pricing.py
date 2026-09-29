
from abc import ABC, abstractmethod


class PricingStrategy(ABC):
    """
    Strategy interface: turns a cart's subtotal into its final total.
    """

    @abstractmethod
    def price(self, subtotal: float, quantity: int) -> float:
        raise NotImplementedError


class StandardPricing(PricingStrategy):
    """No discount: the total is just the subtotal."""

    def price(self, subtotal: float, quantity: int) -> float:
        return subtotal

class EarlyBirdPricing(PricingStrategy):
    """Flat percentage off the subtotal, for shows still far from sold out."""

    def __init__(self, percent: float):
        if not 0 <= percent <= 100:
            raise ValueError("percent must be between 0 and 100 (inclusive)")
        self.percent = percent
        # TODO: store `percent`, raising ValueError if it isn't between 0
        # and 100 (inclusive).
        pass

    def price(self, subtotal: float, quantity: int) -> float:
        total = subtotal - (subtotal * self.percent / 100)
        return max(0.0, total)
        # TODO: apply the percentage discount to `subtotal`. The result must
        # never be negative (clamp at 0.0).


class GroupPricing(PricingStrategy):
    """Per-ticket discount once a party reaches a minimum size."""

    def __init__(self, threshold: int, per_ticket_off: float):
        self.threshold = threshold
        self.per_ticket_off = per_ticket_off
        # TODO: store `threshold` and `per_ticket_off`.
        pass

    def price(self, subtotal: float, quantity: int) -> float:
        if quantity < self.threshold:
            return subtotal
        else:
            total = subtotal - (self.per_ticket_off * quantity)
            return max(0.0,total)
        # TODO: if `quantity` is below `threshold`, return subtotal
        # unchanged. Otherwise subtract `per_ticket_off * quantity` from
        # `subtotal`, clamped at 0.0.
