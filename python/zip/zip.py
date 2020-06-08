obj1 = ["abc", "xyz"]

obj2 = [1, 2]

obj3 = dict(zip(obj1, obj2))

print(obj3)

obj4 = {"jkl": 3}
obj5 = {**obj3, **obj4}

print(obj5)