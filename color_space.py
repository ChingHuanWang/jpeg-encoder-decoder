import numpy as np

def rgd_2_ycbcr(mcu):
    
    return np.random.randint(0, 256, (16, 16)), np.random.randint(0, 256, (8, 8)), np.random.randint(0, 256, (8, 8))

def ycbcr2rgb(img):

    rgb = np.zeros(img.shape)
    rgb[:, :, 0] = img[:, :, 0] + 1.402 * (img[:, :, 2] - 128)
    rgb[:, :, 1] = img[:, :, 0] - 0.344136 * (img[:, :, 1] - 128) - 0.714136 * (img[:, :, 2] - 128)
    rgb[:, :, 2] = img[:, :, 0] + 1.772 * (img[:, :, 1] - 128)
    rgb = np.clip(rgb, 0, 255)

    return np.uint8(rgb)