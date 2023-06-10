# jpeg-encoder-decoder
## 簡介
在這次的final project，我們實作了python版本的baseline的jpeg的編碼器和解碼器。經過實驗比較，我們的mean square error為(?)，壓縮率為(?)，編碼和解碼的時間分別為(?)秒和(?)秒。除了baseline的壓縮算法，還有其他四種算法:
* 循序（sequential）
* 遞進（progressive）
* 層次（hierarchical）
* 無損（lossless）

但是礙於時間關係，我們只實作了baseline版本的算法

## jpeg 編碼器和解碼器架構圖
![](https://hackmd.io/_uploads/H1AdnXzPn.png)


## 檔案架構

- jpeg-encoder-decoder
    - huffman_table.py
    - dc_huffman_table.py
    - ac_huffman_table.py
    - dct.py
    - color_space.py
    - quant.py
    - utils.py
    - encoder.py
    - decoder.py

## 執行程式

編碼圖片
* python3 encoder.py -i <input_img_path> -o <output_img_path>

解碼圖片
* python3 decoder.py -i <input_img_path> -o <output_img_path>

這邊有三點要注意:
1. 若要測試解碼器的效果，input image只能放用baseline算法編碼的jpg檔案，編碼器的input image則無限制。
2. 當使用解碼器去解碼由編碼器所編碼的圖片時，output image的檔案格式記得使用bmp，以便好檢視解碼前後圖片的差距
3. 當執行解碼器，被解碼的圖片會直接顯示在螢幕上

## 實作細節
1. 我們沒有找到一份可靠的baseline霍夫曼編碼表，所以在這個repo我們都是吃進一張圖片建出屬於它的霍夫曼表用來編碼和解碼，所以程式的運行速度會較一般的jpeg編碼器和解碼器慢。
2. 在通信實驗lab3所實作的霍夫曼表無法適用在jpeg編碼，因為我們在檢視一般jpg檔案時發現用於編碼的霍夫曼表會依code word長短，由短至長依序讓symbol佔據霍夫曼樹的leaf node。
3. 在jpeg的檔案規範中\xff被視為特殊符號，因此若在解碼過程中發現\xff則會立刻中止解碼，因此若在編碼圖片的過程中發現\xff，則須在後面加上\x00讓解碼器繼續往下解碼。




