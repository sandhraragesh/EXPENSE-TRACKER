import csv
import os
import matplotlib.pyplot as plt

FILE_NAME = "expenses.csv"

# Create CSV file with headers if it doesn't exist
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Amount", "Category", "Description"])

def add_expense(amount, category, description):
    with open(FILE_NAME, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([amount, category, description])
    print("✅ Expense added successfully!")

def show_expenses():
    print("\n--- All Expenses ---")
    with open(FILE_NAME, mode="r") as file:
        reader = csv.reader(file)
        next(reader)
        for i, row in enumerate(reader, 1):
            print(f"{i}. {row[0]} - {row[1]} - {row[2]}")

def total_expense():
    total = 0
    with open(FILE_NAME, mode="r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            total += float(row[0])
    print(total)

def expense_by_category():
    categories = {}
    with open(FILE_NAME, mode="r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            categories[row[1]] = categories.get(row[1], 0) + float(row[0])

    # Pie chart
    if categories:
        plt.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
        plt.title("Expenses by Category")
        plt.show()
    else:
        print("❌ No expenses to show chart.")

def expense_over_time():
    amounts = []
    with open(FILE_NAME, mode="r") as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            amounts.append(float(row[0]))

    # Line chart
    if amounts:
        plt.plot(range(1, len(amounts)+1), amounts, marker="o")
        plt.title("Expenses Over Time")
        plt.xlabel("Entry Number")
        plt.ylabel("Amount")
        plt.show()
    else:
        print("❌ No expenses to show chart.")

# Menu
while True:
    print("\nExpense Tracker Menu")
    print("1. Add Expense")
    print("2. Show Expenses")
    print("3. Show Total")
    print("4. Expense by Category (Chart)")
    print("5. Expense Over Time (Chart)")
    print("6. Exit")
    choice = input("Enter choice: ")

    if choice == "1":
        amt = float(input("Enter amount: "))
        cat = input("Enter category: ")
        desc = input("Enter description: ")
        add_expense(amt, cat, desc)
    elif choice == "2":
        show_expenses()
    elif choice == "3":
        print("💰 Total Expense = ", total_expense())
    elif choice == "4":
        expense_by_category()
    elif choice == "5":
        expense_over_time()
    elif choice == "6":
        print("Goodbye 👋")
        break
    else:
        print("❌ Invalid choice! Try again.")
