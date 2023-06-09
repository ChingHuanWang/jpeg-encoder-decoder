import numpy as np
from scipy.fftpack import dct, idct

def dct_2d(y, cb, cr):

    for i in range(2):
        for j in range(2):
            y[i * 8:(i + 1) * 8, j * 8:(j + 1) * 8] -= 128
            y[i * 8:(i + 1) * 8, j * 8:(j + 1) * 8] = dct(y[i * 8:(i + 1) * 8, j * 8:(j + 1) * 8].T, norm='ortho')
            y[i * 8:(i + 1) * 8, j * 8:(j + 1) * 8] = dct(y[i * 8:(i + 1) * 8, j * 8:(j + 1) * 8].T, norm='ortho')

    cb -= 128
    cb = dct(cb.T, norm='ortho')
    cb = dct(cb.T, norm='ortho')

    cr -= 128
    cr = dct(cr.T, norm='ortho')
    cr = dct(cr.T, norm='ortho')

    return y, cb, cr

def idct_2d(y, cb, cr):

    y = idct(np.transpose(y, (0, 2, 1)), norm='ortho', axis=2)
    y = idct(np.transpose(y, (0, 2, 1)), norm='ortho', axis=2)
    y = np.round(y + 128)

    cb = idct(np.transpose(cb, (0, 2, 1)), norm='ortho', axis=2)
    cb = idct(np.transpose(cb, (0, 2, 1)), norm='ortho', axis=2)
    cb = np.round(cb + 128)

    cr = idct(np.transpose(cr, (0, 2, 1)), norm='ortho', axis=2)
    cr = idct(np.transpose(cr, (0, 2, 1)), norm='ortho', axis=2)
    cr = np.round(cr + 128)

    return y, cb, cr
