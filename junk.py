# l = {}
# for i in xrange(4):
#     l[i] = '%d' % i
# for i in l:
#     print l[i]

import time
start_time = time.time()
print 'Hello World'
print '== FINISHED IN %4.4f MILLISECONDS ==' % ((time.time() - start_time)*1000000)
