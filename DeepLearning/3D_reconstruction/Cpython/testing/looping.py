import time

def marching(n, m, p):
    cnt = 0
    for i in range(n):
        for j in range(m):
            for k in range(p):
                cnt += 1
    print(cnt)