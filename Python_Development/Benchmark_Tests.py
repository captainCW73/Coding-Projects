import random
import time
import sys
total_size = 50_000_000
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)
def main():
    print("Generating random integers...")
    data = [random.randint(0, 1000000) for _ in range(total_size)]
    print("Sorting")
    star = time.time()
    sorted_data = quick_sort(data)
    end = time.time()
    print(f"Sorting took {end - star:.2f} seconds.")
if __name__ == "__main__":
    main()