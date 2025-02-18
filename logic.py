import time

def match(a, b, s1, s2):
    if s1 < s2:
        for c in a[0] + a[1]:
            if not (c in b[0] or c in b[1]):
                return False
    else:
        for c in b[0] + b[1]:
            if not (c in a[0] or c in a[1]):
                return False
    return True


def diff_1(a, b, s1, s2):
    val = -1
    if s1 < s2:
        for c in a[0]:
            if c in b[1]:
                if val == -1:
                    val = c
                else:
                    return -1
        for c in a[1]:
            if c in b[0]:
                if val == -1:
                    val = c
                else:
                    return -1
    else:
        for c in b[0]:
            if c in a[1]:
                if val == -1:
                    val = c
                else:
                    return -1
        for c in b[1]:
            if c in a[0]:
                if val == -1:
                    val = c
                else:
                    return -1

    if val == -1:
        return -2
    return val
        

# valid = ["0001", "0010", "0011", "0101", "0111", "1011", "1101"]
valid = ["0000", "0011", "1000", "1111"]
def convert(vals):
    n = len(vals[0])
    ret = []
    for x in vals:
        ones = []
        zeros = []
        for i in range(n-1, -1, -1):
            if x[i] == '0':
                zeros.append(n-i-1)
            else:
                ones.append(n-i-1)
        
        ret.append([zeros, ones])

    return n, ret

# values[i] = [[zero pos], [one pos]]
# n = 4
# values = [[[1,2,3], [0]], 
#           [[0,2,3], [1]], 
#           [[2,3], [0,1]],
#           [[1,3], [0,2]],
#           [[3], [0,1,2]],
#           [[2], [0,1,3]],
#           [[1], [0,2,3]]
# ]

n, values = convert(valid)
# print(n)
# print(values)

start = time.time()

def find_circuit(n, values):
    found = True

    while (found):
        found = False
        n = len(values)
        
        for i in range(n):
            for j in range(i+1, n):
                if j >= len(values):
                    break
                    
                v1, v2 = values[i], values[j]

                s1 = len(v1[0]) + len(v1[1])
                s2 = len(v2[0]) + len(v2[1])

                if not match(v1, v2, s1, s2):
                    continue
                
                diff = diff_1(v1, v2, s1, s2)
                if diff == -1:
                    continue
                if diff == -2:
                    del values[j]
                    continue

                # print(values[i])
                # print(values[j])
                # print("---")
                
                found = True

                if diff in v1[0]:
                    if s1 >= s2:
                        del values[i][0][v1[0].index(diff)]
                    if s2 >= s1:
                        del values[j][1][v2[1].index(diff)]
                else:
                    if s1 >= s2:
                        del values[i][1][v1[1].index(diff)]
                    if s2 >= s1:
                        del values[j][0][v2[0].index(diff)]
                
                # print(values[i])
                if s1 == s2:
                    del values[j]
                # else:
                #     print(values[j])
                # print()

        n = len(values)
        for i in range(n - 1, -1, -1):
            if values.index(values[i]) != i:
                del values[i]


    # can delete extraneous terms be generating all possibilities and getting counts

    return values

# print(find_circuit(n, values))
# print(time.time() - start)