import numpy as np
from dct import dct_2d

def load_quantization_mat(type):
    
    if type == "lum":
        q_mat = np.array([[2, 2, 2, 2, 3, 4, 5, 6],
                      [2, 2, 2, 2, 3, 4, 5, 6],
                      [2, 2, 2, 2, 4, 5, 7, 9],
                      [2, 2, 2, 4, 5, 7, 9, 12],
                      [3, 3, 4, 5, 8, 10, 12, 12],
                      [4, 4, 5, 7, 10, 12, 12, 12],
                      [5, 5, 7, 9, 12, 12, 12, 12],
                      [6, 6, 9, 12, 12, 12, 12, 12]])
        
    elif type == "chrom":
        q_mat = np.array([[3, 3, 5, 9, 13, 15, 15, 15],
                      [3, 4, 6, 11, 14, 12, 12, 12],
                      [5, 6, 9, 14, 12, 12, 12, 12],
                      [9, 11, 14, 12, 12, 12, 12, 12],
                      [13, 14, 12, 12, 12, 12, 12, 12],
                      [15, 12, 12, 12, 12, 12, 12, 12],
                      [15, 12, 12, 12, 12, 12, 12, 12],
                      [15, 12, 12, 12, 12, 12, 12, 12]])
        
    else:
        raise ValueError(
            f"type should be either lum or chrom, but {type} was found\n"
        )
        
    return q_mat

def quantize(block: np.ndarray, type):
        
    q_mat = load_quantization_mat(type)
    dct_block = dct_2d(block)
    quant_block = (dct_block / q_mat).round()
    
    return quant_block

def move_up_right(start_point, block):
    row, col = start_point[0], start_point[1]
    end_point = [col, row]
    points = []
    while([row, col] != end_point):
        points.append(block[row][col])
        row -= 1
        col += 1
    points.append(block[row][col])
    return points, [row, col]

def move_down_left(start_point, block):
    row, col = start_point[0], start_point[1]
    end_point = [col, row]
    points = []
    while([row, col] != end_point):
        points.append(block[row][col])
        col -= 1
        row += 1
    points.append(block[row][col])
    return points, [row, col]

def block_2_zigzag(block: np.array):
    
    row, col = block.shape
    zz = []
    start_point = [0, 0]
    while(start_point != [row-1, col-1]):
        # print(start_point)
        if(start_point[1] == 0 or start_point[0] == row-1):
            points, start_point = move_up_right(start_point, block)
            zz += points
        else:
            points, start_point = move_down_left(start_point, block)
            zz += points
            
        if(start_point[0] == 0 and start_point[1] == 0):
            start_point[1] += 1
            
        elif(start_point[0] == 0):
            if(start_point[1] == col-1):
                start_point[0] += 1
            else:
                start_point[1] += 1
        
        elif(start_point[1] == 0):
            if(start_point[0] == row-1):
                start_point[1] += 1
            else:
                start_point[0] += 1
            
        elif(start_point[0] == row-1):
            start_point[1] += 1
            
        else:
            start_point[0] += 1
        
    zz.append(block[row-1][col-1])
        
    return np.array(zz)
    
    


