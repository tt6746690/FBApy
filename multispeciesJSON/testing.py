list1 = [1, '2', 3]
list2 = ['2', '3', 2, 3, 8]
f = set(list1)
p = f.intersection(list2)

hi = list(set(list1) & set(list2))
print(hi)
print(list(p))
if 1 is list:
    print('yes')