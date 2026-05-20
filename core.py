import csv
import os
from datetime import datetime
from typing import List, Dict
from models import Transaction

class FinanceManager:
    def __init__(self, input_reader, output_writer, filename="expenses.csv"):
        self.reader = input_reader
        self.writer = output_writer
        self._transactions: List[Transaction] = []
        self.filename = filename

    def load_from_csv(self):
        """Loads transactions from CSV. Creates file if missing."""
        if not os.path.exists(self.filename):
            # Automatic CSV File Maker
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
        """Saves current transactions to CSV."""
        with open(self.filename, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['date', 'name', 'category', 'amount'])
            for t in self._transactions:
                writer.writerow([t.date, t.name, t.category, t.amount])

    def add_expense(self, transaction: Transaction):
        self._transactions.append(transaction)

    def delete_expenses(self, ids_to_delete):
        # IDs in HTML are strings like "row_0", "row_1"
        # We map them to the list index
        try:
            ids_to_delete = [int(id_str.split('_')[1]) for id_str in ids_to_delete]
            # Sort in descending order to remove from back without shifting indices
            for index in sorted(ids_to_delete, reverse=True):
                if 0 <= index < len(self._transactions):
                    self._transactions.pop(index)
        except (ValueError, IndexError):
            pass

    def clear_all(self):
        self._transactions = []

    def get_total_amount(self):
        # Sum of all amounts (Expenses only)
        return sum(t.amount for t in self._transactions)

    # FEATURE: Expenses Report Logic
    def get_category_breakdown(self) -> Dict[str, float]:
        """Returns a dictionary of category -> total amount."""
        breakdown = {}
        for t in self._transactions:
            cat = t.category
            breakdown[cat] = breakdown.get(cat, 0) + t.amount
        return breakdown