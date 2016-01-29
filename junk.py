# l = {}
# for i in xrange(4):
#     l[i] = '%d' % i
# for i in l:
#     print l[i]
import random
random.seed()

import time
start_time = time.time()

p = [[0,1], [1,2]]
p.remove([0,1])
print p

print("--- %s seconds ---" % (time.time() - start_time))
