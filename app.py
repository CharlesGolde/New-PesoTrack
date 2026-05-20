
import http.server
import socketserver
import webbrowser
import urllib.parse
import os
from core import FinanceManager
from strategies import WebInputReader, WebOutputWriter

# Global state
current_total = 0.0
transaction_history_html = ""
category_report_html = ""
# Savings state
savings_amount = 0.0
savings_display = "none"
savings_class = ""
savings_message = ""


class PesoTrackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        """Serve the HTML page."""
        global current_total, transaction_history_html, category_report_html
        global savings_amount, savings_display, savings_class, savings_message

        # Reset savings display on fresh load (optional, keeps it sticky currently)

        manager = FinanceManager(None, None)
        manager.load_from_csv()

        current_total = manager.get_total_amount()

        # Generate Transaction List
        writer = WebOutputWriter()
        for t in manager._transactions:
            writer.write_report(t.to_dict())
        transaction_history_html = writer.get_html()

        # Generate Category Report
        report_writer = WebOutputWriter()
        breakdown = manager.get_category_breakdown()
        report_writer.write_category_report(breakdown)
        category_report_html = report_writer.get_html()

        # Read HTML
        script_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            with open(os.path.join(script_dir, "index.html"), "r") as f:
                html_content = f.read()
        except FileNotFoundError:
            self.send_error(404, "index.html not found")
            return

        # Inject Data
        html_content = html_content.replace("{{TOTAL_AMOUNT}}", f"{current_total:.2f}")
        html_content = html_content.replace("{{TRANSACTIONS}}", transaction_history_html)

        # Inject Report & Savings
        html_content = html_content.replace("{{CATEGORY_REPORT}}", category_report_html)
        html_content = html_content.replace("{{SAVINGS_AMOUNT}}", f"{savings_amount:.2f}")
        html_content = html_content.replace("{{SAVINGS_DISPLAY}}", savings_display)
        html_content = html_content.replace("{{SAVINGS_CLASS}}", savings_class)
        html_content = html_content.replace("{{SAVINGS_MESSAGE}}", savings_message)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode())

    def do_POST(self):
        """Handle Form Submission (Add, Delete, Clear, Calculate)."""
        global current_total, transaction_history_html, category_report_html
        global savings_amount, savings_display, savings_class, savings_message

        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

        action = parsed_data.get('action', ['add'])[0]

        manager = FinanceManager(None, None)
        manager.load_from_csv()
        reader = WebInputReader(parsed_data)

        # Reset savings display on new action
        savings_display = "none"

        if action == 'add':
            new_transactions = reader.get_transactions()
            for t in new_transactions:
                manager.add_expense(t)
            manager.save_to_csv()

        elif action == 'delete':
            ids_to_delete = reader.get_ids_to_delete()
            manager.delete_expenses(ids_to_delete)
            manager.save_to_csv()

        elif action == 'clear':
            manager.clear_all()
            manager.save_to_csv()

        # FEATURE: Handle Savings Calculation
        elif action == 'calculate_savings':
            try:
                income = float(parsed_data.get('income', [0])[0])
                expenses = manager.get_total_amount()
                savings_amount = income - expenses

                if savings_amount >= 0:
                    savings_class = ""
                    savings_message = f"Great job! You have potential savings of ₱{savings_amount:.2f}."
                else:
                    savings_class = "negative"
                    savings_message = f"Warning: You are over budget by ₱{abs(savings_amount):.2f}."
                    savings_amount = 0.0  # Show 0 savings if negative

                savings_display = "block"
            except ValueError:
                savings_display = "none"

        # Redirect back to Home
        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()


if __name__ == "__main__":
    PORT = 1246
    print(f"Peso Track by TrioTech running at http://localhost:{PORT}")
    webbrowser.open(f'http://localhost:{PORT}')

    with socketserver.TCPServer(("", PORT), PesoTrackHandler) as httpd:
        httpd.serve_forever()