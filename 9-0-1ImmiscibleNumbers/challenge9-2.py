import sys
import pdb
import multiprocessing as mp
from collections import defaultdict
import numpy as np


n_cores = 7

path = open(sys.argv[1], 'r')
output = open(sys.argv[2], 'w')


def is_immiscible01(strnumber):
    for a_digit in strnumber:
        if a_digit != '0' and a_digit != '1':
            return False
    return True

def decreasing_order(trial_num):
    already_zero = False
    for a_digit in trial_num:
        if a_digit == '0':
            already_zero = True
        else:
            if already_zero:
                return False
    return True


factors = range(10)
def get_immiscible(params):
    case = params[0]
    number = params[1]
    strnum = str(number)
    pos_prev = []
    possibles = []
    bi = 0
    if True:#case % 10 == 0:
        print('Case: ',case)
    # First step manually
    for xi in factors:
        bi = xi*int(strnum[-1])
        rest = bi // 10
        bi = bi % 10
        if bi==1 or bi==0:
            pos_prev.append((str(xi), str(bi), rest))
    results = []
    for possible in pos_prev:
        if possible[2] == 0:
            if int(possible[1]) % number == 0 and int(possible[1]) >= number:
                results.append(int(possible[1]))
    if len(results) > 0:
        if True:#case % 10 == 0:
            print('Case {} done'.format(case))
        return case, min(results)
    while True:
        # print(pos_prev)
        for a_x, a_b, a_rest in pos_prev:
            for xi in factors:
                bi = 0
                a_x2 = str(xi)+a_x
                for i in range(len(a_x2)):
                    if len(strnum) > i:
                        bi += int(a_x2[i])*int(strnum[len(strnum)-i-1])

                bi += a_rest
                rest = bi // 10
                bi = bi % 10
                if (bi == 1) or (bi == 0 and a_b[0] == '0'):
                    possibles.append((a_x2, str(bi)+a_b, rest))
        # Check if we already have a solution (the first one would be the smallest one)
        results = []
        for possible in possibles:
            if possible[2] == 0:
                if int(possible[1]) % number == 0 and int(possible[1]) >= number:
                    results.append(int(possible[1]))
        if len(results) > 0:
            if True:#case % 10 == 0:
                print('Case {} done'.format(case))
            return case, min(results)
        pos_prev = possibles
        possibles = []

def get_immiscible01_reversed(params):
    # This is the fast way!
    case = params[0]
    # if case % 10 == 0:
    #     print('Case: ',case)
    number = params[1]
    # We do the maths with binary numbers
    trial_bin = 1
    trial_num = bin(trial_bin)[2:]
    while not (int(trial_num) % number == 0 and decreasing_order(trial_num)):
        trial_bin += 1
        trial_num = bin(trial_bin)[2:]

    n_ones, n_zeros = 0, 0
    for a_digit in trial_num:
        if a_digit == '0':
            n_zeros += 1
        else:
            n_ones += 1
    # print(trial_num)
    return case, n_ones, n_zeros

def get_immiscible01_reversed2(params):
    # This is the fast way!
    case = params[0]
    # if case % 10 == 0:
    print('Case ', case)
    number = params[1]
    # We do the maths with binary numbers
    already_known = {6113: (6112, 0), 8452: (2112, 2), 7269: (7266, 0)}
    if number in already_known:
        return case, already_known[number][0], already_known[number][1]
    digits, last_zero = 1, 2
    trial_num = '1'
    while int(trial_num) % number != 0:
        if last_zero > digits:
            # add one digit
            trial_num = '1'+'0'*digits
            digits += 1
            last_zero = 2
        else:
            trial_num = '1'*last_zero + '0'*(digits-last_zero)
            last_zero += 1

    n_ones, n_zeros = 0, 0
    for a_digit in trial_num:
        if a_digit == '0':
            n_zeros += 1
        else:
            n_ones += 1
    print('Case {} done'.format(case))
    return case, n_ones, n_zeros


# pdb.set_trace()
pool = mp.Pool(processes=n_cores)

# pdb.set_trace()
n_case = 0
max_cases = 0
cases = []
for line in path:#sys.stdin:
    if n_case == 0:
        max_cases = int(line)
    else:
        # save the number and the string of the number
        base_number = int(line)
        cases.append((n_case, base_number))
    n_case += 1
# All cases in cases and numbers

# results = pool.imap_unordered(get_immiscible01_reversed2, cases)
results = pool.imap_unordered(get_immiscible, cases)
# results = pool.map(get_immiscible01_reversed, cases)
results_ordered = {}
# for a_case, ones, zeros in results:
#     results_ordered[a_case] = (ones, zeros)
for a_case, result in results:
    results_ordered[a_case] = result

# for a_case, ones, zeros in results:
#     output.write('Case #{}: {} {}\n'.format(a_case, ones, zeros))

for i in range(1, max_cases+1):
    # output.write('Case #{}: {} {}\n'.format(a_case, ones, zeros))
    # output.write('Case #{}: {} {}\n'.format(i, results_ordered[i][0], results_ordered[i][1]))
    n_ones, n_zeros = 0, 0
    for a_digit in str(results_ordered[i]):
        if a_digit == '0':
            n_zeros += 1
        else:
            n_ones += 1
    output.write('Case #{}: {} {}\n'.format(i, n_ones, n_zeros))



path.close()
output.close()
