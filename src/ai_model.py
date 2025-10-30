# src/ai_model.py
import numpy as np
from sklearn.linear_model import LogisticRegression

# Small training dataset
X = np.array([
    [5, 10, 4],   # low stock, near expiry, high sales -> reorder
    [50, 100, 2], # high stock -> no reorder
    [8, 7, 5],
    [30, 60, 3],
    [10, 15, 4],
    [25, 200, 1]
])
y = np.array([1, 0, 1, 0, 1, 0])  # 1 = reorder, 0 = ok

model = LogisticRegression()
model.fit(X, y)

def predict_reorder(quantity, expiry_days, avg_sales):
    pred = model.predict([[quantity, expiry_days, avg_sales]])[0]
    prob = model.predict_proba([[quantity, expiry_days, avg_sales]])[0][1]
    return bool(pred), round(prob, 2)
