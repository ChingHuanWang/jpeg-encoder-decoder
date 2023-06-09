import numpy as np
from huffman_table import huffman_table
from utils import dec2bin

def get_lum_ac(ac):
    lum_ac = np.array([block[0:63*4] for block in ac])
    return lum_ac.flatten()

def get_chrom_cb_ac(ac):
    chrom_cb_ac = np.array([block[63*4:63*5] for block in ac])
    return chrom_cb_ac.flatten()

def get_chrom_cr_ac(ac):
    chrom_cr_ac = np.array([block[63*5:63*6] for block in ac])
    return chrom_cr_ac.flatten()

def init_prob_and_category():
    run_table = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]
    size_table = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A"]
    category = ["0/0"]
    for r in run_table:
        for s in size_table:
            category.append(r+"/"+s)
            
    prob = np.zeros(len(category))
    return prob, category

def last_nonzero_idx(seq):
    for idx, e in reversed(list(enumerate(seq))):
        if(e != 0):
            return idx
    return 0

def parse_seq(seq, prob_dict):
    
    size_table = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A"]
    hex_dict = { 0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 
                 8: "8", 9: "9", 10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F"}
    k = last_nonzero_idx(seq)
    run = 0
    for i in range(k+1):
        if(seq[i] > 0 or seq[i] < 0):
            tmp = abs(seq[i])
            bin_tmp = dec2bin(tmp)
            size = size_table[len(bin_tmp)-1]
            sym = hex_dict[run]+"/"+size
            prob_dict[sym] += 1
            run = 0
        else:
            if(run == 15):
                sym = "F/0"
                prob_dict[sym] += 1
                run = 0
            else:
                run += 1
                
    prob_dict["0/0"] += 1
    return prob_dict
    

def get_prob_and_category(component):
    
    prob, category = init_prob_and_category()
    prob_dict = dict(zip(category, prob))
    
    for i in range(0, len(component), 63):
        seq = component[i:i+63]
        prob_dict = parse_seq(seq, prob_dict)
        
    category = list(prob_dict.keys())
    prob = np.array(list(prob_dict.values()))
    prob = np.divide(prob, sum(prob))
    
    return prob, category
    
    
def lum_ac_huffman_table(ac):
    
    lum_ac = get_lum_ac(ac)
    prob, category = get_prob_and_category(lum_ac)
    return huffman_table(prob, category)

def chrom_ac_huffman_table(ac):
    
    chrom_cb_ac = get_chrom_cb_ac(ac)
    chrom_cr_ac = get_chrom_cr_ac(ac)
    
    cb_prob, cb_category = get_prob_and_category(chrom_cb_ac)
    cr_prob, cr_category = get_prob_and_category(chrom_cr_ac)
    
    category = cb_category
    prob = np.divide(cb_prob+cr_prob, 2)
    
    return huffman_table(prob, category)
    