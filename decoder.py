import argparse
import math
import numpy as np

from bitstring import BitArray
from PIL import Image
from struct import unpack
import time

from dct import idct_2d
from quant import dequantization
from sample import upsample
from color_space import ycbcr2rgb

class Huffman_Tree:

    def __init__(self, depth=0, node=None, is_symbol=False, binary=''):
        self.left = None
        self.right = None
        self.node = node
        self.is_symbol = is_symbol
        self.depth = depth
        self.binary = binary

    def insert(self, data):
        
        is_insert = False

        # left
        if self.left is not None and not self.left.is_symbol:
            is_insert = self.left.insert(data)
        elif self.left is None and self.depth + 1 != data[0]:
            self.left = Huffman_Tree(self.depth + 1, binary=self.binary + '0')
            is_insert = self.left.insert(data)
        elif self.left is None and self.depth + 1 == data[0]:
            self.left = Huffman_Tree(self.depth + 1, data[1], True, self.binary + '0')
            return True
        
        if is_insert:
            return True
        
        # right
        if self.right is not None and not self.right.is_symbol:
            return self.right.insert(data)
        elif self.right is None and self.depth + 1 != data[0]:
            self.right = Huffman_Tree(self.depth + 1, binary=self.binary + '1')
            return self.right.insert(data)
        elif self.right is None and self.depth + 1 == data[0]:
            self.right = Huffman_Tree(self.depth + 1, data[1], True, binary=self.binary + '1')
            return True

    def get_table(self, table):
        if self.left is not None:
            table = self.left.get_table(table)
        if self.is_symbol:
            table[self.binary] = self.node
        if self.right is not None:
            table = self.right.get_table(table)
        return table

def inv_zigzag(data):
    """
        
    """
    table = np.zeros((8, 8))
    i, direct = 0, -1
    ptr = 0
    for k in range(15):
        while True:
            j = k - i
            table[i, j] = data[ptr]
            ptr += 1
            if i + direct < 0 or i + direct >= 8:
                break
            if j - direct < 0 or j - direct >= 8:
                break
            i += direct
        direct = -direct
        if direct == -1 and k < 7:
            i += 1
        elif direct == 1 and k >= 7:
            i += 1
    return table

def get_qt(data):

    """
        Get quantization tables
        Args:
            data:
        Returns:
    """

    length = len(data)
    ptr = 2
    qts = []
    tqs = []
    while ptr < length:
        pq, tq = data[ptr] >> 4, data[ptr] % 16
        table_len = 64 * (1 + pq)
        dtype = np.uint8 if pq == 0 else np.uint16
        table = np.frombuffer(data[ptr + 1:ptr + 1 + table_len], dtype=dtype)
        table = inv_zigzag(table)
        ptr += 1 + table_len
        tqs.append(tq)
        qts.append(table)

    return tqs, qts

def get_img_info(data):

    infos = {}
    infos["precision"] = data[2]
    (infos["height"], ) = unpack(">H", data[3:5])
    (infos["width"], ) = unpack(">H", data[5:7])
    infos["n_components"] = data[7]
    sampling_factor = [[] for i in range(infos["n_components"])]
    quantization_table = [0] * infos["n_components"]
    ptr = 8
    for i in range(infos["n_components"]):
        
        assert len(data) >= ptr + 3

        component_id = data[ptr] - 1
        h_fs, w_fs = data[ptr + 1] >> 4, data[ptr + 1] % 16
        sampling_factor[component_id] = [h_fs, w_fs]
        quantization_table[component_id] = data[ptr + 2]
        ptr += 3
    infos["sampling_factor"] = sampling_factor
    infos["quantization_table"] = quantization_table

    return infos

def get_huffman_table(data):

    # get huffman table info
    infos = []
    tmp = "DC" if data[2] >> 4 == 0 else "AC"
    infos.append(tmp)
    infos.append(data[2] % 16)

    lengths = np.frombuffer(data[3:19], dtype=np.uint8)
    num_sym_pair = []
    ptr = 19
    for i, num in enumerate(lengths):
        for j in range(num):
            num_sym_pair.append([i + 1, data[ptr]])
            ptr += 1

    ht = Huffman_Tree()
    for d in np.array(num_sym_pair):
        ht.insert(d)
    table = {}
    table = ht.get_table(table)

    return infos, table

def get_sos_infos(data):

    infos = {}
    n_components = data[2]
    infos["n_components"] = n_components
    ptr = 3
    component_data = []
    for i in range(n_components):
        component_data.append([data[ptr], data[ptr + 1] >> 4, data[ptr + 1] % 16])
        ptr += 2
    infos["component_data"] = np.array(component_data)
    infos["skip"] = np.frombuffer(data[ptr:ptr+3], dtype=np.uint8)
    
    return infos

def remove_ff00(data):
    
    tmp = data.find(b'\xff\x00')
    while tmp != -1:
        data = data[:tmp+1] + data[tmp+2:]
        tmp = data.find(b'\xff\x00')
    return data

def build_matrix(dc_y, ac_ys, dc_cb, ac_cbs, dc_cr, ac_crs):

    y = np.zeros((len(dc_y), 64))
    cb = np.zeros((len(dc_cb), 64))
    cr = np.zeros((len(dc_cr), 64))

    dc_y = np.cumsum(dc_y)
    dc_cb = np.cumsum(dc_cb)
    dc_cr = np.cumsum(dc_cr)

    y[:, 0], y[:, 1:] = dc_y, ac_ys
    cb[:, 0], cb[:, 1:] = dc_cb, ac_cbs
    cr[:, 0], cr[:, 1:] = dc_cr, ac_crs

    y = np.array([inv_zigzag(data) for data in y])
    cb = np.array([inv_zigzag(data) for data in cb])
    cr = np.array([inv_zigzag(data) for data in cr])
    
    return y, cb, cr

def decode_compressed_data(data, sof_infos, sos_infos, dc_hts, ac_hts):

    # remove \xff\x00
    data = remove_ff00(data)

    c = BitArray(data).bin
    
    sampling_factor = sof_infos["sampling_factor"]
    h, w = sof_infos["height"], sof_infos["width"]
    component_data = sos_infos["component_data"]
    mcu_num = math.ceil(h / (8 * sampling_factor[0][0])) * math.ceil(w / (8 * sampling_factor[0][1]))
    ptr = 0
    dc_y, ac_ys = [], []
    dc_cb, ac_cbs = [], []
    dc_cr, ac_crs = [], []
    for k in range(mcu_num):
        for i, (a, b) in enumerate(sampling_factor):
            comp, dc_table, ac_table = sos_infos["component_data"][i]
            for j in range(a * b):
                # DC
                ptr_add = 1
                while c[ptr:ptr + ptr_add] not in dc_hts[dc_table].keys():
                    ptr_add += 1
                    if ptr_add > 16:
                        raise ValueError(f'ptr_add > 16')
                sym = dc_hts[dc_table][c[ptr:ptr + ptr_add]]
                ptr += ptr_add

                if sym == 0:
                    value = 0
                else:
                    if c[ptr] == '1':
                        value = int(c[ptr:ptr+sym], 2)
                    else:
                        tmp = c[ptr:ptr+sym]
                        tmp = tmp.replace('1', 'x')
                        tmp = tmp.replace('0', '1')
                        tmp = tmp.replace('x', '0')
                        value = -int(tmp, 2)

                    ptr += sym

                if i == 0:
                    dc_y.append(value)
                elif i == 1:
                    dc_cb.append(value)
                elif i == 2:
                    dc_cr.append(value)

                
                # AC
                ac = []
                while True:
                    
                    ptr_add = 1
                    while c[ptr:ptr + ptr_add] not in ac_hts[ac_table].keys():
                        ptr_add += 1
                        if ptr_add > 16:
                            raise ValueError(f'ptr_add > 16')
                    sym = ac_hts[ac_table][c[ptr:ptr + ptr_add]]

                    ptr += ptr_add
                    run, size = sym >> 4, sym % 16

                    if run == 0 and size == 0:
                        ac += [0] * (63 - len(ac))
                        break
                    elif run == 15 and size == 0:
                        ac += [0] * 16
                    else:
                        ac += [0] * run # add `run` zeros
                        if c[ptr] == '1':
                            value = int(c[ptr:ptr+size], 2)
                        else:
                            tmp = c[ptr:ptr+size]
                            tmp = tmp.replace('1', 'x')
                            tmp = tmp.replace('0', '1')
                            tmp = tmp.replace('x', '0')
                            value = -int(tmp, 2)                    
                        ac.append(value)
                        ptr += size
                    if len(ac) >= 63:
                        break

                if i == 0:
                    ac_ys.append(ac)
                elif i == 1:
                    ac_cbs.append(ac)
                elif i == 2:
                    ac_crs.append(ac)

    return build_matrix(dc_y, ac_ys, dc_cb, ac_cbs, dc_cr, ac_crs)

def decoder(args):

    # define markers
    markers = {
        0xffd8: "SOI",      # start of image segment
        0xffe0: "APP-0",    # JPEG/JFIF image segment
        0xfffe: "COM",      # comment segment
        0xffdb: "DQT",      # define quantization table segment
        0xffc0: "SOF-0",    # start of frame-0
        0xffc4: "DHT",      # define huffman table segment
        0xffda: "SOS",      # start of scan segment
        0xffd9: "EOI"       # end of image segment
    }

    # read image
    fn = args.input_file
    f = open(fn, 'rb')
    data = f.read()

    # parse
    ptr = 0
    qts = {}
    dc_hts = {}
    ac_hts = {}
    while True:

        (marker, ) = unpack(">H", data[ptr:ptr+2])
        ptr += 2

        if markers[marker]  == "SOI":
            print("start of image segment")
            pass

        elif markers[marker] == "APP-0":
            print("JPEG/JFIF image segment")
            (length, ) = unpack(">H", data[ptr:ptr+2])
            ptr += length

        elif markers[marker] == "COM":
            print("comment segment")
            (length, ) = unpack(">H", data[ptr:ptr+2])
            ptr += length

        elif markers[marker] == "DQT":
            print("define quantization table segment")
            (length, ) = unpack(">H", data[ptr:ptr+2])
            tqs, qt = get_qt(data[ptr:ptr+length])
            for i in range(len(tqs)):
                qts[tqs[i]] = qt[i]
            ptr += length

        elif markers[marker] == "SOF-0":
            print("start of frame-0")
            (length, ) = unpack(">H", data[ptr:ptr+2])
            sof_infos = get_img_info(data[ptr:ptr+length])
            ptr += length
        
        elif markers[marker] == "DHT":
            print("define huffman table segment")
            (length, ) = unpack(">H", data[ptr:ptr+2])
            infos, table = get_huffman_table(data[ptr:ptr+length])
            if infos[0] == "DC":
                dc_hts[infos[1]] = table
            else:
                ac_hts[infos[1]] = table
            ptr += length

        elif markers[marker] == "SOS":
            print("start of scan segment")
            (length, ) = unpack(">H", data[ptr:ptr+2])
            sos_infos = get_sos_infos(data[ptr:ptr+length])
            ptr += length
            y, cb, cr = decode_compressed_data(data[ptr:-2], sof_infos, sos_infos, dc_hts, ac_hts)
            tmp = len(data[ptr:]) - 2
            ptr += tmp

            # dequantization
            y, cb, cr = dequantization(y, cb, cr, sof_infos, qts)
            
            # IDCT
            y, cb, cr = idct_2d(y, cb, cr)

            # upsampling
            img = upsample(y, cb, cr, sof_infos)

            # color space transform
            img = ycbcr2rgb(img)

            h, w = sof_infos["height"], sof_infos["width"]
            img = img[:h, :w]
            
            image = Image.fromarray(np.uint8(img), mode="RGB")

            fn = args.output_file
            image.save(fn)

        elif markers[marker] == "EOI":
            print("end of image segment")
            break

    return img

def main():

    # get arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', "--input_file", type=str, help="path to the input image", required=True)
    parser.add_argument('-o', "--output_file", type=str, default='./output.bmp', help="path to the output image")
    args = parser.parse_args()

    start_time = time.time()
    decoder(args)
    end_time = time.time()
    print(f'time used: {end_time - start_time}s')


if __name__ == "__main__":
    main()