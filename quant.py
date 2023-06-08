import numpy as np
from dct import dct_2d

def load_quantization_mat(type):
    
    if type == "lum":
        q_mat = np.array([[ 9.,  6., 18., 21., 23., 21., 21., 22.],
                          [ 7., 18., 16., 21., 21., 21., 22., 21.],
                          [16., 16., 21., 21., 15., 21., 27., 21.],
                          [18., 21., 21., 21., 21., 37., 33., 23.],
                          [21., 21., 21., 21., 26., 49., 46., 31.],
                          [16., 16., 21., 24., 33., 46., 51., 40.],
                          [16., 24., 32., 37., 46., 56., 55., 45.],
                          [29., 40., 41., 43., 51., 45., 46., 43.]])
        
    elif type == "chrom":
        q_mat = np.array([[10., 10., 14., 26., 45., 45., 45., 45.],
                          [10., 13., 16., 29., 45., 45., 45., 45.],
                          [14., 16., 29., 45., 45., 45., 45., 43.],
                          [23., 29., 43., 45., 45., 45., 45., 45.],
                          [45., 45., 45., 45., 45., 45., 45., 45.],
                          [45., 45., 43., 45., 45., 43., 43., 45.],
                          [45., 45., 45., 45., 45., 45., 45., 45.],
                          [45., 45., 45., 45., 45., 43., 45., 45.]])
        
    else:
        raise ValueError(
            f"type should be either lum or chrom, but {type} was found\n"
        )
        
    return q_mat

def quantize(dct_block: np.ndarray, type):
        
    q_mat = load_quantization_mat(type)
    quant_block = (dct_block / q_mat).round()
    
    return quant_block



