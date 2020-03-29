from functools import lru_cache


@lru_cache()  # caching helps improve performance
def some_func():
    print(True)


