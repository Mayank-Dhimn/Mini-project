import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from datetime import datetime
from tkcalendar import DateEntry
import sqlite3
import matplotlib.pyplot as plt

from sorts import bubble_sort, insertion_sort, merge_sort, quick_sort
from db import insert_inventory
from db import (
    get_inventory,
    insert_inventory,
    insert_sort_log,
    setup_database,
)


# --------------------------------------------
# DATABASE HELPER FUNCTION
# --------------------------------------------
# def get_inventory():
#     conn = sqlite3.connect("inventory.db")
#     c = conn.cursor()
#     c.execute("SELECT product_name, category, price, quantity, expiry_days FROM inventory")
#     rows = c.fetchall()
#     conn.close()
#     return rows


# --------------------------------------------
# SORTING ANALYZER - Sorts inventory data
# --------------------------------------------
def sort_data():
    rows = get_inventory()
    if not rows:
        messagebox.showwarning("No Data", "No products in inventory yet!")
        return

    algo = algo_var.get()

    # 1️⃣ Sort real inventory data by expiry days
    data = [r[4] for r in rows]
    if algo == "Bubble":
        sorted_data, t = bubble_sort(data)
    elif algo == "Quick":
        sorted_data, t = quick_sort(data)
    elif algo == "Insertion":
        sorted_data, t = insertion_sort(data)
    else:  # Merge
        sorted_data, t = merge_sort(data)

    # Show results for your actual inventory
    sorted_pairs = sorted(zip(sorted_data, [r[0] for r in rows]))
    result_text = "\n".join([f"{p}: {d} days" for d, p in sorted_pairs])
    messagebox.showinfo("Sorting Done", f"{algo} Sort finished in {t:.4f}s\n\nSorted by expiry:\n{result_text}")

    # 2️⃣ DAA Demonstration: test all algorithms on a large dataset
    large_data = np.random.randint(1, 10000, size=1000).tolist()
    algorithms = {
        "Bubble": bubble_sort,
        "Quick": quick_sort,
        "Insertion": insertion_sort,
        "Merge": merge_sort
    }

    times = []
    for name, func in algorithms.items():
        _, elapsed = func(large_data)
        times.append((name, elapsed))

    # 3️⃣ Show results in console (optional)
    print("\nDAA Performance Test:")
    for name, t in times:
        print(f"{name} Sort: {t:.4f}s")






# --------------------------------------------
# ADD INVENTORY ITEM
# --------------------------------------------
def add_inventory():
    try:
        expiry_input = expiry_entry.get().strip()

        # Convert date → days until expiry
        if "-" in expiry_input:
            expiry_date = datetime.strptime(expiry_input, "%Y-%m-%d")
            today = datetime.today()
            expiry_days = (expiry_date - today).days
        else:
            expiry_days = int(expiry_input)

        insert_inventory(
            prod_entry.get(),
            cat_entry.get(),
            float(price_entry.get()),
            int(qty_entry.get()),
            expiry_days
        )

        messagebox.showinfo("Saved", "Product added to database!")

    except Exception as e:
        messagebox.showerror("Error", str(e))


# --------------------------------------------
# CHECK REORDER / EXPIRY ANALYSIS
# --------------------------------------------
def check_reorder():
    rows = get_inventory()
    if not rows:
        messagebox.showwarning("No Data", "No inventory records found!")
        return

    low_stock = []
    expiring_soon = []
    for name, cat, price, qty, expiry in rows:
        if qty <= 5:  # low stock threshold
            low_stock.append((name, qty))
        if expiry <= 30:  # expiring within 30 days
            expiring_soon.append((name, expiry))

    msg = ""
    if low_stock:
        msg += "⚠️ Low Stock:\n"
        for n, q in low_stock:
            msg += f"  - {n}: {q} left\n"

    if expiring_soon:
        msg += "\n⏳ Expiring Soon:\n"
        for n, e in expiring_soon:
            msg += f"  - {n}: {e} days left\n"

    if not msg:
        msg = "✅ All items are healthy in stock!"

    messagebox.showinfo("Inventory Health", msg)


# --------------------------------------------
# SHOW INVENTORY LIST (AUTO REFRESH)
# --------------------------------------------
def show_inventory():
    win = tk.Toplevel(root)
    win.title("Live Inventory List")

    cols = ["Product", "Category", "Price", "Quantity", "Expiry (days)"]
    tree = ttk.Treeview(win, columns=cols, show="headings")
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(fill="both", expand=True)

    def refresh_inventory():
        for row in tree.get_children():
            tree.delete(row)

        rows = get_inventory()
        for row in rows:
            tree.insert("", "end", values=row)

        win.after(5000, refresh_inventory)  # auto-refresh every 5 seconds

    refresh_inventory()


# --------------------------------------------
# MATPLOTLIB GRAPH VISUALIZATION
# --------------------------------------------
def show_graph():
    rows = get_inventory()
    if not rows:
        messagebox.showwarning("No Data", "No inventory records to plot!")
        return

    products = [r[0] for r in rows]
    quantities = [r[3] for r in rows]
    expiries = [r[4] for r in rows]

    fig, ax1 = plt.subplots()
    ax1.bar(products, quantities, label="Quantity")
    ax1.set_ylabel("Quantity", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")

    ax2 = ax1.twinx()
    ax2.plot(products, expiries, color="red", marker="o", label="Days to Expiry")
    ax2.set_ylabel("Days to Expiry", color="red")
    ax2.tick_params(axis="y", labelcolor="red")

    plt.title("Inventory Health Overview")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


# --------------------------------------------
# GUI SETUP
# --------------------------------------------
root = tk.Tk()
root.title("Inventory Sorting & AI Assistant")
root.geometry("480x550")
root.resizable(False, False)

# ---- Sorting Section ----
frame1 = ttk.LabelFrame(root, text="Sorting Analyzer (DAA)")
frame1.pack(padx=10, pady=10, fill="x")

algo_var = tk.StringVar(value="Quick")
ttk.Label(frame1, text="Sort by Expiry using:").pack(side="left", padx=5)
ttk.OptionMenu(frame1, algo_var, "Quick", "Quick", "Bubble", "Insertion", "Merge").pack(side="left", padx=5)
ttk.Button(frame1, text="Run Sort", command=sort_data).pack(side="left", padx=5)

# ---- AI Reorder Assistant ----
frame2 = ttk.LabelFrame(root, text="Inventory Manager")
frame2.pack(padx=10, pady=10, fill="x")

labels = ["Product", "Category", "Price", "Quantity", "Expiry (days or YYYY-MM-DD)"]
for i, lbl in enumerate(labels):
    ttk.Label(frame2, text=lbl + ":").grid(row=i, column=0, sticky="w", padx=5, pady=3)

# Entry Fields
prod_entry = ttk.Entry(frame2); prod_entry.grid(row=0, column=1)
cat_entry = ttk.Entry(frame2); cat_entry.grid(row=1, column=1)
price_entry = ttk.Entry(frame2); price_entry.grid(row=2, column=1)
qty_entry = ttk.Entry(frame2); qty_entry.grid(row=3, column=1)
expiry_entry = DateEntry(frame2, date_pattern="yyyy-MM-dd"); expiry_entry.grid(row=4, column=1)

# Buttons
ttk.Button(frame2, text="Add Inventory", command=add_inventory).grid(row=5, column=0, pady=10)
ttk.Button(frame2, text="Check Reorder", command=check_reorder).grid(row=5, column=1, pady=10)
ttk.Button(frame2, text="Show Inventory", command=show_inventory).grid(row=6, column=0, columnspan=2, pady=5)
ttk.Button(frame2, text="Show Graph", command=show_graph).grid(row=7, column=0, columnspan=2, pady=5)

root.mainloop()


