import math

from decoder import get_huffman_table
from dc_huffman_table import lum_dc_huffman_table, chrom_dc_huffman_table
from ac_huffman_table import lum_ac_huffman_table, chrom_ac_huffman_table
from utils import img_2_dc_ac, block_2_zigzag, dec2bin
from quant import load_quantization_mat

class JpegEncoder:
    
    def __init__(self):
        self.gen_lum_dc = lum_dc_huffman_table
        self.gen_chrom_dc = chrom_dc_huffman_table
        self.gen_lum_ac = lum_ac_huffman_table
        self.gen_chrom_ac = chrom_ac_huffman_table
        self.img_2_dc_ac = img_2_dc_ac
        
    def img_2_huffman_code(self, img):
        
        dc, ac = self.img_2_dc_ac(img)
        
        # print(f'lum_dc')
        self.lum_dc_table = self.gen_lum_dc(dc)

        
        dht_data = [0]
        huffman_table = sorted(self.lum_dc_table.items(), key=lambda x: len(x[1]))
        count = [0] * 16
        symbols = []
        for sym, code in huffman_table:
            count[len(code) - 1] += 1
            symbols += [int(sym)]
        dht_data += count + symbols
        length = 2 + len(dht_data)
        dht_data = [length >> 8, length & 0xFF] + dht_data
        dht_data = np.array(dht_data, dtype=np.uint8).tobytes()
        dht_data = b'\x00\x1b\x00\x00\x03\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03\x04\x05\x06\x07'

        _, table = get_huffman_table(dht_data)
        table = {str(y): x for x, y in table.items()}
        self.lum_dc_table = table
        # print(f'self.lum_dc_table = {self.lum_dc_table}')
        # input()
        # for row in self.lum_dc_table:
        #     print(row)

        # print(f'lum_ac')
        self.lum_ac_table = self.gen_lum_ac(ac)


        dht_data = [16]
        huffman_table = sorted(self.lum_ac_table.items(), key=lambda x: len(x[1]))
        count = [0] * 16
        symbols = []
        for sym, code in huffman_table:
            count[len(code) - 1] += 1
            symbols += [int(sym[0], 16) * 16 + int(sym[-1], 16)]
        dht_data += count + symbols
        length = len(dht_data) + 2
        dht_data = [length >> 8, length & 0xFF] + dht_data
        dht_data = np.array(dht_data, dtype=np.uint8).tobytes()
        with open('./ac_0.txt', 'rb') as f:
            dht_data = b'\x003\x10\x00\x02\x01\x03\x01\x06\x04\x05\x04\x01\x05\x00\x00\x00\x00\x00\x00\x01\x02\x03\x11!1\x04\x12AQaq\x05"\x81\xf0\x91\xa1\xb1\xc1\xd1\x13#2\xe1\x82\x06\x143b\xc2'
        _, table = get_huffman_table(dht_data)
        table = {y: x for x, y in table.items()}
        self.lum_ac_table = table




        # print(f'self.lum_ac_table = {self.lum_ac_table}')
        # input()
        # for row in self.lum_ac_table:
        #     print(row)
        
        # print(f'chrom_dc')
        self.chrom_dc_table = self.gen_chrom_dc(dc)
        dht_data = [1]
        huffman_table = sorted(self.chrom_dc_table.items(), key=lambda x: len(x[1]))
        count = [0] * 16
        symbols = []
        for sym, code in huffman_table:
            count[len(code) - 1] += 1
            symbols += [int(sym)]
        dht_data += count + symbols
        length = 2 + len(dht_data)
        dht_data = [length >> 8, length & 0xFF] + dht_data
        dht_data = np.array(dht_data, dtype=np.uint8).tobytes()
        dht_data = b'\x00\x17\x01\x01\x01\x01\x01\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01\x02\x03'

        _, table = get_huffman_table(dht_data)
        table = {str(y): x for x, y in table.items()}
        self.chrom_dc_table = table
        # print(f'self.chrom_dc_table = {self.chrom_dc_table}')
        # input()
        # for row in self.chrom_dc_table:
        #     print(row)

        # print(f'chrom_ac')
        self.chrom_ac_table = self.gen_chrom_ac(ac)

        dht_data = [17]
        huffman_table = sorted(self.chrom_ac_table.items(), key=lambda x: len(x[1]))
        count = [0] * 16
        symbols = []
        for sym, code in huffman_table:
            count[len(code) - 1] += 1
            symbols += [int(sym[0], 16) * 16 + int(sym[-1], 16)]
        dht_data += count + symbols
        length = len(dht_data) + 2
        dht_data = [length >> 8, length & 0xFF] + dht_data
        dht_data = np.array(dht_data, dtype=np.uint8).tobytes()
        with open('./ac_1.txt', 'rb') as f:
            dht_data = b'\x00\x1f\x11\x01\x01\x01\x01\x00\x02\x02\x03\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x11\x02!1\x03\x12"Aqa'
        _, table = get_huffman_table(dht_data)
        table = {y: x for x, y in table.items()}
        self.chrom_ac_table = table

        # print(f'self.chrom_ac_table = {self.chrom_ac_table}')
        # input()
        # for row in self.chrom_ac_table:
        #     print(row)
        dc_y = dc[:, :4]
        dc_y = dc_y.flatten()
        first = dc_y[0]
        dc_y = np.insert(np.diff(dc_y), 0, first)
        dc_y = dc_y.reshape((len(dc_y) // 4, 4))
        dc[:, :4] = dc_y

        dc_cb = dc[:, 4]
        first = dc_cb[0]
        dc_cb = np.insert(np.diff(dc_cb), 0, first)
        dc[:, 4] = dc_cb

        dc_cr = dc[:, 5]
        first = dc_cr[0]
        dc_cr = np.insert(np.diff(dc_cr), 0, first)
        dc[:, 5] = dc_cr

        # dc: (209, 6), ac: (209, 378)
        # dc: 0 ~ 1253, ac: ac[i * 63:(i + 1) * 63]
        dc = dc.flatten()
        ac = ac.flatten()

        run_times = len(dc) # 1253
        bitstreams = ''
        for i in range(run_times):
            # Y
            if i % 6 < 4:
                # DC
                # print(f'lum_dc_table = {self.lum_dc_table}')
                dc_y = int(dc[i])
                if dc_y == 0:
                    category = 0
                    bitstreams += self.lum_dc_table['0']
                    print(f'category = {category}, codeword = {self.lum_dc_table["0"]}')
                else:
                    print(f'dc_y = {dc_y}')
                    category = str(len(dec2bin(abs(dc_y))))
                    print(f'category = {category}, codeword = {self.lum_dc_table[category]}')
                    bitstreams += self.lum_dc_table[category]
                    if dc_y > 0:
                        bitstreams += dec2bin(dc_y)
                    else:
                        tmp = dec2bin(-dc_y)
                        tmp = tmp.replace('1', 'x')
                        tmp = tmp.replace('0', '1')
                        tmp = tmp.replace('x', '0')
                        bitstreams += tmp
                
                print(f'bitstreams = {bitstreams}')
                input()

                # AC
                # print(f'lum_ac_table = {self.lum_ac_table}')
                ac_ys = ac[i * 63:(i + 1) * 63]
                print(ac_ys)

                # find last nonzero element
                nonzero_inds = np.argwhere(ac_ys != 0).flatten()
                if len(nonzero_inds) == 0:
                    bitstreams += self.lum_ac_table[0]
                    continue
                last_nonzero_ind = nonzero_inds[-1]
                    
                run = 0
                for i in range(last_nonzero_ind + 1):
                    ac_y = int(ac_ys[i])
                    print(f'ac_y = {ac_y}')
                    if ac_y > 0:
                        size = len(dec2bin(ac_y))
                        print(f'run = {run}, size = {size}')
                        # sym = f'{hex(run).upper()[2:]}/{hex(size).upper()[2:]}'
                        sym = run * 16 + size
                        codeword = self.lum_ac_table[sym]
                        print(f'sym = {sym}, codeword = {codeword}')
                        bitstreams += self.lum_ac_table[sym]
                        bitstreams += dec2bin(ac_y)
                        run = 0
                    elif ac_y < 0:
                        size = len(dec2bin(-ac_y))
                        print(f'run = {run}, size = {size}')
                        # sym = f'{hex(run).upper()[2:]}/{hex(size).upper()[2:]}'
                        sym = run * 16 + size
                        codeword = self.lum_ac_table[sym]
                        print(f'sym = {sym}, codeword = {codeword}')
                        bitstreams += self.lum_ac_table[sym]
                        
                        tmp = dec2bin(-ac_y)
                        tmp = tmp.replace('1', 'x')
                        tmp = tmp.replace('0', '1')
                        tmp = tmp.replace('x', '0')
                        bitstreams += tmp
                        run = 0
                    else:
                        if run == 15:
                            bitstreams += self.lum_ac_table[240]
                            run = 0
                        else:
                            run += 1
                    print(f'bitstreams = {bitstreams}')
                    input()
                if last_nonzero_ind != 62:
                    bitstreams += self.lum_ac_table[0]
                
            # Cb & Cr
            else:
                # print(f'chrom_dc_table = {self.chrom_dc_table}')
                dc_c = int(dc[i])
                if dc_c == 0:
                    category = 0
                    # print(f'category = {category}')
                    bitstreams += self.chrom_dc_table['0']
                else:
                    # print(f'dc_c = {dc_c}')
                    category = str(len(dec2bin(abs(dc_c))))
                    # print(f'category = {category}')
                    # print(f'codeword = {self.chrom_dc_table[category]}')
                    bitstreams += self.chrom_dc_table[category]
                    if dc_c > 0:
                        bitstreams += dec2bin(dc_c)
                    else:
                        tmp = dec2bin(-dc_c)
                        tmp = tmp.replace('1', 'x')
                        tmp = tmp.replace('0', '1')
                        tmp = tmp.replace('x', '0')
                        bitstreams += tmp
                
                # print(f'bitstreams = {bitstreams}')
                # input()

                # AC
                # print(f'lum_ac_table = {self.chrom_ac_table}')
                ac_cs = ac[i * 63:(i + 1) * 63]
                # print(ac_cs)

                # find last nonzero element
                nonzero_inds = np.argwhere(ac_cs != 0).flatten()
                if len(nonzero_inds) == 0:
                    bitstreams += self.chrom_ac_table[0]
                    continue
                last_nonzero_ind = nonzero_inds[-1]
                
                run = 0
                for i in range(last_nonzero_ind + 1):
                    ac_c = int(ac_cs[i])
                    if ac_c > 0:
                        size = len(dec2bin(ac_c))
                        # print(f'run = {run}, size = {size}')
                        # sym = f'{hex(run).upper()[2:]}/{hex(size).upper()[2:]}'
                        sym = run * 16 + size
                        codeword = self.chrom_ac_table[sym]
                        # print(f'sym = {sym}, codeword = {codeword}')
                        bitstreams += codeword
                        
                        bitstreams += dec2bin(ac_c)
                        run = 0
                    elif ac_c < 0:
                        size = len(dec2bin(-ac_c))
                        # print(f'run = {run}, size = {size}')
                        # sym = f'{hex(run).upper()[2:]}/{hex(size).upper()[2:]}'
                        sym = run * 16 + size
                        codeword = self.chrom_ac_table[sym]
                        # print(f'sym = {sym}, codeword = {codeword}')
                        bitstreams += codeword
                        
                        tmp = dec2bin(-ac_c)
                        tmp = tmp.replace('1', 'x')
                        tmp = tmp.replace('0', '1')
                        tmp = tmp.replace('x', '0')
                        bitstreams += tmp
                        run = 0
                    else:
                        if run == 15:
                            bitstreams += self.chrom_ac_table[240]
                            run = 0
                        else:
                            run += 1
                    # print(f'bitstreams = {bitstreams}')
                    # input()
                if last_nonzero_ind != 62:
                    bitstreams += self.chrom_ac_table[0]
        
        print(self.lum_dc_table)
        print(self.lum_ac_table)
        print(self.chrom_dc_table)
        print(self.chrom_ac_table)
        input()

        return (self.lum_dc_table, self.lum_ac_table, self.chrom_dc_table, self.chrom_ac_table), bitstreams
    
    def write_to_jpeg(self, img):
        
        # padding
        h, w, _ = img.shape
        mcu_h, mcu_w = math.ceil(h / 16), math.ceil(w / 16)
        tmp = np.zeros((mcu_h * 16, mcu_w * 16, 3))
        tmp[:h, :w, :] = img
        img = tmp

        # define markers
        markers = {
            "SOI": b'\xff\xd8',      # start of image segment
            "APP-0": b'\xff\xe0',    # JPEG/JFIF image segment
            "COM": b'\xff\xfe',      # comment segment
            "DQT": b'\xff\xdb',      # define quantization table segment
            "SOF-0": b'\xff\xc0',    # start of frame-0
            "DHT": b'\xff\xc4',      # define huffman table segment
            "SOS": b'\xff\xda',      # start of scan segment
            "EOI": b'\xff\xd9'       # end of image segment
        }

        # SOI
        data = [num for num in markers["SOI"]]
        
        # APP-0
        data += [num for num in markers["APP-0"]]
        app0_data = b'\x00\x10JFIF\x00\x01\x01\x00\x00\x01\x00\x01\x00\x00'
        data += [num for num in app0_data]

        # COM
        # no comment

        # DQT
        data += [num for num in markers["DQT"]]

        types = ["lum", "chrom"]
        dqt_data = []
        for i, t in enumerate(types):
            dqt_data += [i]
            qt = block_2_zigzag(load_quantization_mat(t)).tolist()
            dqt_data += [int(num) for num in qt]
        length = len(dqt_data) + 2

        data += [length >> 8, length & 0xFF] + dqt_data

        # SOF-0
        data += [num for num in markers["SOF-0"]]
        
        precision = 8
        height = h
        width = w
        # height, width = mcu_h * 16, mcu_w * 16
        n_components = 3
        sampling_factor = [[2, 2], [1, 1], [1, 1]]
        qt_table_nums = [0, 1, 1]
        sof0_data = [precision, height >> 8, height & 0xFF, width >> 8, width & 0xFF, n_components]

        for i in range(n_components):
            sof0_data += [i + 1]
            horizontal_factor, vertical_factor = sampling_factor[i]
            qt_table_num = qt_table_nums[i]
            sof0_data += [horizontal_factor * 16 + vertical_factor]
            sof0_data += [qt_table_num]

        length = len(sof0_data) + 2
        data += [length >> 8, length & 0xFF] + sof0_data

        # DHT: DC, 0
        dhts, bitstream = self.img_2_huffman_code(img)
        print(f'dhts[0] = {dhts[0]}')
        input()

        data += [num for num in markers["DHT"]]
        print(data)
        input()
        dht_data = [0]
        huffman_table = sorted(dhts[0].items(), key=lambda x: len(x[1]))
        print(f'huffman_table = {huffman_table}')
        count = [0] * 16
        symbols = []
        for sym, code in huffman_table:
            count[len(code) - 1] += 1
            symbols += [int(sym)]

        dht_data += count + symbols
        print(f'count = {count}, symbols = {symbols}')
        print(f'dht_data = {dht_data}')
        length = 2 + len(dht_data)
        print(f'length = {[length >> 8, length & 0xFF]}')
        data += [length >> 8, length & 0xFF] + dht_data
        print(data)
        input()

        # DHT: AC, 0
        data += [num for num in markers["DHT"]]
        dht_data = [16]

        huffman_table = sorted(dhts[1].items(), key=lambda x: len(x[1]))
        count = [0] * 16
        symbols = []
        for sym, code in huffman_table:
            count[len(code) - 1] += 1
            symbols += [sym]

        dht_data += count + symbols

        length = len(dht_data) + 2
        data += [length >> 8, length & 0xFF] + dht_data

        # DHT: DC, 1
        data += [num for num in markers["DHT"]]
        dht_data = [1]

        huffman_table = sorted(dhts[2].items(), key=lambda x: len(x[1]))
        count = [0] * 16
        symbols = []
        for sym, code in huffman_table:
            count[len(code) - 1] += 1
            symbols += [int(sym)]

        dht_data += count + symbols

        length = len(dht_data) + 2
        data += [length >> 8, length & 0xFF] + dht_data

        # DHT: AC, 1
        data += [num for num in markers["DHT"]]
        dht_data = [17]

        huffman_table = sorted(dhts[3].items(), key=lambda x: len(x[1]))
        count = [0] * 16
        symbols = []
        for sym, code in huffman_table:
            count[len(code) - 1] += 1
            symbols += [sym]

        dht_data += count + symbols

        length = len(dht_data) + 2
        data += [length >> 8, length & 0xFF] + dht_data

        # SOS
        data += [num for num in markers["SOS"]]
            # component
        n_components = 3
        sos_data = [n_components]

            # component data
        huffman_tables = [[0, 0], [1, 1], [1, 1]]
        for i in range(n_components):
            j, k = huffman_tables[i]
            sos_data += [i + 1, j * 16 + k]

            # bytes to skip
        sos_data += [0, 63, 0]
        length = len(sos_data) + 2
        data += [length >> 8, length & 0xFF] + sos_data

        # compressed data
        times = math.ceil(len(bitstream) / 8)
        bitstream += '0' * (times * 8 - len(bitstream))
        data += [int(bitstream[i * 8:(i + 1) * 8], 2) for i in range(times)]

        # EOI
        data += [num for num in markers["EOI"]]

        data = np.array(data, dtype=np.uint8)
        
        print(f'data: {data.tobytes()}')
        with open('./output.jpg', 'wb') as f:
            f.write(data.tobytes())
        
        
if __name__ == "__main__":
    from PIL import Image
    import numpy as np
    img = Image.open('./test.jpg')
    img = np.array(img, dtype=np.uint8)
    encoder = JpegEncoder()
    bitstream = encoder.write_to_jpeg(img)