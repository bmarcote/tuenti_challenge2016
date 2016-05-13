import sys


path = open(sys.argv[1], 'r')
output = open(sys.argv[2], 'w')





n_case = 0
for line in path:#sys.stdin:
    if n_case != 0:


        output.write('Case #{}: {:0d}\n'.format(n_case, tables))
    n_case += 1

path.close()
output.close()
