import numpy as np
from dct import dct_2d
from quant import quantize
from color_space import rgd_2_ycbcr

def dec2bin(n):
    return bin(n).replace("0b", "")


def remove_dummy(prob: np.array, category: np.array):
    index = [idx for idx, p in enumerate(prob) if p == 0]
    return np.delete(prob, index), np.delete(category, index)
            

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




def img_2_dc_ac(img):
    
    rows, cols, _ = img.shape
    
    blocks_count = (rows // 16) * (cols // 16)
    if(rows % 16 != 0 or cols % 16 != 0):
        raise ValueError(("the width and height of the image "
                          "should both be mutiples of 8"))
    
    dc = np.zeros((blocks_count, 6))
    ac = np.zeros((blocks_count, 63*6))
    block_idx = 0
    
    for i in range(0, rows, 16):
        for j in range(0, cols, 16):
            mcu = img[i:i+16, j:j+16, :]
            
            y, cb, cr = rgd_2_ycbcr(mcu)
            dct_y, dct_cb, dct_cr = dct_2d(y, cb, cr)
            
            # do quantize
            quant_y_1 = quantize(dct_y[0:8, 0:8], "lum")
            quant_y_2 = quantize(dct_y[0:8, 8:16], "lum")
            quant_y_3 = quantize(dct_y[8:16, 0:8], "lum")
            quant_y_4 = quantize(dct_y[8:16, 8:16], "lum")
            quant_cb = quantize(dct_cb, "chrom")
            quant_cr = quantize(dct_cr, "chrom")
            
            # do zigzag
            zz_y_1 = block_2_zigzag(quant_y_1)
            zz_y_2 = block_2_zigzag(quant_y_2)
            zz_y_3 = block_2_zigzag(quant_y_3)
            zz_y_4 = block_2_zigzag(quant_y_4)
            zz_cb = block_2_zigzag(quant_cb)
            zz_cr = block_2_zigzag(quant_cr)
            
            
            # import pdb; pdb.set_trace()
            dc[block_idx, :] = np.array([zz_y_1[0], zz_y_2[0], zz_y_3[0], zz_y_4[0], zz_cb[0], zz_cr[0]]) 
            ac[block_idx, :] = np.concatenate((zz_y_1[1:], zz_y_2[1:], zz_y_3[1:], zz_y_4[1:], zz_cb[1:], zz_cr[1:]), axis=None)
                
    return dc, ac
                
            
    
    
