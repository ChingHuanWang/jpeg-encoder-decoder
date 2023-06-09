import numpy as np
from scipy.fftpack import idct

def idct_2d(y, cb, cr):

    y = idct(np.transpose(y, (0, 2, 1)), norm='ortho', axis=2)
    y = idct(np.transpose(y, (0, 2, 1)), norm='ortho', axis=2)
    y = np.round(y + 128)
    # y = np.round(y)

    cb = idct(np.transpose(cb, (0, 2, 1)), norm='ortho', axis=2)
    cb = idct(np.transpose(cb, (0, 2, 1)), norm='ortho', axis=2)
    cb = np.round(cb + 128)
    # cb = np.round(cb)

    cr = idct(np.transpose(cr, (0, 2, 1)), norm='ortho', axis=2)
    cr = idct(np.transpose(cr, (0, 2, 1)), norm='ortho', axis=2)
    cr = np.round(cr + 128)

    return y, cb, cr