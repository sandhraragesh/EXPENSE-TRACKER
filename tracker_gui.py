import csv
import os
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt

FILE_NAME = "expenses.csv"

# Create CSV if not exists
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Amount", "Category", "Description"])

def add_expense():
    amount = entry_amount.get()
    category = entry_category.get()
    description = entry_desc.get()

    if amount and category and description:
        try:
            amt = float(amount)
            with open(FILE_NAME, "a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([amt, category, description])
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

    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            tree.insert("", tk.END, values=row)

def show_total():
    total = 0
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            total += float(row[0])
    messagebox.showinfo("Total Expense", f"💰 Total = {total}")

def chart_by_category():
    categories = {}
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            categories[row[1]] = categories.get(row[1], 0) + float(row[0])
    if categories:
        plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
        plt.title("Expenses by Category")
        plt.show()
    else:
        messagebox.showinfo("No Data", "No expenses found!")

def chart_over_time():
    amounts = []
    with open(FILE_NAME, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            amounts.append(float(row[0]))
    if amounts:
        plt.plot(range(1, len(amounts) + 1), amounts, marker="o")
        plt.title("Expenses Over Time")
        plt.xlabel("Entry Number")
        plt.ylabel("Amount")
        plt.show()
    else:
        messagebox.showinfo("No Data", "No expenses found!")

# ------------------ GUI ------------------
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("600x500")

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
tk.Button(root, text="Category Chart", command=chart_by_category, bg="orange").pack(pady=5)
tk.Button(root, text="Time Chart", command=chart_over_time, bg="pink").pack(pady=5)

# Table for expenses
tree = ttk.Treeview(root, columns=("Amount", "Category", "Description"), show="headings")
tree.heading("Amount", text="Amount")
tree.heading("Category", text="Category")
tree.heading("Description", text="Description")
tree.pack(fill=tk.BOTH, expand=True, pady=10)

load_expenses()

root.mainloop()
