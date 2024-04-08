"""
Через итерируемую последовательность class cyclebf_iter_lst

Через deque(), закольцован - при переполнении первый уходит class cyclebf2
## Класс deque() модуля collections возвращает новый объект deque(),
## инициализированный слева направо данными из итерируемой последовательности iterable.
## .appendleft добавление в начало очереди .append добавление в конец очереди

Через односвязный список class cyclebf_one_lst
## class node содержит значение и указатель следующего
"""

import time
#----------------------------------------------------------------
class cyclebf_iter_lst:
    def __init__(self, siz=4):
        self.readuk = None  # номер ячейки на чтение head
        self.writeuk = 0  # номер ячейки на запись tail
        self._siz = siz
        self.cb = [None for _ in range(self._siz)]

    # присваивание ячейки
    def pull_t(self, value):
        self.cb[self.writeuk] = value
        if self.readuk is None:
            self.readuk = self.writeuk
        elif self.writeuk == self.readuk:
            self.readuk = (self.readuk + 1) % self._siz
        self.writeuk = (self.writeuk + 1) % self._siz

    # чистка ячейки
    def pop_left(self):
        if self.readuk is None:
            return None
        temp = self.cb[self.readuk]
        if not temp is None:
            self.cb[self.readuk] = None
            self.readuk = (self.readuk + 1) % self._siz
        # return tmp

    # Перегрузка для результата
    def __str__(self):
        return '->'.join(f'[{i}]' for i in self.cb)

    # получение элемента буфера по номеру
    def get_from(self, nomer_el):
        try:
            if nomer_el in range(len(self.cb)):
                if self.cb[nomer_el] != None:
                    return self.cb[nomer_el]
        except:
            return False
#----------------------------------------------------------------
import collections
class cyclebf2:
    def __init__(self, siz=5):
        self._siz = siz
        self.cb = collections.deque(self._siz * [None], self._siz)
        self.delPtr = None  # номер del ячейки
        # self.head = 0
        # self.tail = 0

    # присваивание ячейки FI
    def pull_t(self, val):
        self.cb.appendleft(val)

    # действие FO
    def pop_left(self):
        self.delPtr = self.cb.__len__() - 1
        if self.delPtr >= 0:
            temp = self.cb.pop()
        elif self.delPtr < 0:
            temp = None
            self.delPtr = None
            raise Exception("Buffer is empty")
        # return temp,self.delPtr

    # Перегрузка для результата
    def __str__(self):
        return '->'.join(f'[{i}]' for i in self.cb)

    # получение элемента буфера по номеру
    def get_from(self, nomer_el):
        try:
            if nomer_el in range(self.cb.__len__()):
                if self.cb[nomer_el] != None:
                    return self.cb[nomer_el]
        except:
            return False

    def getsize(self):
        return self.cb.__len__()
#----------------------------------------------------------------
class node:
    def __init__(self, value, next_node):
        self.value = value
        self.next_node = next_node

    def getdata(self):
        return self.value

    def getnextnode(self):
        return self.next_node

    def setnextnode(self, node):
        self.next_node = node

class cyclebf_one_lst:
    def __init__(self, siz=4):
        self.head = None
        self.tail = None
        self.size_correct = 0
        self._siz = siz

    def pull_t(self, value):
        if self.size_correct == self._siz:
            self.pop_fi()
        new_node = node(value, self.head)
        if self.head is None:
            self.tail = new_node
            self.head = new_node
        else:
            self.head = new_node

        self.size_correct += 1

    def pop_fi(self):
        prev = None
        curr = self.head
        size_correct = self.size_correct
        while curr:
            if size_correct == 1:
                # изменение указателя следующего
                if prev:
                    prev.setnextnode(curr.next_node)
                else:
                    self.head = curr.next_node
                self.size_correct -= 1
                # return 'razmer - ',self.size_correct
            # if size_correct == 0:
            # print('empty')
            size_correct -= 1
            prev = curr
            curr = curr.next_node
        # return 'empty'

    # получение элемента буфера по номеру
    def get_from(self, nomer_el):
        curr = self.head
        size_correct = self.size_correct
        while curr:
            if size_correct == nomer_el:
                return nomer_el, ' - ', curr.getdata()
            if size_correct == 0:
                print('empty')
            size_correct -= 1
            prev = curr
            curr = curr.getnextnode()
        return False

    # Перегрузка для результата
    def __str__(self):
        result = ''
        node = self.head
        while node:
            result += f'[{node.value}]->'
            node = node.next_node
        return result

    def getsize(self):
        return self.size_correct
#----------------------------------------------------------------


if __name__=='__main__':
    siz = 10000
#-----------------------------------
    buff = cyclebf_iter_lst(siz)

    t0 = time.time()
    for i in range(10000):
        buff.pull_t(i)  # "push" in head
    print('cyclebf_iter_lst_t = ', time.time() - t0)  # t_empty = 0.011

    t0 = time.time()
    for i in range(10000):
        buff.pop_left()  # "pop" from head
    print('cyclebf_iter_lst-p_t = ', time.time() - t0)  # t = 0.08
#-----------------------------------
    buff = cyclebf2(siz)

    t0 = time.time()
    for i in range(10000):
        buff.pull_t(i)  # "push" in head
    print('cyclebf2_t = ', time.time() - t0)  # t = 0.009

    t0 = time.time()
    for i in range(10000):
        buff.pop_left()  # "pop" from head
    print('cyclebf2_p_t = ', time.time() - t0)  # t = 0.007
#-----------------------------------
    buff = cyclebf_one_lst(siz)

    t0 = time.time()
    for i in range(10000):
        buff.pull_t(i)  # "push" in head
    print('cyclebf_one_lst_t = ', time.time() - t0)  # t = 0.011 при заполнении и 9.33 при переполнении

    t0 = time.time()
    for i in range(100000):
        buff.pop_fi()  # "pop" from head
    print('cyclebf_one_lst_p_t = ', time.time() - t0)  # t = 4.57