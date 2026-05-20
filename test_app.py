"""
================================================================================
                                 Unit Testing Module.
================================================================================

This module contains unit tests for the PesoTrack application using the
`pytest` framework. It verifies the correctness of the logic in `models`
and `core` modules, specifically testing encapsulation, calculation logic,
and data persistence.

Classes:
    MockInputReader: A mock object to simulate input reading.
    MockOutputWriter: A mock object to capture output writing.

================================================================================
"""

import pytest
import os
from models import Transaction
from core import FinanceManager


class MockInputReader:
    """
    A mock implementation of IInputReader for testing purposes.

    Provides hardcoded data to avoid user interaction during tests.
    """

    def get_transactions(self):
        """
        Returns a predefined list of mock transactions.

        Returns:
            List[Transaction]: Hardcoded transaction list.
        """
        return [
            Transaction("2023-10-01", "Lunch", "Food", 500.0),
            Transaction("2023-10-02", "Rent", "Housing", 2000.0),
        ]

    def get_ids_to_delete(self):
        """
        Returns an empty list as deletion is not tested here.

        Returns:
            List: Empty list.
        """
        return []


class MockOutputWriter:
    """
    A mock implementation of IOutputWriter for testing purposes.

    Captures the data passed to it for assertion in tests.
    """

    def __init__(self):
        """Initializes the storage list."""
        self.reports = []

    def write_report(self, report_data):
        """
        Appends the report data to the internal list.

        Args:
            report_data (Dict): Data to capture.
        """
        self.reports.append(report_data)


def test_transaction_encapsulation():
    """
    Test 1: Verify Transaction encapsulation and validation.

    Checks that the amount property setter correctly validates input
    and raises ValueError for negative numbers.
    """
    t = Transaction("2023-01-01", "Test", "TestCat", 100)
    assert t.amount == 100

    # Test that negative amounts raise an error
    with pytest.raises(ValueError):
        t.amount = -50


def test_add_expense_logic():
    """
    Test 2: Verify adding expenses and calculating totals.

    Tests that transactions are added correctly and the total calculation
    sums the amounts accurately.
    """
    # Arrange
    mock_reader = MockInputReader()
    mock_writer = MockOutputWriter()
    # Use a separate file for testing
    manager = FinanceManager(mock_reader, mock_writer, filename="test_expenses.csv")

    # Clean up test file if it exists
    if os.path.exists("test_expenses.csv"):
        os.remove("test_expenses.csv")

    # Act
    manager.add_expense(Transaction("2023-01-01", "A", "B", 500.0))
    manager.add_expense(Transaction("2023-01-01", "C", "D", 1000.0))

    # Assert
    assert manager.get_total_amount() == 1500.0


def test_delete_expense_logic():
    """
    Test 3: Verify deleting expenses by index.

    Tests that `delete_expenses` correctly removes items from the list
    based on their string IDs (e.g., "row_0").
    """
    # Arrange
    mock_reader = MockInputReader()
    mock_writer = MockOutputWriter()
    manager = FinanceManager(mock_reader, mock_writer, filename="test_expenses.csv")

    # Add data first
    manager.add_expense(Transaction("2023-01-01", "A", "B", 500.0))
    manager.add_expense(Transaction("2023-01-01", "C", "D", 1000.0))

    # Act: Delete the first item (row_0)
    manager.delete_expenses(["row_0"])

    # Assert: Remaining total should be 1000.0
    assert manager.get_total_amount() == 1000.0


def test_category_breakdown():
    """
    Test 4: Verify the Expenses Report logic (Category Breakdown).

    Tests that `get_category_breakdown` correctly aggregates amounts
    by their category.
    """
    # Arrange
    mock_reader = MockInputReader()
    mock_writer = MockOutputWriter()
    manager = FinanceManager(mock_reader, mock_writer, filename="test_expenses.csv")

    # Add specific categorized data
    manager.add_expense(Transaction("2023-01-01", "Burger", "Food", 100.0))
    manager.add_expense(Transaction("2023-01-02", "Bus Ticket", "Transport", 50.0))
    manager.add_expense(Transaction("2023-01-03", "Pizza", "Food", 150.0))

    # Act
    breakdown = manager.get_category_breakdown()

    # Assert
    assert "Food" in breakdown
    assert "Transport" in breakdown
    assert breakdown["Food"] == 250.0  # 100 + 150
    assert breakdown["Transport"] == 50.0