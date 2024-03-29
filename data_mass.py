data_mas = [
    [1, 2, 2, 2, 2, 2, 2, 3],
    [2, 2, 2, 2, 2, 2, 2, 3],
    [3, 2, 2, 2, 2, 2, 2, 3],
    [4, 2, 2, 2, 2, 2, 2, 3],
    [11, 2, 2, 2, 2, 2, 2, 3],
    [12, 2, 2, 2, 2, 2, 2, 3],
    [13, 2, 2, 4, 2, 4, 2, 5],
    [14, 2, 2, 4, 2, 4, 2, 5],
    [21, 4, 2, 2, 2, 2, 2, 3],
    [22, 8, 2, 4, 2, 4, 2, 5],
    [23, 12, 3, 4, 3, 5, 3, 5],
    [24, 12, 3, 4, 3, 5, 3, 5],
    [31, 8, 2, 4, 2, 4, 2, 5],
    [32, 12, 3, 4, 3, 5, 3, 5],
    [33, 16, 4, 4, 3, 6, 3, 6],
    [34, 20, 4, 6, 3, 8, 3, 8],
    [41, 12, 3, 4, 3, 5, 3, 5],
    [42, 16, 4, 4, 3, 6, 3, 6],
    [43, 20, 4, 5, 4, 5, 3, 7],
    [44, 24, 4, 7, 4, 7, 3, 10],
    [51, 16, 4, 4, 3, 6, 3, 6],
    [52, 20, 4, 5, 4, 5, 3, 7],
    [53, 24, 4, 6, 4, 6, 3, 8],
    [54, 28, 4, 8, 4, 8, 4, 11],
    [61, 20, 4, 5, 4, 5, 3, 7],
    [62, 24, 4, 6, 4, 6, 3, 8],
    [63, 28, 4, 7, 4, 7, 4, 7],
    [64, 32, 4, 10, 4, 10, 4, 10],
    [71, 24, 4, 6, 4, 6, 3, 8],
    [72, 28, 4, 7, 4, 7, 4, 7],
    [73, 32, 4, 8, 4, 8, 4, 8],
    [74, 36, 4, 11, 4, 11, 4, 11],
]

def point_quantity_circle(diameter, L):
    num_str = 0
    lenght = 0.2
    step = 0.3

    while diameter > lenght:
        num_str = num_str + 10
        lenght = lenght + step
        step = step + 0.1
        #print(num_str, lenght, step)
        if lenght > 3.5:
            break
    koef = L / diameter 
    if koef > 5.5:
        num_str = num_str + 1
    elif koef > 4:
        num_str = num_str + 2
    elif koef > 2.5:
        num_str = num_str + 3
    else:
        num_str = num_str + 4

    #num_str = int(num_str)
    for el in data_mas:
        if el[0] == num_str:
            print(num_str, el)
            return el[1]
    return 0


def point_quantity_rectangle(diameter, L, min_side, max_side):
    num_str = 0
    lenght = 0.2
    step = 0.3
    nA = 0
    nB = 0

    while diameter > lenght:
        num_str = num_str + 10
        lenght = lenght + step
        step = step + 0.1
        #print(num_str, lenght, step)
        if lenght > 3.5:
            break
    koef = L / diameter 
    if koef > 5.5:
        num_str = num_str + 1
    elif koef > 4:
        num_str = num_str + 2
    elif koef > 2.5:
        num_str = num_str + 3
    else:
        num_str = num_str + 4

    # num_str = int(num_str)
    koef = max_side / min_side
    for el in data_mas:
        if el[0] == num_str:
            # print(num_str, el)
            if koef > 2.5:
                nA = el[6]
                nB = el[7]
            elif koef > 1.6:
                nA = el[4]
                nB = el[5] 
            else:
                nA = el[2]
                nB = el[3] 
            print("point_quantity_rectangle ", nA, nB)
            return (nA, nB)
    return 0
