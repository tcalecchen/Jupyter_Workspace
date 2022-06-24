''' fileOverlap.py 檔案重覆之處理 Author: neoCaffe 2021/9/9 '''
import os, hashlib

#--- 找出重覆之檔案 
# 參數 nPath 資料夾 / fTypes 要搜尋的類型
def findOverlap( nPath, fTypes ):
    allimage = []
    allhsh  = dict()   # key: hash / value: filePath
    overlapA = []      # 重覆之檔 位置A
    overlapB = []      # 重覆之檔 位置B
    f_tree = os.walk(nPath)
    # os.walk 傳回的是generator
    print(f'return a generator: {type(f_tree)}')
    
    for dirname,subdir,files in f_tree:
        # 一層一層向下
        print(f'file count of this folder: {len(files)}')
        imgFiles = []    # 這一層的 image files
        # 取得 符合之檔案，存入 imgFiles 串列中
        for file in files:  
            ext = file.split('.')[-1]
            if ext in filetypes:
                tmp = dirname +'/'+file
                imgFiles.append(tmp)
                allimage.append(tmp)
      
        # 如果這一層有符合檔案 
        if len(imgFiles) > 0:
            #--- 逐一檢查，如果發現新來之檔hash已存在，則加入overlap 
            for img in imgFiles:
                imghsh = hashlib.md5(open(img,'rb').read()).digest()
                fname = os.path.abspath(img)
                if imghsh in allhsh:
                    overlapA.append(fname)
                    overlapB.append(allhsh[imghsh]) #B位置放入已有hash值之檔
                else:  # else 增添入 hash dict 中
                    allhsh[imghsh] = fname

    return allimage, overlapA, overlapB

#--- 流程 主軸 -----
# 指定搜尋之目錄 (或者預設為當前目錄)
pathHere = os.getcwd() # 當前目錄位置
path = input('從哪個資料夾 開始搜尋 ? ') or pathHere
print(f'搜尋資料夾: {path} (含子目錄)圖檔')

# 要篩選的檔案類型
filetypes = ['jpg', 'png', 'bmp', 'jpeg']  
iFile, overA, overB = findOverlap( path, filetypes )

print(f'圖檔數量: {len(iFile)} 重覆者: {len(overA)}')

if len(overA) != 0:
    print("找到下列重覆的檔案：")
    for i in range(len(overA)):
        print(f'位置A: {overA[i]}\n位置B: {overB[i]}')
   
# 把結果存檔
f = open( pathHere+'\overlap.txt','w',encoding='utf-8' )
print(f'圖檔數量: {len(iFile)} 重覆者: {len(overA)}',file=f)
print("找到下列重覆的檔案：",file=f)
for i in range(len(overA)):
    print(f'位置A: {overA[i]}\n位置B: {overB[i]}\n',file=f)
f.close()
