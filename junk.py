# l = {}
# for i in xrange(4):
#     l[i] = '%d' % i
# for i in l:
#     print l[i]
import copy

p = [[1, 2], [3, 4]]
p2 = copy.deepcopy(p)

i = [0,1]
p[i[0]][i[1]] = 100

print 'p:', p
print 'p2:', p2
