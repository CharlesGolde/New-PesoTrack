"""
================================================================================
                            Data Models Module.
================================================================================

This module defines the core data structures used in the application.
Currently, it defines the `Transaction` class.

The `Transaction` class uses Encapsulation to protect data integrity,
ensuring that amounts are non-negative and valid.
================================================================================
"""

from datetime import datetime


class Transaction:
    """
    Represents a single financial transaction.

    This class encapsulates the details of an expense, including date,
    name, category, and amount. It enforces validation rules on the amount
    to ensure data consistency.

    Attributes:
        _date (str): Private attribute for the transaction date.
        _name (str): Private attribute for the transaction name.
        _category (str): Private attribute for the category.
        _amount (float): Private attribute for the amount.
    """

    def __init__(self, date: str, name: str, category: str, amount: float):
        """
        Constructs a Transaction object.

        Args:
            date (str): The date of the transaction (YYYY-MM-DD).
            name (str): The name or description of the transaction.
            category (str): The category (e.g., Food, Transport).
            amount (float): The monetary value of the transaction.

        Raises:
            ValueError: If the amount is negative, raised via the setter.
        """
        self._date = date
        self._name = name
        self._category = category
        self._amount = 0.0  # Default safe value

        # Use setter to validate immediately
        self.amount = amount

    @property
    def amount(self):
        """
        Getter for the amount property.

        Returns:
            float: The transaction amount.
        """
        return self._amount

    @amount.setter
    def amount(self, value):
        """
        Setter for the amount property with validation.

        Validates that the amount is a positive number.

        Args:
            value (int or float): The value to set.

        Raises:
            ValueError: If value is not a number or is negative.
        """
        if not isinstance(value, (int, float)):
            raise ValueError("Amount must be a number")
        if value < 0:
            raise ValueError("Amount cannot be negative")
        self._amount = float(value)

    @property
    def date(self):
        """Getter for the date property."""
        return self._date

    @property
    def name(self):
        """Getter for the name property."""
        return self._name

    @property
    def category(self):
        """Getter for the category property."""
        return self._category

    def to_dict(self):
        """
        Serializes the transaction to a dictionary.

        Useful for passing data to writers or templates.

        Returns:
            dict: A dictionary representation of the transaction.
        """
        return {
            "date": self._date,
            "name": self._name,
            "category": self._category,
            "amount": self._amount
        }