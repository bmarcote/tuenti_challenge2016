import sys
from collections import defaultdict
import pdb
path = open(sys.argv[1], 'r')
output = open('submitOutput', 'w')

corpus = open('corpus.txt','r').readlines()[0].split(' ')
if corpus[-1] == '':
    corpus.pop(-1)


n_case = 0
for line in path:
    if n_case != 0:
        # pdb.set_trace()
        a, b = [int(l) for l in line.split()]
        subcorpus = corpus[a-1:b] 
        freqs = defaultdict(int)
        while len(subcorpus)>0:
            freqs[subcorpus.pop()] += 1

        freqs_sorted = sorted(freqs, key=freqs.get, reverse=True)
        s = ','.join(['{} {}'.format(word, freqs[word]) for word in freqs_sorted[:3]])
        output.write('Case #{}: {}\n'.format(n_case, s))
    n_case += 1




path.close()
output.close()
