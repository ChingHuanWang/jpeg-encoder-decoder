import numpy as np


def tune_table(table, category_num):
    
    # sort sym by code len
    table = table[0:category_num]
    sym_list = np.array([row[0][:-1] for row in table])
    code_list = np.array([row[4] for row in table])
    code_len_list = np.array([len(code) for code in code_list])
    sort = np.argsort(code_len_list)
    sym_list = sym_list[sort]
    code_list = code_list[sort]
    code_len_list = code_len_list[sort]
    
    
    # assign 
    code = "0"*code_len_list[0]
    final_code_list = [code]
    for code_len in code_len_list[1:]:
        if(code[-1] == '0'):
            code = code[:-1] + '1'
            code += '0'*abs(code_len-len(code))
        else:
            last_zero_idx = code.rfind('0')
            code = code[0:last_zero_idx]+'1'
            code += '0'*abs(code_len-len(code))
            
        final_code_list.append(code)
        
    if('0' not in final_code_list[-1]):
        final_code_list[-1] += '0'
    
    return [[sym, code] for sym, code in zip(sym_list, final_code_list)]
        
            

def huffman_table(prob, category):
    
    category_num = len(category)
    
    category = list(category)
    # init huffman table
    for i in range(len(category)):
        if isinstance(category[i], np.int32):
            category[i] = str(category[i]) + 'L'
        else:
            category[i] += 'L'
        
    node_set = dict(zip(category, list(range(len(category)))))
    table = [[] for i in range(len(prob))]

    for idx, sym in enumerate(category):
        table[idx] = [sym, prob[idx], -1, -1, ""]
        
    # generate rest row of table
    while(len(prob) != 1):

        new_prob = prob[-2] + prob[-1]

        if category[-2].count('L') > category[-1].count('L'):
            new_sym = category[-1] + category[-2]
            new_row = [new_sym, new_prob, node_set[category[-1]], node_set[category[-2]], ""]
        elif category[-2].count('L') == category[-1].count('L'):
            if category[-2][0] > category[-1][0]:
                new_sym = category[-1] + category[-2]
                new_row = [new_sym, new_prob, node_set[category[-1]], node_set[category[-2]], ""]
            else:
                new_sym = category[-2] + category[-1]
                new_row = [new_sym, new_prob, node_set[category[-2]], node_set[category[-1]], ""]
        else:
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
        
    table = tune_table(table, category_num)
    
    ht = {}
    for row in table:
        ht[row[0]] = row[1]
    return ht
    




    
    
    
    
        
    

    
    
    
    

