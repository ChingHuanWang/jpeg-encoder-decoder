import math
import numpy as np

def downsample(y, cb, cr):
    new_w, new_h = int(cb.shape[0]/2), int(cb.shape[1]/2)
    cb_prime = np.zeros((new_h, new_w))
    cr_prime = np.zeros((new_h, new_w))
    mcu_h, mcu_w = cb.shape
    k_w = 2
    k_h = 2
    for i in range(0, mcu_h, k_h):
        for j in range(0, mcu_w, k_w):
            cb_prime[int(i/k_h)][int(j/k_w)] = np.average(cb[i:i+k_h, j:j+k_w])
            cr_prime[int(i/k_h)][int(j/k_w)] = np.average(cr[i:i+k_h, j:j+k_w])
            
    return y, cb_prime, cr_prime
    
def upsample(y, cb, cr, sof_infos):

    sampling_factor = sof_infos["sampling_factor"]
    n_components = sof_infos["n_components"]
    w, h = sof_infos["width"], sof_infos["height"]

    mcu_width, mcu_height = np.array(max(sampling_factor)) * 8
    w, h = math.ceil(w / mcu_width) * mcu_width, math.ceil(h / mcu_height) * mcu_height
    
    for ind, (i, j) in enumerate(sampling_factor):
        if ind == 0:
            num, _, _ = y.shape
            re_y = np.zeros((num // (i * j), i * 8, j * 8))
            for a in range(i):
                for b in range(j):
                    re_y[:, a * 8:(a + 1) * 8, b * 8:(b + 1) * 8] = y[a * j + b::(i * j), :, :]
        elif ind == 1:
            num, _, _ = cb.shape
            re_cb = np.zeros((num // (i * j), i * 8, j * 8))
            for a in range(i):
                for b in range(j):
                    re_cb[:, a * 8:(a + 1) * 8, b * 8:(b + 1) * 8] = cb[a * j + b::(i * j), :, :]
        elif ind == 2:
            num, _, _ = cb.shape
            re_cr = np.zeros((num // (i * j), i * 8, j * 8))
            for a in range(i):
                for b in range(j):
                    re_cr[:, a * 8:(a + 1) * 8, b * 8:(b + 1) * 8] = cr[a * j + b::(i * j), :, :]

    a, b = sampling_factor[0]
    re_cb = np.repeat(np.repeat(re_cb, b, axis=1), a, axis=2)
    re_cr = np.repeat(np.repeat(re_cr, b, axis=1), a, axis=2)

    img = np.zeros((h, w, 3))
    for i in range(h // mcu_height):
        for j in range(w // mcu_width):
            img[i * mcu_height:(i + 1) * mcu_height, j * mcu_width:(j + 1) * mcu_width, 0] = re_y[i * (w // mcu_width) + j]
            img[i * mcu_height:(i + 1) * mcu_height, j * mcu_width:(j + 1) * mcu_width, 1] = re_cb[i * (w // mcu_width) + j]
            img[i * mcu_height:(i + 1) * mcu_height, j * mcu_width:(j + 1) * mcu_width, 2] = re_cr[i * (w // mcu_width) + j]
    
    return img