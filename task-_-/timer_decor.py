# декоратор для таймера
from time import process_time,perf_counter_ns
def time_of_func(func):
    def wrapped(*args):
        # возвращает значение часов с наибольшим доступным разрешением ns
        start_time = perf_counter_ns()
        res = func(*args)
        print(func.__name__,perf_counter_ns() - start_time)
        return func.__name__, res,perf_counter_ns() - start_time
    return wrapped

# декоратор времени
def time_of_func_prt(func):
    def wrapped(lst):
        t0 = process_time()
        res = func(lst)
        return process_time() - t0, func.__name__, res

    return wrapped