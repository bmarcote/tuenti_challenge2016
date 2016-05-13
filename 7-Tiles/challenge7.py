import sys
import numpy as np

lines = open(sys.argv[1], 'r').readlines()
output = open(sys.argv[2], 'w')

alphabet = '.abcdefghijklmnopqrstuvwxyz'

def row2values(row):
    row = list(row)
    for i,char in enumerate(row):
        row[i] = alphabet.index(char.lower())
        if char.islower():
            row[i] *= -1
    return row

def get_max1d(row, limits, case=0):
    max_sum1d = 0
    # alert = False
    for i1 in range(limits[0], limits[1]+1):
        for i2 in range(i1, max(limits[1]+1, limits[1]+1+i1-2)):
            # if not (i1==limits[0] and i2==limits[1]):
            res = row[i2]-row[i1-1]
            if res >= max_sum1d:
                # if case == 12:
                #     print('Inside: ', res, i1, i2)
                # if (i1 == limits[0] and i2 == limits[1]) or res==max_sum1d:
                #     alert = True
                # else:
                #     alert = False
                max_sum1d = res
    return max_sum1d

def get_max_sum(matrix, ncase=0):
    # We extend the matrix to accomodate the boundary conditions
    # pdb.set_trace()
    n,m = matrix.shape
    if n==1 and m==1:
        if matrix[0,0] > 0:
            return 'INFINITY'
        else:
            return 0
    work_matrix = np.zeros((n+1+max(0,n-2), m+1+max(0,m-2)))
    work_matrix[1:n+1,1:m+1] = matrix
    # repeating the matrix
    work_matrix[n+1:,1:m+1] = work_matrix[1:n+1-2,1:m+1]+work_matrix[n,1:m+1]
    for i in range(m+1, m+1+max(0,m-2)):
        work_matrix[:,i] = work_matrix[:,i-m]+work_matrix[:,m]
    # Now let's find the max submatrix!!!
    max_sum = 0 # empty matrix
    # submatrix_is_fullmatrix = False
    # Check an easy case: if the limits are positive => you can increment
    # infinitely the sum.
    for i in range(1, n+1):
        for i2 in range(1, i):
            if work_matrix[i,m]-work_matrix[i-i2,m] > 0:
                return 'INFINITY'
    for j in range(1, m+1):
        for j2 in range(1, j):
            if work_matrix[n,j]-work_matrix[n,j-j2] > 0:
                return 'INFINITY'
    # Then we need to check everything
    for j1 in range(1, m+1):
        for j2 in range(j1, max(m+1, m+1+j1-2)):
            slide = work_matrix[:,j2]-work_matrix[:,j1-1]
            result = get_max1d(slide, limits=(1,n), case=ncase)
            if result >= max_sum:
                # if ncase == 12:
                #     print(max_sum, j1,j2)
                # if alert or (j1==1 and j2==m+1) or result == max_sum:
                #     submatrix_is_fullmatrix = True
                # else:
                #     submatrix_is_fullmatrix = False
                max_sum = result
    # if ncase == 6:
    #     print(work_matrix)
    # if submatrix_is_fullmatrix:
    #     return 'INFINITY'
    # else:
    return int(max_sum)

def do_case(index, n_case=0):
    # get N,M values
    n, m = [int(i) for i in lines[index].replace('\n', '').split(' ')]
    matrix = np.empty((n, m))
    # Convert the characters to numbers (using cumulative values)
    for i in range(index+1, index+n+1):
        matrix[i-index-1,:] = row2values(lines[i].replace('\n', ''))
        if i-index-1 != 0:
            matrix[i-index-1,:] += matrix[i-index-2,:]
    for col in range(1, m):
        matrix[:,col] += matrix[:,col-1]
    # if n_case == 6:
        # print(matrix)
    return get_max_sum(matrix, n_case)
    # output.write('Case #{}: {}\n'.format(n_case, get_max_sum(matrix, n_case)))
    # index += n+1
    # n_case += 1


# import pdb

index = 1
n_case = 1
import multiprocessing as mp
n_cores = 5

pool = mp.Pool(processes=n_cores)

atrbs, atrbsCase = [], []
while index < len(lines):
    n, m = [int(i) for i in lines[index].replace('\n', '').split(' ')]
    atrbs.append(index)
    atrbsCase.append(n_case)
    # To know what it is doing
    # if n_case % 10 == 0:
    #     print('Case #{}'.format(n_case))
    index += n+1
    n_case += 1
    if len(atrbs) == n_cores or index >= len(lines):
        results = pool.map(do_case, atrbs)
        for a_case, a_result in zip(atrbsCase, results):
            output.write('Case #{}: {}\n'.format(a_case, a_result))
        atrbs, atrbsCase = [], []



output.close()
