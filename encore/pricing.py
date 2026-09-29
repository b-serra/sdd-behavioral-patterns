
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
        # TODO: store `percent`, raising ValueError if it isn't between 0
        # and 100 (inclusive).

        if percent < 0.0 or percent > 100.0:
            raise ValueError("Percent must be between 0 and 100")

        self.percent = float(percent)




    def price(self, subtotal: float, quantity: int) -> float:
        # TODO: apply the percentage discount to `subtotal`. The result must
        # never be negative (clamp at 0.0).

        total = subtotal * (1 - self.percent / 100)
        if total < 0.0:
            total = 0.0

        return total


class GroupPricing(PricingStrategy):
    """Per-ticket discount once a party reaches a minimum size."""

    def __init__(self, threshold: int, per_ticket_off: float):

        self.threshold = threshold
        self.per_ticket_off = per_ticket_off

    def price(self, subtotal: float, quantity: int) -> float:
        # TODO: if `quantity` is below `threshold`, return subtotal
        # unchanged. Otherwise subtract `per_ticket_off * quantity` from
        # `subtotal`, clamped at 0.0.

        if quantity < self.threshold:
            return subtotal
        else:
            total = subtotal - quantity * self.per_ticket_off
            if total < 0.0:
                total = 0.0

            return total

