import numpy as np
from PIL import Image

def rgb_2_ycbcr(mcu):
    
    y = 0.299 * mcu[:, :, 0] + 0.587 * mcu[:, :, 1] + 0.114 * mcu[:, :, 2]
    cb = 128 - 0.168736 * mcu[:, :, 0] - 0.331264 * mcu[:, :, 1] + 0.5 * mcu[:, :, 2]
    cr = 128 + 0.5 * mcu[:, :, 0] - 0.418688 * mcu[:, :, 1] - 0.081312 * mcu[:, :, 2]
    return y, cb, cr

def ycbcr2rgb(img):

    rgb = np.zeros(img.shape)
    rgb[:, :, 0] = img[:, :, 0] + 1.402 * (img[:, :, 2] - 128)
    rgb[:, :, 1] = img[:, :, 0] - 0.344136 * (img[:, :, 1] - 128) - 0.714136 * (img[:, :, 2] - 128)
    rgb[:, :, 2] = img[:, :, 0] + 1.772 * (img[:, :, 1] - 128)
    rgb = np.clip(rgb, 0, 255)

    return np.uint8(rgb)