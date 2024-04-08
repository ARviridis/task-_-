"""
quick_sort
## Взят средний элемент как опорный для случая обработки отсортированного списка,
## чтобы время выполнения было О(n log n), а не O(n**2)
## его скорости значительно быстрее, чем пузырьковая сортировка, сортировка слиянием, вставками и выбором и
## как следствие является самым стабильным из них,   с частично отсортированными массивами справляется еще лучше.

counting Sort
## сортировка подсчета, имеет сложность О(n+k) где n это количество элементов,k - разрядность.
## главным условием высокой скорости работы будет разрядность чисел не выше 10**7

bubble_sort
## последовательноое сравнения соседних элементов и их обмен

merge_sort
##Объединяет два массива (а именно, две части одного массива) в один в отсортированном порядке.
##Разбивает массив на две половины и сортирует их по-отдельности рекурсивно.
##Сортировка частей массива происходит их объединением уже в отсортированном виде.

heap_sort
## Пирамидальная имеет сложность O(n log n), то есть время выполнения растёт логарифмически
## пропорционально количеству элементов
## Алгоритм не меняет порядок равных элементов, то есть он устойчив, будет более стабильной и
## хорошо справляться в случае наличия одинаковых ключей

q_a_h_sort
## Комбинирование quick sort и heap sort
## Изначальная быстрая переключается на пирамидальную с, когда глубина рекурсии
## превысит заранее установленный уровень (логарифма от числа сортируемых элементов).
## Подход сочетает в себе достоинства методов с худшим случаем O(n log n) и быстродействием,
## сравнимым с быстрой сортировкой

# стандартная sort()
## list.sort() пользуются timsort в python, является гибридом, имеющим внутри  вставки и
## слияния, а также  ряд дополнительных условий для оптимизации
"""

from random import randint
from timer_decor import time_of_func_prt


#----------------------------------------------------------------
# counting Sort
@time_of_func_prt
def count_sort(lst):
    mine = min(lst)
    maxe = max(lst)
    # list с нулями + 1
    lst_0_1 = [0 for _ in range(maxe - mine + 1)]
    # list с нулями
    lst_0 = [0 for _ in range(len(lst))]
    # увеличиваем значение на входном
    for _ in range(0, len(lst)):
        lst_0_1[lst[_] - mine] += 1
    # Каждому элементу от 1 до length(c) -1 добавляем к значению текущего элемента значение
    for _ in range(1, len(lst_0_1)):
        lst_0_1[_] += lst_0_1[_ - 1]
    # цикл, который итерируется по списку в обратном порядке
    # создавая вывод уменьшая его на 1
    for _ in range(len(lst) - 1, -1, -1):
        lst_0[lst_0_1[lst[_] - mine] - 1] = lst[_]
        lst_0_1[lst[_] - mine] -= 1
    # переопределение
    for i in range(0, len(lst)):
        lst[i] = lst_0[i]

    return lst

#----------------------------------------------------------------
# quick_sort
@time_of_func_prt
def quick_sort(lst):
    if lst.__len__() >= 1:
        ser = lst[lst.__len__() // 2]
        return quick_sort.__closure__[0].cell_contents(list(filter(lambda k: k < ser, lst))) + \
            list(filter(lambda k: k == ser, lst)) + \
            quick_sort.__closure__[0].cell_contents(list(filter(lambda k: k > ser, lst)))
    else:
        return lst
#----------------------------------------------------------------
# bubble_sort
@time_of_func_prt
def bubble_sort(lst):
    for i in range(len(lst) - 1, 0, -1):
        flag = True
        for k in range(0, i):
            if lst[k] > lst[k + 1]:
                lst[k], lst[k + 1] = lst[k + 1], lst[k]
                flag = False
        if flag:
            return lst
#----------------------------------------------------------------
# merge_sort
def merge(lst, start, mid, end):
    left = []
    right = []
    nleft = mid - start + 1
    nright = end - mid

    for i in range(nleft):
        left.append(lst[start + i])
    for j in range(nright):
        right.append(lst[mid + j + 1])
    # +1 (the most huge)
    left += ([float('inf')])
    right += ([float('inf')])

    i_left = i_right = 0

    for i in range(start, end + 1):
        leftkey = left[i_left]
        rightkey = right[i_right]

        if leftkey <= rightkey:
            lst[i] = left[i_left]
            i_left += 1
        else:
            lst[i] = right[i_right]
            i_right += 1

@time_of_func_prt
def merge_sort(lst, start=0, end = None):
    if end == None:
        end = len(lst) - 1

    if start < end:
        mid = (start + end) // 2
        merge_sort.__closure__[0].cell_contents(lst, start, mid)
        merge_sort.__closure__[0].cell_contents(lst, mid + 1, end)
        merge(lst, start, mid, end)
    return lst
#----------------------------------------------------------------
# heap_sort
def heapify_max_sort(lst, n, i):
    dlina = i
    l = 2 * i + 1
    r = 2 * i + 2
    if l < n and lst[i] < lst[l]:
        dlina = l
    if r < n and lst[dlina] < lst[r]:
        dlina = r
    if dlina != i:
        (lst[i], lst[dlina]) = (lst[dlina], lst[i])
        heapify_max_sort(lst, n, dlina)

@time_of_func_prt
def heap_sort(lst):
    n = len(lst)
    for i in range(n // 2, -1, -1):
        heapify_max_sort(lst, n, i)
    for i in range(n - 1, 0, -1):
        (lst[i], lst[0]) = (lst[0], lst[i])
        heapify_max_sort(lst, i, 0)
    return lst
#----------------------------------------------------------------
# Комбинирование quick sort и heap sort
from math import log2

def quick_sort_2(lst_2, start, end):
    lst = lst_2[start:end]
    if lst.__len__() >= 1:
        ser = lst[lst.__len__() // 2]
        return \
                (list(filter(lambda k: k < ser, lst))) + \
                list(filter(lambda k: k == ser, lst)) + \
                (list(filter(lambda k: k > ser, lst)))
    else:
        return lst

@time_of_func_prt
def q_a_h_sort(lst, start=0, end=None, zero=0):
    if end is None:
        end = len(lst)

    if zero < log2(len(lst)):
        if start < end:
            mid = quick_sort_2(lst, start, end)
            lst[start:end] = mid = q_a_h_sort.__closure__[0].cell_contents(mid, start, (len(mid) // 2), zero + 1)
            lst[start:end] = q_a_h_sort.__closure__[0].cell_contents(mid, (len(mid) // 2) + 1, len(mid) + 1, zero + 1)
    else:
        lst[start:end + 1] = heap_sort.__closure__[0].cell_contents(lst[start:end + 1])
    return lst
#----------------------------------------------------------------
# стандартная sort()
@time_of_func_prt
def sortst(lst):
    lst.sort()
    return lst
#----------------------------------------------------------------


if __name__ == '__main__':
    lst = [randint(0, 100) for _ in range(999999)]

    lst = count_sort(lst)   #0.484375
    print(lst[0:2])
    print(count_sort(lst[2])[0:2]) #0.4375

    lst = [randint(0, 100) for _ in range(999999)]
    lst = quick_sort(lst)   #2.04
    print(lst[0:2])
    print(quick_sort(lst[2])[0:2])    #1.42

    lst = [randint(0, 100) for _ in range(999999)]
    lst = merge_sort(lst)   #7.29
    print(lst[0:2])
    print(merge_sort(lst[2])[0:2])    #7.02

    lst = [randint(0, 100) for _ in range(999999)]
    lst = heap_sort(lst)    #8.75
    print(lst[0:2])
    print(heap_sort(lst[2])[0:2]) #8.04

    lst = [randint(0, 100) for _ in range(999999)]
    lst = q_a_h_sort(lst)   #1.06
    print(lst[0:2])
    print(q_a_h_sort(lst[2])[0:2])    #1.03

    lst = [randint(0, 100) for _ in range(999999)]
    lst = sortst(lst)       #0.078125
    print(lst[0:2])
    print(sortst(lst[2])[0:2])        #0.015625

    #lst = [randint(0, 100) for _ in range(999999)]
    #lst = bubble_sort(lst) #0.015625 over
    #print(lst[0:2])
    print(bubble_sort(lst[2])[0:2])