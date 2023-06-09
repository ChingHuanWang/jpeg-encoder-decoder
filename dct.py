from math import *
import numpy as np

def dct(y,cb,cr):
    dct_y = dct_main(y)
    dct_cb = dct_main(cb)
    dct_cr = dct_main(cr)
    return dct_y, dct_cb, dct_cr
def idct(dct_y, dct_cb, dct_cr):
    y = idct_main(dct_y)
    cb = idct_main(dct_cb)
    cr = idct_main(dct_cr)
    return y,cb,cr
def dct_main(matrix):
    N = len(matrix)
    D = np.zeros((N,N))
    for i in range(N):
        for j in range(N):
            Ci = C(i)
            Cj = C(j)
            summation = 0
            for x in range(N):
                for y in range(N):
                    f = matrix[x][y]
                    summation = summation+f*cos(((2*x+1)*i*pi)/(2*N))*cos(((2*y+1)*j*pi)/(2*N))
            D[i,j] = 1/(2*sqrt(2*N))*Ci*Cj*summation
    D = D.tolist()
    return D
def idct_main(D):
    N = len(D)
    matrix = np.zeros((N,N))
    for x in range(N):
        for y in range(N):
            summation = 0
            for i in range(N):
                for j in range(N):
                    Ci = C(i)
                    Cj = C(j)
                    d = D[i][j]
                    summation = summation+Ci*Cj*d*cos(((2*x+1)*i*pi)/(2*N))*cos(((2*y+1)*j*pi)/(2*N))
            matrix[x,y] = int(1/(2*sqrt(2*N))*summation)
    matrix = matrix.tolist()
    return matrix
def C(x):
    if x==0:
        return 1/sqrt(2)
    else:
        return 1
