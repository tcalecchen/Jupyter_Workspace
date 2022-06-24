''' findKeyword.py  (更正版)
   keyword內容搜尋，子目錄下所有 doc docx txt
   neoCaffe 2021-09-11 '''

import os, sys, docx
from win32com import client

#--- 找出目錄下(包含子目錄)特定類型檔案
# 參數 nPath 資料夾 / fTypes 要搜尋的類型
# 傳回一個list : 符合的檔案 fullpathname
def getFiles(nPath, fTypes):
    matchedFiles = []  # 儲存符合的檔案
    f_tree = os.walk(nPath)
    
    for dirNa, sub, files in f_tree:
        #print(f'資料夾: {dirNa} 檔案數: {len(files)}')
        for f in files:
            ext = f.split('.')[-1]
            # 如果附加檔名 是 fTypes，則加入list中
            if ext in fTypes:
                matchedFiles.append(dirNa+'/'+f)
    return matchedFiles  # 傳回符合的檔案

#--- 找檔案內容，有無 keyword 之存在
# 參數 afile 檔名  keyword 要搜尋的字
# 傳回: found : key:找到的位置 / value:該行文字  
def findText(afile, keyword):
    found = dict()
    try:
        # 開啟文字檔的方式
        f = open(afile,'r',encoding='utf-8')
        # 讀取內容
        lines = f.readlines()
        f.close()
        n = 0
        # 逐行檢查
        for line in lines:
            n += 1
            if keyword in line:
                tmp = f'檔案: {afile} 第{n}行找到< {keyword} >'
                # dict 新增一筆 key:找到的位置 / value:該行文字
                found[tmp] = line
                #print(tmp,line)
    except:
        err = f'檔案: {afile} 讀取錯誤'
        found[0] = err
        
    return found     
#--------------------------

#--- 找檔案內容，有無 keyword 之存在
# 參數 afile 檔名  keyword 要搜尋的字
# 傳回: found : key:找到的位置 / value:該段落文字  
def findDoc(afile, keyword):
    found = dict()
    try:
        # 開啟舊版word檔的方式  .doc
        word = client.gencache.EnsureDispatch('Word.Application')
        word.Visible = 0
        word.DisplayAlerts = 0
        doc = word.Documents.Open(afile)
        paras = doc.Paragraphs
        n = 0 
        print(f'searching ... {afile}' )              
        for p in paras:
            n += 1  # 段落數
            # 如果該段落有此一keyword
            if keyword in p.Range.Text:
                tmp = f'檔案: {afile} 第{n}行找到< {keyword} >'
                # dict 新增一筆 key:找到的位置 / value:該行文字
                found[tmp] = p.Range.Text
        doc.Close()   # 關檔步驟，不可少         
    except:
        err = f'檔案: {afile} 讀取錯誤'
        found[0] = err
        
    return found     
#--------------------------
#--- 找檔案內容，有無 keyword 之存在
# 參數 afile 檔名  keyword 要搜尋的字
# 傳回: found : key:找到的位置 / value:該段落文字  
def findDocx(afile, keyword):
    found = dict()
    try:
        # 開啟word docx 的方式
        doc = docx.Document(afile)
        n = 0 
        print(f'searching ... {afile}' )              
        for para in doc.paragraphs:
            n += 1  # 段落數
            # 如果該段落有此一keyword
            if keyword in para.text:
                tmp = f'檔案: {afile} 第{n}行找到< {keyword} >'
                # dict 新增一筆 key:找到的位置 / value:該行文字
                found[tmp] = para.text
              
    except:
        err = f'檔案: {afile} 讀取錯誤'
        found[0] = err
        
    return found     


#--- 搜尋結果報告 
def resultRpt():
    print(f'文字檔數量: {len(mFiles)}')
    if len(allMatched) != 0:
        print(f'關鍵詞: < {tKey} > 出現次數: {len(allMatched)}\n出現位置:')
        for mkey, mvalue in allMatched.items():
            print(mkey,mvalue)
    else:
        print(f'找不到帶有關鍵詞 {tKey} 的檔案')
        
#--- 搜尋結果存檔  
def resultSave():
    
    resF = pathHere+'/Key_result.txt'
    if os.path.exists(resF):
        os.remove(resF)
        
    f = open(resF ,'w',encoding='utf-8' )
    print(f'文字檔數量: {len(mFiles)}' ,file=f)
    if len(allMatched) != 0:
        print(f'關鍵詞: < {tKey} > 出現次數: {len(allMatched)}\n出現位置:',file=f)
        m = 0
        for mkey, mvalue in allMatched.items():
            m += 1
            print(m,mvalue,file=f)
    else:
        print(f'找不到帶有關鍵詞 {tKey} 的檔案',file=f)
    f.close()
    
#--------------------------
#--- 流程 主軸 -----

# 1. 指定搜尋之目錄 (或者預設為當前目錄)
pathHere = os.getcwd() # 當前目錄位置
path = input('從哪個資料夾 開始搜尋 ? ') or pathHere
print(f'搜尋資料夾: {path} (含子目錄)')
tKey = input('keyword: ') or 'Python'

# 2. 選擇要篩選的檔案類型
tType = input('select file type: (1).doc  (2).docx  (3).txt') or 3

if tType not in ('1','2','3'):
    print('please enter 1  2  3')
    sys.exit()
if tType=='1':
    filetypes = ['doc']  
if tType=='2':
    filetypes = ['docx'] 
if tType=='3':
    filetypes = ['txt']
    
# 3. 取得檔案串列
mFiles = getFiles( path, filetypes )

if len(mFiles)!=0:
    # global dict 存放搜尋結果
    allMatched = dict()
    k = 0
    # 4. 逐一打開檔案，搜尋keyword
    for m in mFiles:
        k += 1    # 給編號
        # 找出 keyword
        if tType=='1':
            temp = findDoc(m,tKey)
        if tType=='2':
            temp = findDocx(m,tKey)
        if tType=='3':
            temp = findText(m,tKey)
            
        if len(temp) != 0:
            allMatched[k] = temp
    
    #print('allMatched ',len(allMatched))

# 5. report
resultRpt()
# 6. save result
resultSave()




