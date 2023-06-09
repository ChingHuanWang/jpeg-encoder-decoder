def dequantization(y, cb, cr, sof_infos, qts):

    n_quant = sof_infos["quantization_table"]
    y = qts[n_quant[0]] * y
    cb = qts[n_quant[1]] * cb
    cr = qts[n_quant[2]] * cr
    
    return y, cb, cr