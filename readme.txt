Finance Tracker Application
Overview
The Finance Tracker application is a desktop application built using Python and Tkinter. It helps users manage their finances by allowing them to track their income and expenses, categorize transactions, and visualize their financial data. This application consists of a user-friendly interface that includes various features such as adding, editing, and deleting categories, recording income and expenses, and viewing balance and cost estimates.

Features
Add, Edit, and Delete Categories: Users can manage categories to classify their financial transactions.
Record Income and Expenses: Users can add income and expense records, specifying the date, category, and amount.
View Balance: Users can view a table of all recorded transactions.
Cost Estimate: Users can add and manage estimated costs.
Visualize Data: Users can see graphical representations of their income and expenses over time.

Dependencies
Python 3.x
Tkinter
Pandas
Matplotlib

Installation

Clone the repository:
git clone https://github.com/zzizyte/capstone_project.git
cd finance-tracker

Install the required packages:
pip install pandas matplotlib

Run the application:
python finance_tracker.py

Usage
Main Application Interface
Tabs: The application has three main tabs - Main, Balance, and Cost Estimate.

Main Tab: Users can add income and expenses. A graph visualizing income and expenses over time is displayed.
Balance Tab: Displays a table of all recorded transactions. Users can add new transactions or edit/delete existing ones.
Cost Estimate Tab: Users can add estimated costs and manage existing ones.
Menu: The menu at the top provides options to manage categories.

Add Category: Opens a window to add a new category.
Edit Category: Opens a window to edit an existing category.
Delete Category: Opens a window to delete a category.
Adding Transactions
Income: Enter the date, select the "Income" category, and enter the amount. Click "Add to Balance" to record the income.
Expenses: Enter the date, select a category, enter the amount, and click "Add Expense" to record the expense.
Managing Categories
Add New Category: Open the "Add New Category" window from the menu, enter the category name, and click "Add".
Edit Category: Open the "Edit Category" window from the menu, select the category to edit, enter the new name, and click "Save".
Delete Category: Open the "Delete Category" window from the menu, select the category to delete, and click "Delete".


To do
Fix pyplot backdate
Add filter for the tables
Refactor duplicate functions
Rename function and variables to be more understandable
Add expenses and estimate cost comparison
Add input validation

