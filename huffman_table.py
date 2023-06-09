import numpy as np

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
        
    # extract individual category and code word    
    table = table[0:category_num]
    # table = [[row[0][:-1], row[4]] for row in table]
    ht = {}
    for row in table:
        # print(row)
        ht[row[0][:-1]] = row[4]
    print(f'ht = {ht}')
    return ht
    




    
    
    
    
        
    

    
    
    
    

