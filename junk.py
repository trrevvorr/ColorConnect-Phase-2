# l = {}
# for i in xrange(4):
#     l[i] = '%d' % i
# for i in l:
#     print l[i]
import random
random.seed()

p = [[0,1], [1,2]]
p2 = p.remove([0,1])
print p2
