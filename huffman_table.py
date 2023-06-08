import numpy as np

def get_lum_dc(dc):
    return np.array([dc for idx, dc in enumerate(dc) if 0 <= idx%6 <= 3])

def get_chrom_rb_dc(dc):
    return np.array([dc for idx, dc in enumerate(dc) if idx%6 == 4])

def get_chrom_rc_dc(dc):
    return np.array([dc for idx, dc in enumerate(dc) if idx%6 == 5])

def dec2bin(n):
    return bin(n).replace("0b", "")

def get_prob_and_category(component):
    component_diff = component
    component_diff[1:] -= component[0:-1]
    component_diff = abs(component_diff)
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

def huffman_table(prob, category):
    
    category_num = len(category)
    
    # init huffman table
    for i in range(len(category)):
        category[i] = str(i) + "L"
        
        
    node_set = dict(zip(category, list(range(len(category)))))
    table = [[] for i in range(len(prob))]

    for idx, sym in enumerate(category):
        table[idx] = [sym, prob[idx], -1, -1, ""]
        
    # generate rest row of table
    while(len(prob) != 1):
        
        new_prob = prob[-2] + prob[-1]
        new_sym = category[-2] + category[-1]
        new_row = [new_sym, new_prob, node_set[category[-2]], node_set[category[-1]], ""]
        table = [*table, new_row]
        node_set[new_sym] = len(node_set)
        prob = np.array([*prob[:-2], new_prob])
        category = np.array([*category[:-2], new_sym])
        
        sort = np.argsort(prob)
        prob = np.flip(prob[sort])
        category = np.flip(category[sort])
        
    # generate code word
    for i in range(len(table)-1, -1, -1):
        
        left_node_idx = table[i][2]
        right_node_idx = table[i][3]
        if(left_node_idx == -1 and right_node_idx ==-1):
            continue
        
        comm_seq = table[i][4]
        table[left_node_idx][4] = comm_seq + "0"
        table[right_node_idx][4] = comm_seq + "1"
        
    # extract individual category and code word    
    table = table[0:category_num]
    table = [[row[0][:-1], row[4]] for row in table]
    return table
    

def lum_dc_huffman_table(dc):
    
    lum_dc = get_lum_dc(dc)
    prob, category = get_prob_and_category(lum_dc)
    return huffman_table(prob, category)

def chrom_dc_huffman_table(dc):
    
    rb_dc = get_chrom_rb_dc(dc)
    rc_dc = get_chrom_rc_dc(dc)
    
    rb_prob, rb_category = get_prob_and_category(rb_dc)
    rc_prob, rc_category = get_prob_and_category(rc_dc)
    
    rb_category_len = len(rb_category)
    rc_category_len = len(rc_category)
    
    max_category_len = max(rb_category_len, rc_category_len)
    category = np.array(list(range(max_category_len)))
    prob = np.zeros(max_category_len)
    
    for i in range(len(category)):
        
        p1 = rb_prob[i] if i < rb_category_len else 0
        p2 = rc_prob[i] if i < rc_category_len else 0
        prob[i] = (p1+p2) / 2
        
    sort = np.argsort(prob)
    prob = np.flip(prob[sort])
    category = list(np.flip(category[sort]))
        
    return huffman_table(prob, category)
    
        
    

    
    
    
    

