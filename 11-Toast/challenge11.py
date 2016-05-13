import sys
import numpy as np

path = open(sys.argv[1], 'r')
output = open(sys.argv[2], 'w')

# It just follows a simple rule:
# for step i, we reach the numbers [ (N+i)M,  (N+2*i+1)M ]  except (N+2*i)M


def get_steps(n, m, k):
    if k % m != 0:
        return 'IMPOSSIBLE'
    min_i = lambda i : (n+i)*m
    max_i = lambda i : (n+2*i+1)*m
    no_i = lambda i : (n+2*i)*m

    i = np.ceil((k/m-n)/2)
    if k == 2*i+1:
        return int(i)
    elif k == no_i(i):
        return int(i+1)
    elif k in np.arange(min_i(i), max_i(i)+1, m):
        return int(i)
    else:
        return 'IMPOSSIBLE'

n_case = 0
for line in path:#sys.stdin:
    if n_case != 0:
        piles, slides, goal = [int(i) for i in line.split(' ')]
        steps = get_steps(piles, slides, goal)
        output.write('Case #{}: {}\n'.format(n_case, steps))
    n_case += 1

path.close()
output.close()
