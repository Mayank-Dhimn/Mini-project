# src/plotter.py
import matplotlib.pyplot as plt

def show_sort_graph(data):
    algos, times = zip(*data)
    plt.bar(algos, times)
    plt.xlabel("Algorithm")
    plt.ylabel("Time (seconds)")
    plt.title("Sorting Algorithm Performance")
    plt.show()
