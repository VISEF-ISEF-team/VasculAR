cimport cython
import time

@cython.boundscheck(False)
@cython.wraparound(False)

def marching(int n, int m, int p):
    cdef int cnt=0
    cdef int i,j,k

    for i in range(n):
        for j in range(m):
            for k in range(p):
                cnt+=1
                
    print(cnt)