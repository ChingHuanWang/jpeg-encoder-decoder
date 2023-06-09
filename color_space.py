import numpy as np
from PIL import Image

def rgb_2_ycbcr(img):
    img = img.convert("YCbCr")
    return np.array(img)

def ycbcr2rgb(img):

    rgb = np.zeros(img.shape)
    rgb[:, :, 0] = img[:, :, 0] + 1.402 * (img[:, :, 2] - 128)
    rgb[:, :, 1] = img[:, :, 0] - 0.344136 * (img[:, :, 1] - 128) - 0.714136 * (img[:, :, 2] - 128)
    rgb[:, :, 2] = img[:, :, 0] + 1.772 * (img[:, :, 1] - 128)
    rgb = np.clip(rgb, 0, 255)

    return np.uint8(rgb)