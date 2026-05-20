"""
================================================================================
                        Strategy Pattern Implementations.
================================================================================

This module defines the Abstract Base Classes for Input and Output strategies,
and their concrete implementations for the Web interface.

The Strategy Pattern allows the application to switch between different input
methods (e.g., Web vs Console) or output formats without changing the core logic.

================================================================================
"""

from abc import ABC, abstractmethod
from typing import List, Dict
from models import Transaction
from datetime import datetime


# --- Interfaces (Blueprints) ---

class IInputReader(ABC):
    """Blueprint for reading input data."""

    @abstractmethod
    def get_transactions(self) -> List[Transaction]:
        """Method to get a list of transactions."""
        pass

    @abstractmethod
    def get_ids_to_delete(self) -> List[str]:
        """Method to get IDs to delete."""
        pass


class IOutputWriter(ABC):
    """Blueprint for writing output data."""

    @abstractmethod
    def write_report(self, report_data: Dict):
        """Method to write a single line of report."""
        pass


# --- Web Implementations ---

class WebInputReader(IInputReader):
    """Reads data from website forms."""

    def __init__(self, post_data: Dict):
        """
        Saves the form data for later use.

        Args:
            post_data: The data dictionary from the website.
        """
        self.post_data = post_data

    def get_transactions(self) -> List[Transaction]:
        """
        Creates Transaction objects from the form data.

        Returns:
            A list containing the new transaction.
        """
        transactions = []
        try:
            current_date = datetime.now().strftime("%Y-%m-%d")
            name = self.post_data.get('name', [''])[0]
            category = self.post_data.get('category', [''])[0]
            amt = float(self.post_data.get('amount', ['0'])[0])
            t = Transaction(current_date, name, category, amt)
            transactions.append(t)
        except ValueError as e:
            print(f"Input Error: {e}")
        return transactions

    def get_ids_to_delete(self) -> List[str]:
        """
        Gets the list of IDs to delete from the form.

        Returns:
            A list of ID strings.
        """
        return self.post_data.get('ids', [])


class WebOutputWriter(IOutputWriter):
    """Writes data as HTML code for the website."""

    def __init__(self):
        """Sets up the writer with empty content."""
        self.html_content = ""
        self.row_counter = 0

    def write_report(self, report_data: Dict):
        """
        Creates an HTML table row for one transaction.

        Args:
            report_data: The data for one transaction.
        """
        row_id = f"row_{self.row_counter}"
        row = f"""
        <tr>
            <td><input type="checkbox" name="delete_ids" value="{row_id}"></td>
            <td>{report_data['date']}</td>
            <td>{report_data['name']}</td>
            <td>{report_data['category']}</td>
            <td class="amount-col">&#8369;{report_data['amount']:.2f}</td>
        </tr>
        """
        self.html_content += row
        self.row_counter += 1

    def write_category_report(self, breakdown: Dict[str, float]):
        """
        Creates HTML list items for the Expenses Report.

        Puts the Category on the Left and the Amount on the Right.
        Uses inline styles so no HTML changes are needed.

        Args:
            breakdown: A dictionary of categories and totals.
        """
        if not breakdown:
            self.html_content += "<li style='color: #64748b; text-align: center;'>No data to report</li>"
            return

        for cat, total in breakdown.items():
            # Inline styles used here to position elements:
            # display: flex -> Makes the items sit side-by-side.
            # justify-content: space-between -> Pushes left item to left, right item to right.
            self.html_content += f"""
            <li style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.1);">
                <span style="font-weight: 600; color: #e2e8f0;">{cat}</span>
                <span style="color: #d4af37;">&#8369;{total:.2f}</span>
            </li>
            """

    def get_html(self) -> str:
        """
        Returns the finished HTML code.

        Returns:
            The HTML string.
        """
        return self.html_content


# --- Console Implementations ---

class ConsoleInputReader(IInputReader):
    """Reads input from the computer terminal (text)."""

    def get_transactions(self) -> List[Transaction]:
        """Asks the user to type details in the console."""
        print("\n--- Enter Transaction Details ---")
        date = input("Date (YYYY-MM-DD, leave blank for today): ")
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        name = input("Name: ")
        category = input("Category: ")
        amt = float(input("Amount: "))
        return [Transaction(date, name, category, amt)]

    def get_ids_to_delete(self):
        """Returns empty list (not used in console)."""
        return []


class ConsoleOutputWriter(IOutputWriter):
    """Writes output to the computer terminal (text)."""

    def write_report(self, report_data: Dict):
        """Prints the report to the console screen."""
        print(f"Recorded: {report_data['name']} | "
              f"Category: {report_data['category']} | "
              f"Amount: {report_data['amount']}")