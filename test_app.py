import pytest
import os
from models import Transaction
from core import FinanceManager

class MockInputReader:
    """A fake reader that provides data without needing user input."""

    def get_transactions(self):
        return [
            Transaction("2023-10-01", "Lunch", "Food", 500.0),
            Transaction("2023-10-02", "Rent", "Housing", 2000.0),
        ]

    def get_ids_to_delete(self):
        return []


class MockOutputWriter:
    """A fake writer that captures the result."""

    def __init__(self):
        self.reports = []

    def write_report(self, report_data):
        self.reports.append(report_data)


def test_transaction_encapsulation():
    """Test 1: Test that setters validate data correctly."""
    t = Transaction("2023-01-01", "Test", "TestCat", 100)
    assert t.amount == 100

    # Test that negative amounts raise an error
    with pytest.raises(ValueError):
        t.amount = -50


def test_add_expense_logic():
    """Test 2: Test adding expenses and calculating total."""
    # Arrange
    mock_reader = MockInputReader()
    mock_writer = MockOutputWriter()
    # Use a separate file for testing to avoid messing up real data
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
    """Test 3: Test deleting expenses."""
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
    """Test 4: Test the Expenses Report logic (Category Breakdown)."""
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