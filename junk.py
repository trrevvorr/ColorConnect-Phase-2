# l = {}
# for i in xrange(4):
#     l[i] = '%d' % i
# for i in l:
#     print l[i]

from Queue import Queue

q = Queue()

q.put(1)
q.put(2)

while not q.empty():
    print q.get()
