# 🧠 Inventory Sorting & AI Assistant

A simple Python-based desktop app for managing and analyzing inventory using:
- **Tkinter** → GUI  
- **SQLite** → database  
- **NumPy & scikit-learn** → AI for reorder prediction  
- **Matplotlib** → visualization  
- **Custom DAA sorting algorithms** → Bubble Sort & Quick Sort

---

## ⚙️ Features

- Add, view, and update inventory items  
- Predict low-stock or soon-to-expire items using AI  
- Analyze sorting algorithms (Bubble vs Quick Sort)  
- Visualize inventory data using graphs  
- All data stored locally in SQLite (`inventory.db`)

---

## 🧩 Prerequisites

- **Python 3.10+** installed and on PATH (check with `python --version`)  
- Git (optional, if cloning from GitHub)  
- Internet connection to download Python packages

---

## 🪜 Complete Windows setup & run (copy & paste these commands)

---

## Create a virtual environment 

- python -m venv venv
 
## Activate the virtual environment

 - Source venv/Source/activate

---

## Upgrade pip (recommended)

- python -m pip install --upgrade pip


---

## Install dependencies from requirements.txt

- pip install -r requirements.txt

---

## Initialize the SQLite database

- python -c 'from src.db import setup_database; setup_database(); print("Database ready!")'

## Run the GUI application 

- python src/main.py