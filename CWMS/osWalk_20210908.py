''' osWalf_20210908.py 篩選某類型檔案
 Author: neoCaffe  '''
from os.path import join
import os, fnmatch

#--- 尋找某目錄(包括子目錄)下全部檔案
#--- 傳入參數 nPath目錄名稱 / txtFile 將結果存檔 
#--- 傳回一個 list fList 全部的檔案名稱 
def findAll( nPath,txtFile ):
    ''' os.walk 遞迴找出所有檔案
    fTree 傳回一個tuple，包含三元素
      dirs     該層的 path
      subdirs  該層的 目錄s
      files    該層的 檔案s
    topdown = True 從上向下找 '''
    fTree = os.walk( nPath, topdown=True )
    dList = []  # 某檔案的 path
    sList = []  # 該檔案同一層的 目錄
    fList = []  # 該檔案的fullPathName 
    
    # 逐層從上向下
    for dirs, subdirs, files in fTree:
        for f in files: 
            # 添加入 list
            dList.append(dirs)
            sList.append(subdirs)
            # dirs+f 組合成 檔案的fullpathname 
            fullpath = join(dirs,f)
            fList.append(fullpath)
    '''       
    # 此時的 dirs, subdirs,files 只是最後一個folder的搜尋結果
    # 並不是全部檔案的 path，可將他們印出來看看
      print(f'len(dirs): {len(dirs)}')
      print(f'len(subdirs): {len(subdirs)}')
      print(f'len(files): {len(files)}')
    '''

    # 檢視成果        
    print(f'dir count目錄數量 : {len(dList)}')
    print(f'sList count: {len(sList)}')
    print(f'file count : {len(fList)}')

    # 印出來看看
    for f in range(len(fList)):
        print(dList[f],sList[f],fList[f])

    # 把結果存檔，以供驗證
    txt = open(txtFile,'w',encoding='utf-8') 
    for f in range(len(fList)):
        print(f'{dList[f]}  {sList[f]} {fList[f]}',file=txt)
    txt.close()
    
    return fList  # 傳回這個list

#-----------------------
#--- 找某些類型的檔案
#--- 傳入參數 nPath目錄名稱 / fTypes檔案類型 / txtFile 將結果存檔 
#--- 傳回一個 list allFiles 符合的檔案名稱 
def findSome(nPath, fTypes, txtFile):
    allFiles = []
    for dirs, subdirs, files in os.walk( nPath ):
        for extension in ( tuple(fTypes) ):
            for filename in fnmatch.filter(files, extension):
                filepath = os.path.join(dirs, filename)		
                if os.path.isfile( filepath ):
                    allFiles.append(filepath)
                    print(filepath)
    
    # 把結果存檔，以供驗證
    f = open( txtFile,'w',encoding='utf-8' ) 
    for i in allFiles:
        print(f'{i}',file=f)
    f.close()
    
    return allFiles  # 傳回這個list
#------------------
#--- 流程 主軸 -----
pathHere = os.getcwd() # 當前目錄位置

# 指定搜尋之目錄 (或者預設為當前目錄)
path = input('從哪個資料夾 開始搜尋 ? ') or pathHere
print(f'搜尋資料夾: {path} (包含子目錄)所有檔案')
#--- call the function findAll()
txt1 = 'resultAll.txt'
retAll = findAll(path, txt1)
print(f'搜尋完成，全部檔案: {len(retAll)} 個')

#--- call the function findSome()
# 要篩選的檔案類型
filetypes = ['*.jpg', '*.png', '*.doc']  
txt2 = 'resultSome.txt'
print('os.walk + filter 使用fnmatch的寫法')
retSome = findSome(path, filetypes, txt2)
print(f'搜尋完成，符合的檔案: {len(retSome)} 個')