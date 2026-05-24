# PesoTrack 💰

[![Python](https://img.shields.io/badge/Python-80.3%25-3776ab?logo=python&logoColor=white)](https://www.python.org/)
[![HTML](https://img.shields.io/badge/HTML-19.7%25-e34c26?logo=html5&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/HTML)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub](https://img.shields.io/badge/GitHub-CharlesGolde-blue?logo=github)](https://github.com/Clarky-Masarap)

**License:** [MIT License](LICENSE)

A lightweight, web-based personal finance tracker built with Python. Track your expenses, categorize spending, and calculate savings all in one place. Perfect for managing your finances in Philippine Pesos (₱).

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

PesoTrack is a simple yet powerful personal finance management application designed to help you track expenses, monitor spending by category, and calculate your monthly savings potential. With a clean web interface and CSV-based data persistence, you can manage your finances without complex setup.

---

## ✨ Features

- **💳 Add Expenses**: Quickly log new transactions with date, name, category, and amount
- **📊 Category Breakdown**: View spending analysis by category (Food, Transport, Entertainment, etc.)
- **💾 Persistent Storage**: All data automatically saved to CSV for data portability
- **🗑️ Transaction Management**: Delete individual transactions or clear all data
- **💰 Savings Calculator**: Calculate potential savings based on income vs. total expenses
- **⚡ Real-time Updates**: Web interface updates instantly with your financial data
- **📈 Transaction History**: Complete history of all expenses in an easy-to-read format

---

## 🛠️ Tech Stack

### Backend
- **Python 3.x** - Core application logic
- **Built-in Libraries**:
  - `http.server` - Web server
  - `socketserver` - TCP server
  - `csv` - Data persistence
  - `datetime` - Date/time handling
  - `urllib.parse` - Form data parsing

### Frontend
- **HTML5** - User interface structure
- **CSS3** - Styling and responsive design
- **Form-based Input** - Simple HTML forms for data entry

### Data Storage
- **CSV (Comma-Separated Values)** - Lightweight, portable data format

### Architecture Pattern
- **Model-View-Controller (MVC)** - Separation of concerns
  - **Models** (`models.py`): Transaction data structure
  - **Core** (`core.py`): Business logic & finance management
  - **Strategies** (`strategies.py`): Input/output handlers
  - **App** (`app.py`): HTTP request handling & web interface

---

## 🚀 Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package manager)

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/CharlesGolde/New-PesoTrack.git
   cd New-PesoTrack
   ```

2. **No additional dependencies required**
   - PesoTrack uses only Python's built-in libraries

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - The app will automatically open in your default web browser
   - Navigate to `http://localhost:1246`

---

## 📖 Usage

### Adding an Expense
1. Fill in the transaction details:
   - **Date**: Transaction date (YYYY-MM-DD format)
   - **Name**: Description of the expense (e.g., "Lunch", "Gas")
   - **Category**: Spending category (e.g., "Food", "Transport")
   - **Amount**: Expense amount in Philippine Pesos (₱)
2. Click "Add Transaction"
3. The expense appears in your transaction history

### Viewing Transactions
- **Transaction List**: See all expenses with dates, descriptions, and amounts
- **Category Report**: View total spending broken down by category

### Calculating Savings
1. Enter your monthly income in the savings calculator
2. Click "Calculate Savings"
3. View your potential savings or budget warnings

### Managing Data
- **Delete Transaction**: Select checkbox next to a transaction and click "Delete"
- **Clear All**: Remove all transactions at once (use with caution)

---

## 📁 Project Structure

```
New-PesoTrack/
├── app.py                 # Main web server & HTTP request handler
├── core.py               # Finance manager & business logic
├── models.py             # Transaction data model
├── strategies.py         # Input/output reader and writer strategies
├── test_app.py           # Unit tests
├── index.html            # Web interface template
├── expenses.csv          # Data storage (auto-generated)
├── templates/            # Additional HTML templates
└── README.md             # This file
```

### File Descriptions

- **app.py**: Handles HTTP GET/POST requests, serves HTML, manages global application state
- **core.py**: `FinanceManager` class manages transactions, CSV operations, and financial calculations
- **models.py**: `Transaction` class with data validation for expenses
- **strategies.py**: `WebInputReader` and `WebOutputWriter` for handling web form data and HTML generation

---

## 🧪 Testing

Run the included test suite:

```bash
python test_app.py
```

Tests cover:
- Transaction creation and validation
- Financial calculations
- CSV persistence
- HTTP request handling

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

**MIT License Summary:**
- ✅ You may use, modify, and distribute this software
- ✅ You may use this in commercial projects
- ✅ You must include a copy of the license and copyright notice
- ❌ The software is provided "as is" without warranty

---

## 👥 Author

**PesoTrack** is developed by **TrioTech** (CharlesGolde)

---

## 💡 Future Enhancements

- 📱 Mobile-responsive design improvements
- 📊 Advanced analytics and charts
- 🔐 User authentication system
- 🌙 Dark mode theme
- 📧 Email expense summaries
- 💾 Database migration (SQLite/PostgreSQL)

---

## ❓ FAQ

**Q: Where is my data stored?**
A: Your data is stored in `expenses.csv` in the application directory. This file is auto-created on first run.

**Q: Can I export my data?**
A: Yes! Your `expenses.csv` file is portable and can be opened in Excel, Google Sheets, or any spreadsheet application.

**Q: Is my data secure?**
A: PesoTrack is a local application. Data remains on your machine. For sensitive financial data, consider running it on a secure private network.

**Q: Can I run this on a different port?**
A: Yes! Modify the `PORT` variable in `app.py` (currently set to 1246).

---

## 🙏 Support

For issues, feature requests, or questions, please open an issue on the [GitHub repository](https://github.com/CharlesGolde/New-PesoTrack/issues).

---

**Happy tracking! 💚₱**
