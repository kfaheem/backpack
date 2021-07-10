import threading


tmp_lst = [1, 2, 3]


def some_func(arg1, arg2):
    pass


threads = [threading.Thread(target=some_func, args=[arg1, "arg2"]) for arg1 in tmp_lst]

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
