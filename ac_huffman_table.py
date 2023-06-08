import numpy as np
from huffman_table import huffman_table

def get_lum_ac(ac):
    lum_ac = np.array([block[0:63*4] for block in ac])
    return lum_ac.flatten()

def get_chrom_cb_ac(ac):
    chrom_cb_ac = np.array([block[63*4:63*5] for block in ac])
    return chrom_cb_ac.flatten()

def get_chrom_cr_ac(ac):
    chrom_cr_ac = np.array([block[63*5:63*6] for block in ac])
    return chrom_cr_ac.flatten()

def lum_ac_huffman_table(ac):
    
    size_table = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    lum_ac = get_lum_ac(ac)