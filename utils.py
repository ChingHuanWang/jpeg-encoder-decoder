import numpy as np
from dct import dct_2d
from quant import quantize

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


def zigzag_2_dc(zigzag):
    return zigzag[0]

def zigzag_2_ac(zigzag):
    return zigzag[1:]


def img_2_dc_ac(img):
    
    rows, cols, _ = img.shape
    
    blocks_count = (rows // 8) * (cols // 8)
    if(rows % 8 != 0 or cols % 8 != 0):
        raise ValueError(("the width and height of the image "
                          "should both be mutiples of 8"))
    
    dc = np.empty((blocks_count, 3))
    ac = np.empty((blocks_count, 63, 3))
    block_idx = 0
    
    for i in range(0, rows, 8):
        for j in range(0, cols, 8):
            for k in range(3):
                block = img[i:i+8, j:j+8, k] - 128
                dct_block = dct_2d(block)
                quant_block = quantize(dct_block, 'lum' if k == 0 else 'chrom')
                zigzag = block_2_zigzag(quant_block)
                
                dc[block_idx, k] = zigzag_2_dc(zigzag)
                ac[block_idx, :, k] = zigzag_2_ac(zigzag)
                
    return dc, ac
                
            
    
    
