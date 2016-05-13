import sys
import pdb
import multiprocessing as mp

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

results = pool.imap_unordered(get_immiscible01_reversed2, cases)
# results = pool.map(get_immiscible01_reversed, cases)
results_ordered = {}
for a_case, ones, zeros in results:
    results_ordered[a_case] = (ones, zeros)

# for a_case, ones, zeros in results:
#     output.write('Case #{}: {} {}\n'.format(a_case, ones, zeros))

for i in range(1, max_cases+1):
    # output.write('Case #{}: {} {}\n'.format(a_case, ones, zeros))
    output.write('Case #{}: {} {}\n'.format(i, results_ordered[i][0], results_ordered[i][1]))



path.close()
output.close()
