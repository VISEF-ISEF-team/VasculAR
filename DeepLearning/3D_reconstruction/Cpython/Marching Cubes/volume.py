class FenwickTree3D():
    def __init__(self, V, n, m, p):
        self.V = V
        self.n = n
        self.m = m
        self.p = p
        self.bit = [[[0] * (p + 1) for _ in range(m + 1)] for _ in range(n + 1)]

    def update(self, x, y, z, val):
        x += 1
        y += 1
        z += 1
        while (x <= self.n):
            y1 = y
            while (y1 <= self.m):
                z1 = z
                while (z1 <= self.p):
                    self.bit[x][y1][z1] += val
                    z1 += z1 & -z1
                y1 += y1 & -y1
            x += x & -x

    def getSum(self, x, y, z):
        x += 1
        y += 1
        z += 1
        res = 0
        while x > 0:
            y1 = y
            while y1 > 0:
                z1 = z
                while (z1 > 0):
                    res += self.bit[x][y1][z1]
                    z1 -= z1 & -z1
                y1 -= y1 & -y1
            x -= x & -x
        return res

    def queryByRange(self, x1, y1, z1, x2, y2, z2):
        return self.getSum(x2, y2, z2) - self.getSum(x2, y2, z1 - 1) - self.getSum(x2, y1 - 1, z2) + self.getSum(x2, y1 - 1, z1 - 1) \
               - self.getSum(x1 - 1, y2, z2) + self.getSum(x1 - 1, y2, z1 - 1) + self.getSum(x1 - 1, y1 - 1, z2) - self.getSum(x1 - 1, y1 - 1, z1 - 1)

# Initialize Fenwick tree
n, m, p = V.shape
fenwick_tree = FenwickTree3D(V, n, m, p)

# Build Fenwick tree
for i in range(n):
    for j in range(m):
        for k in range(p):
            fenwick_tree.update(i, j, k, V[i][j][k])