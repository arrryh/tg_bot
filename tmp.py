a = [1, 2, 3, 4, 5, 6]

def find_indx_by_id(pk, items: list):
    i = 0

    for v in items:
        if id(v) == pk:
            return i
        i += 1

pk = id(a[2])
indx = find_indx_by_id(pk, a)

indx = 5

next_indx = indx + 1 if len(a) < indx + 1 else indx
prev_indx = indx - 1


print(
    'next_indx', next_indx,
    a[next_indx],
    indx,
)