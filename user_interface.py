import tkinter as tk
from tkinter import ttk
from tkinter import *
from datetime import datetime
from finance_tracker import EstimateCost, Balance
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

balance = Balance()
estimateCost = EstimateCost(balance)


root = tk.Tk()
root.title("Finance tracker")
root.iconbitmap("finance.ico")
root.geometry("1200x900")

def show_notification(message, duration=3000):
    notification_window = tk.Toplevel(root)
    notification_window.title("Notification")
    notification_window.geometry("300x100")
    notification_window.resizable(False, False)
    tk.Label(notification_window, text=message, font=("Helvetica", 12)).pack(expand=True)
    root.after(duration, notification_window.destroy)


def add_new_category(new_user_category):
    """Adds new category to the list, calls successes message"""
    new_category_name = new_user_category.get()
    all_categories = list(balance.categories + balance.user_categories)
    if new_category_name not in all_categories:
        balance.add_category(new_category_name)
        show_notification("Category added successfully!")
    else:
        show_notification("Duplicate categories can not exist")  


def add_category_and_close(new_user_category, window):
    add_new_category(new_user_category)
    window.destroy() 


def open_add_category_window():
    add_category_window = tk.Toplevel(root)
    add_category_window.title("Add New Category")
    add_category_window.geometry("500x300")
    
    tk.Label(add_category_window, text="New Category Name:").pack(pady=10)
    new_user_category = tk.Entry(add_category_window)
    new_user_category.pack(pady=20)
    tk.Button(add_category_window, text="Add", command=lambda:add_category_and_close(new_user_category, add_category_window)).pack()
    tk.Label(add_category_window, text="Caution: the categories can not repeat", fg="red").pack(pady=20)
    all_categories = list(balance.categories + balance.user_categories)
    categories_text = ", ".join(all_categories)
    tk.Label(add_category_window, text=f"All Categories: {categories_text}").pack(pady=20)


def edit_category(edited_user_category, old_value):
    old_category = old_value.get()
    new_category = edited_user_category.get()
    if new_category not in (balance.categories + balance.user_categories):
        for i, category in enumerate(balance.user_categories):
            if category == old_category:
                balance.user_categories[i] = new_category          
        show_notification("Edited category saved successfully!")
    else:
        show_notification("Duplicate categories can not exist")


def edit_category_and_close(new_category_entry, old_value, window):
    edit_category(new_category_entry, old_value)
    window.destroy()    


def open_edit_category_window():
    edit_category_window = tk.Toplevel(root)
    edit_category_window.title("Edit Category")
    edit_category_window.geometry("500x300")
    
    tk.Label(edit_category_window, text="Select the Category to edit:").pack(pady=10)
    old_value = ttk.Combobox(edit_category_window, values=balance.user_categories, state='readonly')
    old_value.pack(pady=10)
    tk.Label(edit_category_window, text="Write a new category")
    edited_user_category = tk.Entry(edit_category_window)
    edited_user_category.pack(pady=20)
    tk.Button(edit_category_window, text="Save", command=lambda:edit_category_and_close(edited_user_category, old_value, edit_category_window)).pack()
    tk.Label(edit_category_window, text="Caution: the categories can not repeat", fg="red").pack(pady=20)


def delete_category(category_for_deletion):
    selected_category = category_for_deletion.get()
    balance.remove_category(selected_category)
    show_notification("Category deleted successfully!")


def delete_category_and_close(new_user_category, window):
    delete_category(new_user_category)
    window.destroy()     


def open_delete_category_window():
    delete_category_window = tk.Toplevel(root)
    delete_category_window.title("Edit Category")
    delete_category_window.geometry("500x300")
    
    tk.Label(delete_category_window, text="Select the Category for deletion:").pack(pady=10)
    category_for_deletion = ttk.Combobox(delete_category_window, values=balance.user_categories, state='readonly')
    category_for_deletion.pack(pady=10)
    tk.Button(delete_category_window, text="Delete", command=lambda:delete_category_and_close(category_for_deletion, delete_category_window)).pack()


# Create a Menu widget
menu = Menu(root)
root.config(menu=menu)
filemenu = Menu(menu, tearoff=0)
menu.add_cascade(label='Categories', menu=filemenu)
filemenu.add_command(label='Add category', command=open_add_category_window)
filemenu.add_command(label='Edit category', command=open_edit_category_window)
filemenu.add_command(label='Delete category', command=open_delete_category_window)

    
#tabs
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill='both')

tab1 = ttk.Frame(notebook)
tab2 = ttk.Frame(notebook)
tab3 = ttk.Frame(notebook)

notebook.add(tab1, text="Main")
notebook.add(tab2, text="Balance")
notebook.add(tab3, text="Cost Estimate")

def on_tab_change(event):
    selected_tab = event.widget.select()
    tab_text = event.widget.tab(selected_tab, "text")
    if tab_text == "Main":
        main_tab()
    elif tab_text == "Balance":
        balance_tab()
    elif tab_text == "Cost Estimate":
        estimate_tab()


notebook.bind("<<NotebookTabChanged>>", on_tab_change)


def balance_succsess_message(window):
    window.destroy()
    notification_window = tk.Toplevel(root)
    notification_window.title("Notification")
    notification_window.geometry("300x100")
    notification_window.resizable(False, False)
    tk.Label(notification_window, text="Added succsessfully!", font=("Helvetica", 12)).pack(expand=True)


def adding_new_line(date, category, amount, new_line_window):
    new_line = [
        date.get(),
        category.get(),
        amount.get(),
        0
    ]
    balance.add_new_line_to_file(new_line)


def adding_income_new_line(date, category, amount):
    new_line = [
        date.get(),
        category,
        amount.get(),
        0
    ]
    balance.add_new_line_to_file(new_line)
   
    
def balance_add_new_line_window():
    new_line_window = Toplevel(root)
    new_line_window.title("Add Balance")
    new_line_window.geometry("600x100")

    Label(new_line_window, text="Date").grid(row=0, column=0, padx=5, pady=5)
    date = tk.Entry(new_line_window)
    date.grid(row=0, column=1, padx=5, pady=5)

    Label(new_line_window, text="Category").grid(row=0, column=2, padx=5, pady=5)
    categories = balance.categories + balance.user_categories
    category = ttk.Combobox(new_line_window, values=categories, state='readonly')
    category.grid(row=0, column=3, padx=5, pady=5)

    Label(new_line_window, text="Amount").grid(row=0, column=4, padx=5, pady=5)
    amount = tk.Entry(new_line_window)
    amount.grid(row=0, column=5, padx=5, pady=5)

    Label(new_line_window, text="€ ").grid(row=0, column=6, padx=(0, 10), pady=5)
    
    button = tk.Button(new_line_window, text="Add", command=lambda: adding_new_line(date, category, amount, new_line_window))
    button.grid(row=1, column=0, columnspan=7, pady=10)
    
    
def balance_tab():
    global table_balance
    for widget in tab2.winfo_children():
        widget.destroy()
        
    df = balance.read_file()
    
    table_balance = ttk.Treeview(tab2, columns=balance.title, show='headings')
    for header in balance.title:
        table_balance.heading(header, text=header)
    table_balance.pack(expand=True, fill='both')

    for _, row in df.iterrows():
        values = [row[col] for col in balance.title]
        table_balance.insert('', tk.END, values=values)
        
    tk.Button(tab2, text="Add new", command=balance_add_new_line_window).pack()
    table_balance.bind('<Double-1>', open_edit_delete_window)

def edit_row_balance(date, category, amount, item_values, window):
    edited_line = [
        date.get(),
        category.get(),
        amount.get()
    ]
    balance.editing_row_of_file(item_values[0], edited_line)
    window.destroy()

def delete_row_balance(item_values, window):
    balance.deleting_line_from_file(item_values[0])
    window.destroy()
        
def open_edit_delete_window(event):
    selected_item = table_balance.selection()[0]
    item_values = table_balance.item(selected_item, 'values')
    edit_delete_row_window = tk.Toplevel(root)
    edit_delete_row_window.title("Edit Category")
    edit_delete_row_window.geometry("700x100")
    
    Label(edit_delete_row_window, text="Date").grid(row=0, column=0, padx=5, pady=5)
    date = tk.Entry(edit_delete_row_window)
    date.grid(row=0, column=1, padx=5, pady=5)
    date.insert(0, item_values[1])

    Label(edit_delete_row_window, text="Category").grid(row=0, column=2, padx=5, pady=5)
    categories = balance.categories + balance.user_categories
    category = ttk.Combobox(edit_delete_row_window, values=categories, state='readonly')
    category.grid(row=0, column=3, padx=5, pady=5)
    category.set(item_values[2])

    Label(edit_delete_row_window, text="Amount").grid(row=0, column=4, padx=5, pady=5)
    amount = tk.Entry(edit_delete_row_window)
    amount.grid(row=0, column=5, padx=5, pady=5)
    amount.insert(0, item_values[3])

    Label(edit_delete_row_window, text="€").grid(row=0, column=6, padx=(0, 10), pady=5)
    
    button = tk.Button(edit_delete_row_window, text="Save changes", command=lambda: edit_row_balance(date, category, amount, item_values, edit_delete_row_window))
    button.grid(row=1, column=1, columnspan=7, pady=10)
    button = tk.Button(edit_delete_row_window, text="Delete", command=lambda: delete_row_balance(item_values, edit_delete_row_window))
    button.grid(row=1, column=2, columnspan=7, pady=10)
    
def estimate_succsess_message(window):
    window.destroy()
    notification_window = tk.Toplevel(root)
    notification_window.title("Notification")
    notification_window.geometry("300x100")
    notification_window.resizable(False, False)
    tk.Label(notification_window, text="Added succsessfully!", font=("Helvetica", 12)).pack(expand=True)


def estimate_adding_new_line(date, category, amount, new_line_window):
    new_line = [
        date.get(),
        category.get(),
        amount.get()
    ]
    estimateCost.add_estimate_line_to_file(new_line)
    estimate_succsess_message(new_line_window)
    
    
def estimate_add_new_line_window():
    new_line_window = Toplevel(root)
    new_line_window.title("Add Balance")
    new_line_window.geometry("600x100")

    Label(new_line_window, text="Date").grid(row=0, column=0, padx=5, pady=5)
    date = tk.Entry(new_line_window)
    date.grid(row=0, column=1, padx=5, pady=5)

    Label(new_line_window, text="Category").grid(row=0, column=2, padx=5, pady=5)
    categories = balance.categories + balance.user_categories
    category = ttk.Combobox(new_line_window, values=categories, state='readonly')
    category.grid(row=0, column=3, padx=5, pady=5)

    Label(new_line_window, text="Amount").grid(row=0, column=4, padx=5, pady=5)
    amount = tk.Entry(new_line_window)
    amount.grid(row=0, column=5, padx=5, pady=5)

    Label(new_line_window, text="€ ").grid(row=0, column=6, padx=(0, 10), pady=5)
    
    button = tk.Button(new_line_window, text="Add", command=lambda: estimate_adding_new_line(date, category, amount, new_line_window))
    button.grid(row=1, column=0, columnspan=7, pady=10)


def estimate_edit_row_balance(date, category, amount, item_values, window):
    edited_line = [
        date.get(),
        category.get(),
        amount.get()
    ]
    estimateCost.edit_estimate_row_of_file(item_values[0], edited_line)
    window.destroy()

def estimate_delete_row_balance(item_values, window):
    estimateCost.delete_estimate_line_from_file(item_values[0])
    window.destroy()
        
def estimate_open_edit_delete_window(event):
    selected_item = table_estimate.selection()[0]
    item_values = table_estimate.item(selected_item, 'values')
    edit_delete_row_window = tk.Toplevel(root)
    edit_delete_row_window.title("Edit Category")
    edit_delete_row_window.geometry("700x100")
    
    Label(edit_delete_row_window, text="Date").grid(row=0, column=0, padx=5, pady=5)
    date = tk.Entry(edit_delete_row_window)
    date.grid(row=0, column=1, padx=5, pady=5)
    date.insert(0, item_values[1])

    Label(edit_delete_row_window, text="Category").grid(row=0, column=2, padx=5, pady=5)
    categories = balance.categories + balance.user_categories
    category = ttk.Combobox(edit_delete_row_window, values=categories, state='readonly')
    category.grid(row=0, column=3, padx=5, pady=5)
    category.set(item_values[2])

    Label(edit_delete_row_window, text="Amount").grid(row=0, column=4, padx=5, pady=5)
    amount = tk.Entry(edit_delete_row_window)
    amount.grid(row=0, column=5, padx=5, pady=5)
    amount.insert(0, item_values[3])

    Label(edit_delete_row_window, text="€").grid(row=0, column=6, padx=(0, 10), pady=5)
    
    button = tk.Button(edit_delete_row_window, text="Save changes", command=lambda: estimate_edit_row_balance(date, category, amount, item_values, edit_delete_row_window))
    button.grid(row=1, column=1, columnspan=7, pady=10)
    button = tk.Button(edit_delete_row_window, text="Delete", command=lambda: estimate_delete_row_balance(item_values, edit_delete_row_window))
    button.grid(row=1, column=2, columnspan=7, pady=10)


def estimate_tab():
    global table_estimate
    for widget in tab3.winfo_children():
        widget.destroy()
    df = estimateCost.read_estimate_csv_file()
    table_estimate = ttk.Treeview(tab3, columns=estimateCost.title, show='headings')
    for header in estimateCost.title:
        table_estimate.heading(header, text=header)
    table_estimate.pack(expand=True, fill='both')

    for _, row in df.iterrows():
        values = [row[col] for col in estimateCost.title]
        table_estimate.insert('', tk.END, values=values)
    tk.Button(tab3, text="Add new", command=estimate_add_new_line_window).pack()
    table_estimate.bind('<Double-1>', estimate_open_edit_delete_window)   


def adding_expenses_new_line(date, category, amount):
    new_line = [
        date.get(),
        category.get(),
        amount.get(),
        0
    ]
    balance.add_new_line_to_file(new_line)


def adding_income_new_line(date, category, amount):
    new_line = [
        date.get(),
        category,
        amount.get(),
        0
    ]
    balance.add_new_line_to_file(new_line)    
    
def main_tab():
    for widget in tab1.winfo_children():
        widget.destroy()



    total_balance = balance.count_balance()
    total_balance_label = tk.Label(
        tab1, text=f"Total Balance: {total_balance} €", font=("Helvetica", 16, "bold"), bg="#f0f0f0"
    )
    total_balance_label.grid(row=0, column=0, padx=20, pady=20, columnspan=6, sticky="ew")


    today_date = datetime.now().strftime("%Y-%m-%d")

    tk.Label(tab1, text="Date:", font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
    add_date_entry = tk.Entry(tab1, font=("Helvetica", 12))
    add_date_entry.insert(0, today_date)
    add_date_entry.grid(row=1, column=1, padx=10, pady=10, sticky="w")

    tk.Label(tab1, text="Add Balance:", font=("Helvetica", 12)).grid(row=1, column=2, padx=10, pady=10, sticky="e")
    add_balance_entry = tk.Entry(tab1, font=("Helvetica", 12))
    add_balance_entry.grid(row=1, column=3, padx=10, pady=10, sticky="w")
    euro_sign_label = tk.Label(tab1, text="€", font=("Helvetica", 12))
    euro_sign_label.grid(row=1, column=4, padx=5, pady=10, sticky="w")

    add_balance_button = tk.Button(
        tab1, text="Add to Balance", command=lambda: adding_income_new_line(add_date_entry, "Income", add_balance_entry),
        font=("Helvetica", 12), bg="#99F471", fg="black"
    )
    add_balance_button.grid(row=1, column=5, padx=10, pady=10)


    tk.Label(tab1, text="Date:", font=("Helvetica", 12)).grid(row=2, column=0, padx=10, pady=10, sticky="e")
    expense_date_entry = tk.Entry(tab1, font=("Helvetica", 12))
    expense_date_entry.insert(0, today_date)
    expense_date_entry.grid(row=2, column=1, padx=10, pady=10, sticky="w")

    tk.Label(tab1, text="Category:", font=("Helvetica", 12)).grid(row=2, column=2, padx=10, pady=10, sticky="e")
    categories = balance.categories + balance.user_categories
    categories.remove("Income")
    expense_category_entry = ttk.Combobox(tab1, values=categories, state='readonly', font=("Helvetica", 12))
    expense_category_entry.grid(row=2, column=3, padx=10, pady=10, sticky="w")

    tk.Label(tab1, text="Amount:", font=("Helvetica", 12)).grid(row=2, column=4, padx=10, pady=10, sticky="e")
    expense_amount_entry = tk.Entry(tab1, font=("Helvetica", 12))
    expense_amount_entry.grid(row=2, column=5, padx=10, pady=10, sticky="w")

    tk.Label(tab1, text="€", font=("Helvetica", 12)).grid(row=2, column=6, padx=10, pady=10, sticky="w")

    expense_add_button = tk.Button(
        tab1, text="Add Expense", command=lambda: adding_expenses_new_line(expense_date_entry, expense_category_entry, expense_amount_entry),
        font=("Helvetica", 12), bg="#FF6961", fg="black"
    )
    expense_add_button.grid(row=2, column=7, padx=10, pady=10)


    df = balance.read_file()
    df['Date'] = pd.to_datetime(df['Date'])
    df['Cumulative_Balance'] = df['Balance']
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['Date'], df['Cumulative_Balance'], marker='o', color='green', label='Cumulative Balance')
    ax.set_xlabel('Date')
    ax.set_ylabel('Balance Amount')
    ax.set_title('Cumulative Balance Over Time')
    ax.legend()
    canvas = FigureCanvasTkAgg(fig, master=tab1)
    canvas.draw()
    canvas.get_tk_widget().grid(row=3, column=0, columnspan=8, padx=10, pady=10, sticky="nsew")

   
root.mainloop()