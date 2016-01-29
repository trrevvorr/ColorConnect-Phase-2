# l = {}
# for i in xrange(4):
#     l[i] = '%d' % i
# for i in l:
#     print l[i]
import random
random.seed()

p = [[1, 2], [3, 4]]

random.shuffle(p)
print p
