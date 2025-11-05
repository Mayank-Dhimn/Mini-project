import pandas as pd
import random

categories = ['Electronics', 'Groceries', 'Clothing', 'Stationery', 'Cosmetics', 'Toys', 'Medicines']
products = [
    'Laptop', 'Phone', 'Headphones', 'Charger', 'Keyboard', 'Mouse', 'Milk', 'Bread', 'Sugar', 'Rice',
    'Shirt', 'Pants', 'Notebook', 'Pen', 'Lipstick', 'Perfume', 'Action Figure', 'Puzzle', 'Syrup', 'Tablet'
]

data = []
for i in range(1, 201):  # 100 fake rows
    product = random.choice(products)
    category = random.choice(categories)
    price = round(random.uniform(50, 5000), 2)
    quantity = random.randint(1, 100)
    expiry_days = random.randint(10, 1000)
    data.append([i, product, category, price, quantity, expiry_days])

df = pd.DataFrame(data, columns=['id', 'product_name', 'category', 'price', 'quantity', 'expiry_days'])
df.to_csv("fake_inventory_data.csv", index=False)

print("✅ Fake data generated and saved as fake_inventory_data.csv")
