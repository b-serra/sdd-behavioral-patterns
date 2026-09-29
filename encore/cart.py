from abc import ABC, abstractmethod
from typing import Dict, Tuple

from .pricing import PricingStrategy, StandardPricing


class Cart:
    """
    Receiver: holds ticket line items and the active pricing strategy.
    """

    def __init__(self, pricing_strategy: PricingStrategy = None):
        self._items: Dict[str, Tuple[int, float]] = {}
        self._pricing_strategy = pricing_strategy or StandardPricing()

    @property
    def pricing_strategy(self) -> PricingStrategy:
        return self._pricing_strategy

    def add_item(self, category: str, qty: int, unit_price: float) -> None:
        current_qty, _ = self._items.get(category, (0, unit_price))
        self._items[category] = (current_qty + qty, unit_price)

    def remove_item(self, category: str, qty: int) -> int:
        if category not in self._items:
            return 0
        current_qty, unit_price = self._items[category]
        removed = min(qty, current_qty)
        remaining = current_qty - removed
        if remaining > 0:
            self._items[category] = (remaining, unit_price)
        else:
            del self._items[category]
        return removed

    def set_pricing_strategy(self, strategy: PricingStrategy) -> PricingStrategy:
        previous = self._pricing_strategy
        self._pricing_strategy = strategy
        return previous

    def items(self) -> Dict[str, Tuple[int, float]]:
        return dict(self._items)

    def quantity(self) -> int:
        return sum(qty for qty, _ in self._items.values())

    def subtotal(self) -> float:
        return sum(qty * unit_price for qty, unit_price in self._items.values())

    def total(self) -> float:
        return self._pricing_strategy.price(self.subtotal(), self.quantity())


class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def undo(self) -> None:
        raise NotImplementedError


class AddTicketCommand(Command):
    def __init__(self, cart: Cart, category: str, qty: int, unit_price: float):
        # TODO: store cart, category, qty and unit_price for later use.
        self._cart = cart
        self._category = category
        self._qty = qty
        self._unit_price = unit_price

    def execute(self) -> None:
        # TODO: add `qty` tickets of `category` at `unit_price` to the cart.
        self._cart.add_item(self._category, self._qty, self._unit_price)

    def undo(self) -> None:
        # TODO: remove exactly the tickets this command added.
        self._cart.remove_item(self._category, self._qty)


class RemoveTicketCommand(Command):
    def __init__(self, cart: Cart, category: str, qty: int):
        # TODO: store cart, category and qty. You'll also need somewhere to
        # remember how many tickets were actually removed, and at what
        # price, once execute() runs.
        self._cart = cart
        self._category = category
        self._qty = qty
        self._actual_removed = 0
        self._unit_price = 0.0

    def execute(self) -> None:
        # TODO: remove up to `qty` tickets of `category` from the cart
        # (cart.remove_item returns how many were actually removed), and
        # remember that count plus the unit price so undo() can restore them.
        # Capture the price BEFORE removing, since removing all tickets
        # deletes the category from the cart.
        self._unit_price = self._cart.items().get(self._category, (0, 0.0))[1]
        self._actual_removed = self._cart.remove_item(self._category, self._qty)

    def undo(self) -> None:
        # TODO: add back exactly the quantity that was actually removed, at
        # the price it was removed at. Do nothing if nothing was removed.
        if self._actual_removed > 0:
            self._cart.add_item(self._category, self._actual_removed, self._unit_price)


class SetPricingStrategyCommand(Command):
    def __init__(self, cart: Cart, strategy: PricingStrategy):
        # TODO: store cart and the new strategy. You'll need somewhere to
        # keep the previous strategy once execute() runs.
        self._cart = cart
        self._new_strategy = strategy
        self._previous_strategy = None

    def execute(self) -> None:
        # TODO: swap the cart's pricing strategy, remembering the previous one.
        self._previous_strategy = self._cart.set_pricing_strategy(self._new_strategy)

    def undo(self) -> None:
        # TODO: restore the previous pricing strategy.
        self._cart.set_pricing_strategy(self._previous_strategy)


class CartInvoker:
    def __init__(self):
        # TODO: set up a history stack and a redo stack.
        self._history = []
        self._redo_stack = []

    def run(self, command: Command) -> None:
        # TODO: execute `command`, push it onto the history, and clear the
        # redo stack (a fresh command invalidates any pending redo).
        command.execute()
        self._history.append(command)
        self._redo_stack.clear()

    def undo(self, n: int = 1) -> int:
        # TODO: undo up to `n` commands from the history, moving each onto
        # the redo stack. Return how many were actually undone (fewer than
        # `n` once history runs out).
        undone = 0
        for _ in range(min(n, len(self._history))):
            command = self._history.pop()
            command.undo()
            self._redo_stack.append(command)
            undone += 1
        return undone

    def redo(self, n: int = 1) -> int:
        # TODO: redo up to `n` commands from the redo stack, moving each back
        # onto the history. Return how many were actually redone.
        redone = 0
        for _ in range(min(n, len(self._redo_stack))):
            command = self._redo_stack.pop()
            command.execute()
            self._history.append(command)
            redone += 1
        return redone