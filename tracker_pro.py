import csv
import os
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt
from datetime import datetime

current_user = None
FILE_NAME = None

def get_file():
    return f"expenses_{current_user}.csv"

def ensure_file():
    if not os.path.exists(get_file()):
        with open(get_file(), "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Amount", "Category", "Description", "Date"])

def add_expense():
    amount = entry_amount.get()
    category = entry_category.get()
    description = entry_desc.get()
    date = datetime.now().strftime("%Y-%m-%d")

    if amount and category and description:
        try:
            amt = float(amount)
            with open(get_file(), "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([amt, category, description, date])
            messagebox.showinfo("Success", "✅ Expense Added")
            entry_amount.delete(0, tk.END)
            entry_category.delete(0, tk.END)
            entry_desc.delete(0, tk.END)
            load_expenses()
        except ValueError:
            messagebox.showerror("Error", "Amount must be a number")
    else:
        messagebox.showerror("Error", "Please fill all fields")

def load_expenses():
    for row in tree.get_children():
        tree.delete(row)
    with open(get_file(), "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            tree.insert("", tk.END, values=row)

def show_total():
    total = 0
    with open(get_file(), "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            total += float(row[0])
    messagebox.showinfo("Total Expense", f"💰 Total = {total}")

def chart_by_category(month_only=False):
    categories = {}
    with open(get_file(), "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            amt, cat, desc, date = row
            if month_only:
                if date.startswith(datetime.now().strftime("%Y-%m")):
                    categories[cat] = categories.get(cat, 0) + float(amt)
            else:
                categories[cat] = categories.get(cat, 0) + float(amt)

    if categories:
        plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
        plt.title("Expenses by Category" + (" (This Month)" if month_only else ""))
        plt.show()
    else:
        messagebox.showinfo("No Data", "No expenses found!")

def monthly_report():
    total = 0
    with open(get_file(), "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            amt, cat, desc, date = row
            if date.startswith(datetime.now().strftime("%Y-%m")):
                total += float(amt)
    messagebox.showinfo("Monthly Report", f"📅 This Month's Expense = {total}")
    chart_by_category(month_only=True)

# ------------------ LOGIN SCREEN ------------------
def login_screen():
    def do_login():
        global current_user
        user = entry_user.get().strip().lower()
        if user:
            current_user = user
            ensure_file()
            login.destroy()
            main_screen()
        else:
            messagebox.showerror("Error", "Enter a username")

    login = tk.Tk()
    login.title("Login - Expense Tracker")
    login.geometry("300x200")

    tk.Label(login, text="Enter Username:", font=("Arial", 12)).pack(pady=10)
    entry_user = tk.Entry(login)
    entry_user.pack(pady=5)

    tk.Button(login, text="Login", command=do_login, bg="lightgreen").pack(pady=20)
    login.mainloop()

# ------------------ MAIN APP ------------------
def main_screen():
    global entry_amount, entry_category, entry_desc, tree

    root = tk.Tk()
    root.title(f"Expense Tracker - {current_user}")
    root.geometry("700x600")

    # Input fields
    tk.Label(root, text="Amount:").pack()
    entry_amount = tk.Entry(root)
    entry_amount.pack()

    tk.Label(root, text="Category:").pack()
    entry_category = tk.Entry(root)
    entry_category.pack()

    tk.Label(root, text="Description:").pack()
    entry_desc = tk.Entry(root)
    entry_desc.pack()

    tk.Button(root, text="Add Expense", command=add_expense, bg="lightgreen").pack(pady=5)
    tk.Button(root, text="Show Total", command=show_total, bg="lightblue").pack(pady=5)
    tk.Button(root, text="Category Chart", command=lambda: chart_by_category(False), bg="orange").pack(pady=5)
    tk.Button(root, text="Monthly Report", command=monthly_report, bg="pink").pack(pady=5)

    # Table
    tree = ttk.Treeview(root, columns=("Amount", "Category", "Description", "Date"), show="headings")
    for col in ("Amount", "Category", "Description", "Date"):
        tree.heading(col, text=col)
    tree.pack(fill=tk.BOTH, expand=True, pady=10)

    load_expenses()
    root.mainloop()

# Start app
login_screen()

