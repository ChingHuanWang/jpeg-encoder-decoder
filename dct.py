from scipy import fftpack

def dct_2d(block):
    return fftpack.dct(fftpack.dct(block.T, norm='ortho').T, norm='ortho')