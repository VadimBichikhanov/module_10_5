import time
import os
import mmap
import asyncio
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool

def read_info_mmap(name, block_size=1024*1024):  # block_size = 1 MB
    all_data = []
    with open(name, 'r+b') as file:
        mmapped_file = mmap.mmap(file.fileno(), 0)
        while True:
            block = mmapped_file.read(block_size)
            if not block:
                break
            all_data.append(block.decode('utf-8'))
        mmapped_file.close()

async def read_info_async(name, block_size=1024*1024):  # block_size = 1 MB
    all_data = []
    with open(name, 'r+b') as file:
        mmapped_file = mmap.mmap(file.fileno(), 0)
        while True:
            block = mmapped_file.read(block_size)
            if not block:
                break
            all_data.append(block.decode('utf-8'))
        mmapped_file.close()

def process_file_sync(filename):
    read_info_mmap(filename)

async def process_file_async(filename):
    await read_info_async(filename)

async def process_with_asyncio(filenames):
    tasks = [process_file_async(filename) for filename in filenames]
    await asyncio.gather(*tasks)

def process_with_threads(filenames, num_threads):
    with ThreadPool(processes=num_threads) as pool:
        pool.map(process_file_sync, filenames)

def process_file_with_threads(filename_and_threads):
    filename, num_threads = filename_and_threads
    process_with_threads([filename], num_threads)

if __name__ == '__main__':
    base_dir = '/home/v/Документы/module_10_5'
    filenames = [os.path.join(base_dir, f'file {number}.txt') for number in range(1, 5)]

    # Линейный вызов
    start_time = time.perf_counter()
    for filename in filenames:
        process_file_sync(filename)
    linear_time = time.perf_counter() - start_time
    print(f"{linear_time:.6f} (линейный)")

    # Асинхронный вызов с asyncio
    start_time = time.perf_counter()
    asyncio.run(process_with_asyncio(filenames))
    asyncio_time = time.perf_counter() - start_time
    print(f"{asyncio_time:.6f} (асинхронный с asyncio)")

    # Многопоточный вызов с указанием количества потоков
    num_threads = 9  # Укажите нужное количество потоков
    start_time = time.perf_counter()
    process_with_threads(filenames, num_threads)
    multithread_time = time.perf_counter() - start_time
    print(f"{multithread_time:.6f} (многопоточный с {num_threads} потоками)")

    # Многопроцессный вызов с указанием количества процессов
    num_processes = 4  # Укажите нужное количество процессов
    start_time = time.perf_counter()
    with Pool(processes=num_processes) as pool:
        pool.map(process_file_with_threads, [(f, num_threads) for f in filenames])
    multiprocess_time = time.perf_counter() - start_time
    print(f"{multiprocess_time:.6f} (многопроцессный с {num_processes} процессами и {num_threads} потоками в каждом)")