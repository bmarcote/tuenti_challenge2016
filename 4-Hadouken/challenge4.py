import sys
from numpy import maximum
path = open(sys.argv[1], 'r')
output = open(sys.argv[2], 'w')


##  Moves:
# 1 R  - right        6 L  - left
# 2 RU - right up     7 LU - left up
# 3 RD - right down   8 LD - left down
# 4 D  - down         9 K  - kick
# 5 U  - up           0 P  - push
#
## Combos
# L LD D  RD R P
# D RD R  P
# R D  RD P
# D LD L  K
# R RD D  LD L K


moves = {'R': 1, 'RU': 2, 'RD':3, 'D':4, 'U':5, 'L':6, 'LU':7,
        'LD': 8, 'K': 9, 'P': 0}

combos = ('684310', '4310', '1430', '134869', '4869')

import pdb

def parser_move(move):
    return str(moves[move])


n_case = 0
for line in path:#sys.stdin:
    if n_case != 0:
        movement = ''.join([parser_move(a_move) for a_move in line.replace('\n', '').split('-')])
        n_almost = 0
        # got_first_move, got_second_move = False, False
        for a_combo in combos:
            next_pos = movement.find(a_combo[:-1])
            while next_pos != -1:
                # Check that he was not trying to do the long version
                check_this = True
                try:
                    if combos.index(a_combo)==1 and movement[next_pos-2:next_pos]=='68':
                        check_this = False
                    if combos.index(a_combo)==4 and movement[next_pos-2:next_pos]=='13':
                        check_this = False
                except:
                    pass
                finally:
                    if check_this:
                        if len(movement) == next_pos+len(a_combo)-1:
                            n_almost += 1
                        elif  movement[next_pos+len(a_combo)-1]!=a_combo[-1]:
                            n_almost += 1
                next_pos = movement.find(a_combo[:-1], next_pos+1)
        output.write('Case #{}: {:0d}\n'.format(n_case, n_almost))
    n_case += 1





##############################
n_case = 0
for line in path:#sys.stdin:
    if n_case != 0:
        movement = ''.join([parser_move(a_move) for a_move in line.replace('\n', '').split('-')])
        n_almost = 0
        got_first_move, got_second_move = False, False
        # if n_case == 3:
            # pdb.set_trace()
        for a_combo in combos:
            next_pos = movement.find(a_combo[:-1])
            while next_pos != -1:
                if len(movement) == next_pos+len(a_combo)-1:
                    if combos.index(a_combo) == 2:
                        if not got_first_move:
                            n_almost += 1
                    elif combos.index(a_combo) == 4:
                        if not got_second_move:
                            n_almost += 1
                    else:
                        if combos.index(a_combo) == 0:
                            got_first_move = True
                        elif combos.index(a_combo) == 1:
                            got_second_move = True
                        n_almost += 1
                elif len(movement) < next_pos+len(a_combo)-1:
                    # we missed by two
                    pass
                elif movement[next_pos+len(a_combo)-1] != a_combo[-1]:
                    if combos.index(a_combo) == 2:
                        if not got_first_move:
                            n_almost += 1
                    elif combos.index(a_combo) == 4:
                        if not got_second_move:
                            n_almost += 1
                    else:
                        if combos.index(a_combo) == 0:
                            got_first_move = True
                        elif combos.index(a_combo) == 1:
                            got_second_move = True
                        n_almost += 1

                next_pos = movement.find(a_combo[:-1], next_pos+1)
        output.write('Case #{}: {:0d}\n'.format(n_case, n_almost))
    n_case += 1


path.close()
output.close()
