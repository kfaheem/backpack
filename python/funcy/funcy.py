from funcy import lflatten
from funcy import merge_with, lcat
from funcy import lchunks


def create_chunks():

    some_list = [1, 2, 3, 4, 5]

    print(lchunks(3, some_list))


def merge_dicts():

    dict_a = {"abc": [1, 2, 3], "xyz": [4, 5]}
    dict_b = {"abc": [4, 5], "xyz": [1, 2, 3]}

    print(merge_with(lcat, dict_a, dict_b))


def flatten_list():

    some_list = [1, [2, [3, 4], 5], 8, 9]

    print(lflatten(some_list))

