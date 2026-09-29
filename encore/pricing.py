
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
        # TODO: no discount, return subtotal unchanged.


class EarlyBirdPricing(PricingStrategy):
    """Flat percentage off the subtotal, for shows still far from sold out."""

    def __init__(self, percent: float):
        if (percent < 0) or (percent > 100):
            raise ValueError("percent out of range.")
        self.percent = percent

    def price(self, subtotal: float, quantity: int) -> float:
        discount = subtotal * (self.percent / 100)
        if discount > subtotal:
            return 0.0
        return subtotal - discount


class GroupPricing(PricingStrategy):
    """Per-ticket discount once a party reaches a minimum size."""

    def __init__(self, threshold: int, per_ticket_off: float):
        self.threshold = threshold
        self.per_ticket_off = per_ticket_off
        # TODO: store `threshold` and `per_ticket_off`.

    def price(self, subtotal: float, quantity: int) -> float:
        if quantity < self.threshold:
            return subtotal
        new_subtotal = subtotal - (self.per_ticket_off * quantity)
        if new_subtotal < 0.0:
            return 0.0
        return new_subtotal
    
        # TODO: if `quantity` is below `threshold`, return subtotal
        # unchanged. Otherwise subtract `per_ticket_off * quantity` from
        # `subtotal`, clamped at 0.0.
