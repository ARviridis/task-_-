"""
time_of_func декоратор для таймера
# isEven - приведенный пример:
# + Краткая и простая реализация.
# - Может вызвать переполнение для очень больших чисел.
# - операция деления
------------
# isEven1 - через итерируемую последовательность
# + применим и в других системах исчисления с четным основанием если указывать шаг
# - проходится по всем четным числам от 0 до указанного
------------
# isEven2 - через Побитовое логическое «И»
# при &2 ноль - отличное число;при отрицании, как и должно, считается отрицание
#
# + оперерирует только с нулевым битом исходного числа value в двоичной системе
# из-за чего скорость выполнения возрастает
# Число нечетное, когда его младший бит равен 1. Побитовым "И" искомого числа и единицы - получаем последний бит.
# Оператор not преобразует 1 в False (число нечетное), 0 соответственно в True.

# isEven3 ручной вариант - эквивалент sEven2
------------
# isEven4 - ручной вариант, через вычитание, рекурсия
# - время работы алгоритма больше из-за рекурсии
# - работает медленнее, так как большее колличество повторных шагов
# - выше потребление памяти, проигрывает по колличеству объектов, без gc
------------
# isEven5 через проверку
# проверяет, что число n оканчивается на 0 2 4 6 8
# + не проводит вычисления
# + вариант для комплексного числа, работает через строку
------------
"""

from timer_decor import time_of_func

@time_of_func
def isEven1(value):
    return value in range(0,value+1,2)

@time_of_func
def isEven2(value):
    return not bool(value & 1)

import operator
@time_of_func
def isEven3(value):
    return not operator.truth(value&1)

@time_of_func
def isEven4(value):
    while abs(value) > 0:
        value = abs(value) - 2
        if value < 0:
            break
    return value == 0

from typing import Union
@time_of_func
def isEven5(n: Union[int, float, str]) -> bool:
    if n != 0:
        prepare = str(n)
        if prepare.__contains__('.'):
            return prepare.split('.')[1] == '0' and prepare.split('.')[0][-1] in '02468'
        return prepare[-1] in '02468'
    return False

@time_of_func
def isEven(value):
    return value % 2 == 0


if __name__=='__main__':
    # вызовы
    isEven(100000) # t - 800
    isEven(999999) # t - 1100
    isEven1(100000) # t - 3400
    isEven1(999999) # t - 2600
    isEven2(100000) # t - 1200
    isEven2(999999) # t - 1400
    isEven3(100000) # t - 2500
    isEven3(999999) # t - 2500
    isEven4(100000) # t - 7889600
    isEven4(999999) # t - 76458000
    isEven5(100000) # t - 3600
    isEven5(999999) # t - 3100

    # disasm для сравнения по байт коду
    import dis
    print('isEven - ⇓')
    dis.dis(isEven.__closure__[0].cell_contents)
    print('isEven1 - ⇓')
    dis.dis(isEven1.__closure__[0].cell_contents)
    print('isEven2 - ⇓')
    dis.dis(isEven2.__closure__[0].cell_contents)
    print('isEven3 - ⇓')
    dis.dis(isEven3.__closure__[0].cell_contents)
    print('isEven4 - ⇓')
    dis.dis(isEven4.__closure__[0].cell_contents)
    print('isEven5 - ⇓')
    dis.dis(isEven5.__closure__[0].cell_contents)
"""
результаты без декоратора
isEven
 69           0 LOAD_FAST                0 (value)
              2 LOAD_CONST               1 (2)
              4 BINARY_MODULO
              6 LOAD_CONST               2 (0)
              8 COMPARE_OP               2 (==)
             10 RETURN_VALUE

isEven1
 38           0 LOAD_FAST                0 (value)
              2 LOAD_GLOBAL              0 (range)
              4 LOAD_CONST               1 (0)
              6 LOAD_FAST                0 (value)
              8 LOAD_CONST               2 (1)
             10 BINARY_ADD
             12 LOAD_CONST               3 (2)
             14 CALL_FUNCTION            3
             16 COMPARE_OP               6 (in)
             18 RETURN_VALUE

isEven2
 42           0 LOAD_GLOBAL              0 (bool)
              2 LOAD_FAST                0 (value)
              4 LOAD_CONST               1 (1)
              6 BINARY_AND
              8 CALL_FUNCTION            1
             10 UNARY_NOT
             12 RETURN_VALUE

isEven3
 47           0 LOAD_GLOBAL              0 (operator)
              2 LOAD_METHOD              1 (truth)
              4 LOAD_FAST                0 (value)
              6 LOAD_CONST               1 (1)
              8 BINARY_AND
             10 CALL_METHOD              1
             12 UNARY_NOT
             14 RETURN_VALUE

isEven4
 51     >>    0 LOAD_GLOBAL              0 (abs)
              2 LOAD_FAST                0 (value)
              4 CALL_FUNCTION            1
              6 LOAD_CONST               1 (0)
              8 COMPARE_OP               4 (>)
             10 POP_JUMP_IF_FALSE       36
 52          12 LOAD_GLOBAL              0 (abs)
             14 LOAD_FAST                0 (value)
             16 CALL_FUNCTION            1
             18 LOAD_CONST               2 (2)
             20 BINARY_SUBTRACT
             22 STORE_FAST               0 (value)
 53          24 LOAD_FAST                0 (value)
             26 LOAD_CONST               1 (0)
             28 COMPARE_OP               0 (<)
             30 POP_JUMP_IF_FALSE        0
 54          32 JUMP_ABSOLUTE           36
             34 JUMP_ABSOLUTE            0
 55     >>   36 LOAD_FAST                0 (value)
             38 LOAD_CONST               1 (0)
             40 COMPARE_OP               2 (==)
             42 RETURN_VALUE

isEven5
 60           0 LOAD_FAST                0 (n)
              2 LOAD_CONST               1 (0)
              4 COMPARE_OP               3 (!=)
              6 POP_JUMP_IF_FALSE       78
 61           8 LOAD_GLOBAL              0 (str)
             10 LOAD_FAST                0 (n)
             12 CALL_FUNCTION            1
             14 STORE_FAST               1 (prepare)
 62          16 LOAD_FAST                1 (prepare)
             18 LOAD_METHOD              1 (__contains__)
             20 LOAD_CONST               2 ('.')
             22 CALL_METHOD              1
             24 POP_JUMP_IF_FALSE       66
 63          26 LOAD_FAST                1 (prepare)
             28 LOAD_METHOD              2 (split)
             30 LOAD_CONST               2 ('.')
             32 CALL_METHOD              1
             34 LOAD_CONST               3 (1)
             36 BINARY_SUBSCR
             38 LOAD_CONST               4 ('0')
             40 COMPARE_OP               2 (==)
             42 JUMP_IF_FALSE_OR_POP    64
             44 LOAD_FAST                1 (prepare)
             46 LOAD_METHOD              2 (split)
             48 LOAD_CONST               2 ('.')
             50 CALL_METHOD              1
             52 LOAD_CONST               1 (0)
             54 BINARY_SUBSCR
             56 LOAD_CONST               5 (-1)
             58 BINARY_SUBSCR
             60 LOAD_CONST               6 ('02468')
             62 COMPARE_OP               6 (in)
        >>   64 RETURN_VALUE
 64     >>   66 LOAD_FAST                1 (prepare)
             68 LOAD_CONST               5 (-1)
             70 BINARY_SUBSCR
             72 LOAD_CONST               6 ('02468')
             74 COMPARE_OP               6 (in)
             76 RETURN_VALUE
 65     >>   78 LOAD_CONST               7 (False)
             80 RETURN_VALUE
"""