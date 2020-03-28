from itertools import compress, accumulate
from more_itertools import partition, divide, collapse
import os


def itertools_compress():

    obj1 = [1, 2, 3, 4, 5, 10, 8]
    obj2 = [True, True, False, True, False, False, True]

    print(list(compress(obj1, obj2)))  # returns elements in obj1 corresponding to True elements in obj2


def itertools_accumulate():

    obj1 = [1, 2, 3, 4, 5, 10, 8]
    print(list(accumulate(obj1, max)))  # [1, 2, 3, 4, 5, 10, 10]


def more_itertools_partition():

    obj1 = [1, 2, 3, 4, 5, 10, 8]

    lst_a, lst_b = partition(lambda x: x % 2 == 0, obj1)
    print(list(lst_a))
    print(list(lst_b))


def more_itertools_divide():

    obj1 = [1, 2, 3, 4, 5, 10, 8]

    result = divide(3, obj1)

    for item in list(result):
        print(list(item))


def more_itertools_collapse():

    obj = [1, [2, 3, 4], [9, [6, 7], 10]]

    print(list(collapse(obj)))  # [1, 2, 3, 4, 9, 6, 7, 10]

    # to collapse a directory

    print(list(collapse(os.walk("Directory path"))))




