# sets are touted to be faster to operate over than lists/dicts

set_a = {1, 2, 3, 4, 5, 6}

set_b = {4, 5, 6}

print(set_a.difference(set_b))

print(set_a.issubset(set_b))

print(set_a.issuperset(set_b))