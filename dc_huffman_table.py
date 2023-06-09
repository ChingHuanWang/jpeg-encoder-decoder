import numpy as np
from huffman_table import huffman_table
from utils import dec2bin, remove_dummy

def get_lum_dc(dc):
    lum_dc = np.array([block[0:4] for block in dc])
    return lum_dc.flatten()

def get_chrom_cb_dc(dc):
    return np.array([block[4] for block in dc])

def get_chrom_cr_dc(dc):
    return np.array([block[5] for block in dc])


def get_prob_and_category(component):
    component_diff = component
    component_diff[1:] -= component[0:-1]
    component_diff = abs(component_diff)
    print(f'component_diff = {component_diff}')
    component_diff = component_diff.astype(int)
    component_diff_len = np.array([len(dec2bin(diff)) for diff in component_diff])
    
    prob = np.zeros(max(component_diff_len)+1)
    prob[0] = sum(component_diff == 0)
    prob[1] = sum(component_diff == 1)
    bin_seq_len = list(range(2, max(component_diff_len)+1))
    for l in bin_seq_len:
        prob[l] = sum(component_diff_len == l)
        
    prob = np.divide(prob, component_diff.shape[0])
    category = np.array(list(range(max(component_diff_len)+1)))
    
    # sort prob and category in descending order
    sort = np.argsort(prob)
    prob = np.flip(prob[sort])
    category = np.flip(category[sort])
    
    return prob, list(category)


def lum_dc_huffman_table(dc):
    
    lum_dc = get_lum_dc(dc)
    prob, category = get_prob_and_category(lum_dc)
    prob, category = remove_dummy(prob, category)
    return huffman_table(prob, category)

def chrom_dc_huffman_table(dc):
    
    cb_dc = get_chrom_cb_dc(dc)
    cr_dc = get_chrom_cr_dc(dc)
    
    cb_prob, cb_category = get_prob_and_category(cb_dc)
    print(f'cb_prob = {cb_prob}, cb_category = {cb_category}')
    cr_prob, cr_category = get_prob_and_category(cr_dc)
    print(f'cr_prob = {cr_prob}, cr_category = {cr_category}')
    
    cb_category_len = max(cb_category)
    cr_category_len = max(cr_category)
    
    max_category_len = max(cb_category_len, cr_category_len)
    category = np.array(list(range(max_category_len + 1)))
    prob = np.zeros(max_category_len + 1)
    
    for i in range(len(category)):
        
        if i in cb_category:
            print(f'cb_category.index({i}) = {cb_category.index(i)}')
            print(cb_prob[cb_category.index(i)])

        if i in cr_category:
            print(f'cr_category.index({i}) = {cr_category.index(i)}')
            print(cr_prob[cr_category.index(i)])


        p1 = cb_prob[cb_category.index(i)] if i in cb_category else 0
        p2 = cr_prob[cr_category.index(i)] if i in cr_category else 0
        prob[i] = (p1+p2) / 2
        
    prob, category = remove_dummy(prob, category)
    sort = np.argsort(prob)
    prob = np.flip(prob[sort])
    category = list(np.flip(category[sort]))
    
    print(f'prob = {prob}, category = {category}')

    return huffman_table(prob, category)
