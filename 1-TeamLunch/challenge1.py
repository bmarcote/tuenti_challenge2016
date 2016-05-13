import sys
from numpy import maximum
path = open(sys.argv[1], 'r')
output = open('submitOutput', 'w')

n_case = 0
for line in path:#sys.stdin:
    if n_case != 0:
        tables = (int(line)+1)//2-1
        if tables < 0:
            tables = 0
        elif tables==0 and int(line)>0:
            tables = 1
        output.write('Case #{}: {:0d}\n'.format(n_case, tables))
    n_case += 1

path.close()
output.close()
