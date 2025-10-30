# src/sorts.py
import time

def time_it(func):
    def wrapper(arr):
        start = time.time()
        res = func(arr.copy())
        elapsed = time.time() - start
        return res, elapsed
    return wrapper

@time_it
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

@time_it
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]
    left = [x for x in arr if x < pivot]
    mid = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left)[0] + mid + quick_sort(right)[0]
