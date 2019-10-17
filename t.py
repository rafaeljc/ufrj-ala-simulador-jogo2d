import numpy as np

m = np.array([[2.0, 3.0, 4.0, 5.0],
              [2.0, 3.0, 4.0, 5.0],
              [1.0, 1.0, 1.0, 1.0]])

print(m[:,0])

for i in range(m.shape[1] - 1):
    p1 = (m[0,i], m[1,i])
    p2 = (m[0,i+1], m[1,i+1])
    print(p1)
    print(p2)