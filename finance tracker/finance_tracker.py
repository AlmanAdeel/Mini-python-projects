#!/usr/bin/env python3
import json
import os
from datetime import datetime

DATA_FILE = 'transactions.json'

def load_transactions():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_transactions(transactions):
    with open(DATA_FILE, 'w') as f:
        json.dump(transactions, f, indent=4)

def add_transaction(transactions):
    t_type = input("Type (income/expense): ").strip().lower()
    if t_type not in ('income', 'expense'):
        print("Invalid type. Please enter 'income' or 'expense'.")
        return
    try:
        amount = float(input("Amount: ").strip())
    except ValueError:
        print("Invalid amount.")
        return
    category = input("Category: ").strip()
    description = input("Description: ").strip()
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transactions.append({
        'date': date,
        'type': t_type,
        'amount': amount,
        'category': category,
        'description': description
    })
    save_transactions(transactions)
    print("Transaction added.")

def view_balance(transactions):
    balance = sum(t['amount'] if t['type']=='income' else -t['amount']
                  for t in transactions)
    print(f"\nCurrent balance: {balance:.2f}")

def view_transactions(transactions):
    if not transactions:
        print("\nNo transactions recorded yet.")
        return
    print("\nAll Transactions:")
    for idx, t in enumerate(transactions, 1):
        print(f"{idx}. {t['date']} | {t['type'].capitalize():7} | "
              f"{t['amount']:8.2f} | {t['category']:10} | {t['description']}")

def main():
    transactions = load_transactions()
    while True:
        print("\n=== Personal Finance Tracker ===")
        print("1) Add transaction")
        print("2) View balance")
        print("3) View transactions")
        print("4) Exit")
        choice = input("Choose an option: ").strip()
        if choice == '1':
            add_transaction(transactions)
        elif choice == '2':
            view_balance(transactions)
        elif choice == '3':
            view_transactions(transactions)
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid option, please choose 1-4.")

if __name__ == '__main__':
    main()
