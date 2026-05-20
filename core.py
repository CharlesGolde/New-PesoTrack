"""
================================================================================
                             Core Business Logic Module.
================================================================================

This module contains the `FinanceManager` class, which acts as the primary
controller for the application's data. It handles file I/O (CSV persistence),
transaction management (CRUD operations), and financial calculations.

The module relies on the `models` module for data encapsulation and the
standard `csv` library for persistence.

================================================================================
"""

import csv
import os
from datetime import datetime
from typing import List, Dict
from models import Transaction


class FinanceManager:
    """
    Manages financial transactions and data persistence.

    The FinanceManager is responsible for:
    - Loading and saving transaction data to a CSV file.
    - Adding, deleting, and clearing transactions.
    - Calculating totals and category breakdowns.

    Attributes:
        reader (IInputReader): Strategy object for reading input.
        writer (IOutputWriter): Strategy object for writing output.
        _transactions (List[Transaction]): Internal list of transaction objects.
        filename (str): Path to the CSV storage file.
    """

    def __init__(self, input_reader, output_writer, filename="expenses.csv"):
        """
        Initializes the FinanceManager.

        Args:
            input_reader (IInputReader): An object that implements the input strategy.
            output_writer (IOutputWriter): An object that implements the output strategy.
            filename (str, optional): The name of the CSV file. Defaults to "expenses.csv".
        """
        self.reader = input_reader
        self.writer = output_writer
        self._transactions: List[Transaction] = []
        self.filename = filename

    def load_from_csv(self):
        """
        Loads transactions from the CSV file into memory.

        If the file does not exist, it creates a new file with the header row.
        It iterates through rows, converting them into Transaction objects.
        Rows with invalid data are skipped to prevent crashes.

        Returns:
            None
        """
        if not os.path.exists(self.filename):
            # Create CSV with header if missing
            with open(self.filename, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['date', 'name', 'category', 'amount'])
            return

        with open(self.filename, 'r', newline='') as f:
            reader = csv.DictReader(f)
            self._transactions = []
            for row in reader:
                try:
                    t = Transaction(row['date'], row['name'], row['category'], float(row['amount']))
                    self._transactions.append(t)
                except ValueError:
                    continue

    def save_to_csv(self):
        """
        Saves the current list of transactions to the CSV file.

        This overwrites the existing file to ensure data consistency.

        Returns:
            None
        """
        with open(self.filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['date', 'name', 'category', 'amount'])
            for t in self._transactions:
                writer.writerow([t.date, t.name, t.category, t.amount])

    def add_expense(self, transaction: Transaction):
        """
        Adds a new transaction to the internal list.

        Args:
            transaction (Transaction): The valid Transaction object to add.

        Returns:
            None
        """
        self._transactions.append(transaction)

    def delete_expenses(self, ids_to_delete):
        """
        Deletes transactions based on their index IDs.

        Args:
            ids_to_delete (List[str]): A list of string IDs (e.g., "row_0").

        Returns:
            None

        Notes:
            Indices are sorted in descending order before deletion to prevent
            index shifting issues when popping from the list.
        """
        try:
            ids_to_delete = [int(id_str.split('_')[1]) for id_str in ids_to_delete]
            # Sort descending to pop from back
            for index in sorted(ids_to_delete, reverse=True):
                if 0 <= index < len(self._transactions):
                    self._transactions.pop(index)
        except (ValueError, IndexError):
            pass

    def clear_all(self):
        """
        Clears all transactions from memory.

        Returns:
            None
        """
        self._transactions = []

    def get_total_amount(self):
        """
        Calculates the sum of all transaction amounts.

        Returns:
            float: The total expense amount.
        """
        return sum(t.amount for t in self._transactions)

    def get_category_breakdown(self) -> Dict[str, float]:
        """
        Aggregates expenses by category.

        Iterates through transactions and sums amounts for each unique category.

        Returns:
            Dict[str, float]: A dictionary where keys are category names
            and values are the total amounts for that category.
        """
        breakdown = {}
        for t in self._transactions:
            cat = t.category
            breakdown[cat] = breakdown.get(cat, 0) + t.amount
        return breakdown