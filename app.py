"""
================================================================================
                    Main Application Module for PesoTrack.
================================================================================

This module serves as the entry point for the PesoTrack web application.
It sets up a local HTTP server using Python's built-in `http.server` library
and handles the request/response cycle between the user's browser and the
backend logic.

The application uses a Global State pattern to persist data in memory between
requests, storing the current totals, HTML snippets, and calculation results.

Dependencies:
    - http.server: For creating the web server.
    - webbrowser: To automatically launch the user's browser.
    - core: Contains the FinanceManager business logic.
    - strategies: Contains Input/Output handling strategies.

================================================================================
"""

import http.server
import socketserver
import webbrowser
import urllib.parse
import os
from core import FinanceManager
from strategies import WebInputReader, WebOutputWriter

# --- Global Variables ---
# These store the current data to show on the website.

current_total = 0.0
"""float: The total amount of all expenses."""

transaction_history_html = ""
"""str: The HTML code for the list of transactions."""

category_report_html = ""
"""str: The HTML code for the category report."""

savings_amount = 0.0
"""float: The calculated savings amount."""

savings_display = "none"
"""str: Controls if the savings box is visible ('none' or 'block')."""

savings_class = ""
"""str: The style class for the savings result ('positive' or 'negative')."""

savings_message = ""
"""str: The message telling the user how much they saved."""


class PesoTrackHandler(http.server.BaseHTTPRequestHandler):
    """
    Web Request Handler.

    This class decides what to do when a user visits the site or clicks a button.
    """

    def do_GET(self):
        """
        Runs when the user opens or refreshes the page.

        It loads the data, creates the HTML, and sends the page to the browser.
        """
        global current_total, transaction_history_html, category_report_html
        global savings_amount, savings_display, savings_class, savings_message

        # 1. Load the data manager
        manager = FinanceManager(None, None)
        manager.load_from_csv()

        # 2. Calculate totals
        current_total = manager.get_total_amount()

        # 3. Create the HTML for the transaction list
        writer = WebOutputWriter()
        for t in manager._transactions:
            writer.write_report(t.to_dict())
        transaction_history_html = writer.get_html()

        # 4. Create the HTML for the category report
        report_writer = WebOutputWriter()
        breakdown = manager.get_category_breakdown()
        report_writer.write_category_report(breakdown)
        category_report_html = report_writer.get_html()

        # 5. Read the HTML file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        try:
            # encoding="utf-8" ensures we read special characters correctly
            with open(os.path.join(script_dir, "index.html"), "r", encoding="utf-8") as f:
                html_content = f.read()
        except FileNotFoundError:
            self.send_error(404, "index.html not found")
            return

        # 6. Put the data into the HTML
        html_content = html_content.replace("{{TOTAL_AMOUNT}}", f"{current_total:.2f}")
        html_content = html_content.replace("{{TRANSACTIONS}}", transaction_history_html)
        html_content = html_content.replace("{{CATEGORY_REPORT}}", category_report_html)

        # Put savings data in
        html_content = html_content.replace("{{SAVINGS_AMOUNT}}", f"{savings_amount:.2f}")
        html_content = html_content.replace("{{SAVINGS_DISPLAY}}", savings_display)
        html_content = html_content.replace("{{SAVINGS_CLASS}}", savings_class)
        html_content = html_content.replace("{{SAVINGS_MESSAGE}}", savings_message)

        # --- CHANGE TITLES ---
        # This changes the text in the HTML without editing the file manually
        html_content = html_content.replace("Category Report", "Expenses Report")
        html_content = html_content.replace("Savings Calculator", "Potential Saving Calculator")

        # 7. Send the page to the user
        self.send_response(200)

        # FIX: This tells the browser to read the Peso sign (₱) correctly
        self.send_header('Content-type', 'text/html; charset=utf-8')

        self.end_headers()
        self.wfile.write(html_content.encode())

    def do_POST(self):
        """
        Runs when the user clicks a button (Add, Delete, Clear, Calculate).

        It figures out which button was clicked and runs the correct logic.
        """
        global savings_amount, savings_display, savings_class, savings_message

        # Get the data sent from the form
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

        # Check what action to perform
        action = parsed_data.get('action', ['add'])[0]

        # Prepare the manager
        manager = FinanceManager(None, None)
        manager.load_from_csv()
        reader = WebInputReader(parsed_data)

        # Reset savings display
        savings_display = "none"

        # --- ACTION: ADD ---
        if action == 'add':
            new_transactions = reader.get_transactions()
            for t in new_transactions:
                manager.add_expense(t)
            manager.save_to_csv()

        # --- ACTION: DELETE ---
        elif action == 'delete':
            ids_to_delete = reader.get_ids_to_delete()
            manager.delete_expenses(ids_to_delete)
            manager.save_to_csv()

        # --- ACTION: CLEAR ---
        elif action == 'clear':
            manager.clear_all()
            manager.save_to_csv()

        # --- ACTION: CALCULATE SAVINGS ---
        elif action == 'calculate_savings':
            try:
                income = float(parsed_data.get('income', [0])[0])
                expenses = manager.get_total_amount()
                savings_amount = income - expenses

                if savings_amount >= 0:
                    savings_class = ""
                    # Use &#8369; (HTML code) to ensure Peso sign appears correctly
                    savings_message = f"Great job! You have potential savings of &#8369;{savings_amount:.2f}."
                else:
                    savings_class = "negative"
                    # Use &#8369; (HTML code) to ensure Peso sign appears correctly
                    savings_message = f"Warning: You are over budget by &#8369;{abs(savings_amount):.2f}."
                    savings_amount = 0.0

                savings_display = "block"
            except ValueError:
                savings_display = "none"

        # Refresh the page
        self.send_response(303)
        self.send_header('Location', '/')
        self.end_headers()


if __name__ == "__main__":
    """Starts the server."""
    PORT = 1246
    print(f"Peso Track by TrioTech running at http://localhost:{PORT}")
    webbrowser.open(f'http://localhost:{PORT}')

    with socketserver.TCPServer(("", PORT), PesoTrackHandler) as httpd:
        httpd.serve_forever()