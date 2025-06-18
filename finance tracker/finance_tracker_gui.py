#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox
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

def add_transaction():
    t_type = type_var.get()
    try:
        amount = float(amount_var.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid number for amount.")
        return
    category = category_var.get().strip()
    description = description_var.get().strip()
    if not category or not description:
        messagebox.showerror("Missing Data", "Please fill out all fields.")
        return
    
    transaction = {
        'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'type': t_type,
        'amount': amount,
        'category': category,
        'description': description
    }
    transactions.append(transaction)
    save_transactions(transactions)
    messagebox.showinfo("Success", "Transaction added.")
    amount_var.set('')
    category_var.set('')
    description_var.set('')

def view_balance():
    balance = sum(t['amount'] if t['type']=='income' else -t['amount'] for t in transactions)
    messagebox.showinfo("Balance", f"Current balance: {balance:.2f}")

def view_transactions():
    win = tk.Toplevel(root)
    win.title("All Transactions")
    cols = ('Date', 'Type', 'Amount', 'Category', 'Description')
    tree = ttk.Treeview(win, columns=cols, show='headings')
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor='center')
    for t in transactions:
        tree.insert('', tk.END, values=(t['date'], t['type'], f"{t['amount']:.2f}", t['category'], t['description']))
    tree.pack(expand=True, fill='both')

# Load existing data
transactions = load_transactions()

# Main window
root = tk.Tk()
root.title("Personal Finance Tracker")
root.geometry("450x350")
root.resizable(False, False)

# Variables
type_var = tk.StringVar(value='expense')
amount_var = tk.StringVar()
category_var = tk.StringVar()
description_var = tk.StringVar()

# Layout
frame = ttk.Frame(root, padding="10")
frame.pack(expand=True, fill='both')

ttk.Label(frame, text="Type:").grid(row=0, column=0, sticky='e')
ttk.Combobox(frame, textvariable=type_var, values=('income', 'expense'), state='readonly').grid(row=0, column=1)

ttk.Label(frame, text="Amount:").grid(row=1, column=0, sticky='e')
ttk.Entry(frame, textvariable=amount_var).grid(row=1, column=1)

ttk.Label(frame, text="Category:").grid(row=2, column=0, sticky='e')
ttk.Entry(frame, textvariable=category_var).grid(row=2, column=1)

ttk.Label(frame, text="Description:").grid(row=3, column=0, sticky='e')
ttk.Entry(frame, textvariable=description_var).grid(row=3, column=1)

ttk.Button(frame, text="Add Transaction", command=add_transaction).grid(row=4, column=0, columnspan=2, pady=10)
ttk.Button(frame, text="View Balance", command=view_balance).grid(row=5, column=0, columnspan=2, pady=5)
ttk.Button(frame, text="View Transactions", command=view_transactions).grid(row=6, column=0, columnspan=2, pady=5)

root.mainloop()
