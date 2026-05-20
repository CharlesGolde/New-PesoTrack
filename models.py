from datetime import datetime

class Transaction:
    def __init__(self, date: str, name: str, category: str, amount: float):
        # Private attributes (Encapsulation)
        self._date = date
        self._name = name
        self._category = category
        self._amount = 0.0  # Default safe value

        # Use setter to validate immediately
        self.amount = amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        """Data validation: Ensure amount is a positive number."""
        if not isinstance(value, (int, float)):
            raise ValueError("Amount must be a number")
        if value < 0:
            raise ValueError("Amount cannot be negative")
        self._amount = float(value)

    @property
    def date(self):
        return self._date

    @property
    def name(self):
        return self._name

    @property
    def category(self):
        return self._category

    def to_dict(self):
        return {
            "date": self._date,
            "name": self._name,
            "category": self._category,
            "amount": self._amount
        }