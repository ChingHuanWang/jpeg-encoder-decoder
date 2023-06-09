
from dc_huffman_table import lum_dc_huffman_table, chrom_dc_huffman_table
from ac_huffman_table import lum_ac_huffman_table, chrom_ac_huffman_table
from utils import img_2_dc_ac

class JpegEncoder:
    
    def __init__(self):
        self.gen_lum_dc = lum_dc_huffman_table
        self.gen_chrom_dc = chrom_dc_huffman_table
        self.gen_lum_ac = lum_ac_huffman_table
        self.gen_chrom_ac = chrom_ac_huffman_table
        self.img_2_dc_ac = img_2_dc_ac
        
    def img_2_huffman_code(self, img):
        dc, ac = self.img_2_dc_ac(img)
        self.lum_dc_table = self.gen_lum_dc(dc)
        self.lum_ac_table = self.gen_lum_ac(ac)
        
        self.chrom_dc_table = self.gen_chrom_dc(dc)
        self.chrom_ac_table = self.gen_chrom_ac(ac)
        
        
    
    def write_to_jpeg():
        pass
        
        
        