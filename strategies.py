from abc import ABC, abstractmethod
from typing import List, Dict
from models import Transaction
from datetime import datetime

# --- Interfaces ---
class IInputReader(ABC):
    @abstractmethod
    def get_transactions(self) -> List[Transaction]:
        pass

    def get_ids_to_delete(self) -> List[str]:
        pass

class IOutputWriter(ABC):
    @abstractmethod
    def write_report(self, report_data: Dict):
        pass

# --- Web Implementations (HTML) ---
class WebInputReader(IInputReader):
    def __init__(self, post_data: Dict):
        self.post_data = post_data

    def get_transactions(self) -> List[Transaction]:
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
        return self.post_data.get('ids', [])

class WebOutputWriter(IOutputWriter):
    def __init__(self):
        self.html_content = ""
        self.row_counter = 0

    def write_report(self, report_data: Dict):
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

    # NEW FEATURE: HTML Generator for Category Report
    def write_category_report(self, breakdown: Dict[str, float]):
        if not breakdown:
            self.html_content += "<li style='color: #64748b; text-align: center;'>No data to report</li>"
            return

        for cat, total in breakdown.items():
            self.html_content += f"""
            <li>
                <span style="color: #e2e8f0; font-weight: 700;">{cat}</span>
                <span class="text-gold">&#8369;{total:.2f}</span>
            </li>
            """

    def get_html(self):
        return self.html_content

# --- Console Implementations (For Testing) ---
class ConsoleInputReader(IInputReader):
    def get_transactions(self) -> List[Transaction]:
        print("\n--- Enter Transaction Details ---")
        date = input("Date (YYYY-MM-DD, leave blank for today): ")
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")
        name = input("Name: ")
        category = input("Category: ")
        amt = float(input("Amount: "))
        return [Transaction(date, name, category, amt)]

    def get_ids_to_delete(self):
        return []

class ConsoleOutputWriter(IOutputWriter):
    def write_report(self, report_data: Dict):
        print(f"Recorded: {report_data['name']} | "
              f"Category: {report_data['category']} | "
              f"Amount: {report_data['amount']}")