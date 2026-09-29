
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
        # TODO: no discount, return subtotal unchanged.
        return subtotal


class EarlyBirdPricing(PricingStrategy):
    """Flat percentage off the subtotal, for shows still far from sold out."""

    def __init__(self, percent: float):
        self.percent=percent
        if not 0<percent<=100:
            raise ValueError ("percent not between 0 and 100")
        

    def price(self, subtotal: float, quantity: int) -> float:
        discount=subtotal-(subtotal * (self.percent/100))
        if discount<0:
            discount=0
            
        return discount


class GroupPricing(PricingStrategy):
    """Per-ticket discount once a party reaches a minimum size."""

    def __init__(self, threshold: int, per_ticket_off: float):
        self.threshold=threshold
        self.per_ticket_off=per_ticket_off
        

    def price(self, subtotal: float, quantity: int) -> float:
        # TODO: if `quantity` is below `threshold`, return subtotal
        if quantity < self.threshold:
            return subtotal
        else:
            subtotal=subtotal-(self.per_ticket_off*quantity)

        if subtotal <=0:
            return 0
        else:
            return subtotal

        
        # unchanged. Otherwise subtract `per_ticket_off * quantity` from
        # `subtotal`, clamped at 0.0.
      
