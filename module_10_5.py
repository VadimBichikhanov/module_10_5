import time
from multiprocessing import Pool
import os

def read_info(name):
    all_data = []
    with open(name, 'r') as file:
        while True:
            line = file.readline()
            if not line:
                break
            all_data.append(line)

if __name__ == '__main__':
    base_dir = '/home/v/Документы/module_10_5'
    filenames = [os.path.join(base_dir, f'file {number}.txt') for number in range(1, 5)]

    # Линейный вызов
    start_time = time.time()
    for filename in filenames:
        read_info(filename)
    linear_time = time.time() - start_time
    print(f"{linear_time:.6f} (линейный)")

    # Многопроцессный вызов
    start_time = time.time()
    with Pool() as pool:
        pool.map(read_info, filenames)
    multiprocess_time = time.time() - start_time
    print(f"{multiprocess_time:.6f} (многопроцессный)")