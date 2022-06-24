#coding=utf-8
import os
import json
#獲取目標資料夾的路徑
filedir = r'J:\NumberData\mrcnnHik\test'
#獲取資料夾中的檔名稱列表
filenames=os.listdir(filedir)
#遍歷檔名
for filename in filenames:
  filepath = filedir+'/'+filename
  # print(filepath)
  after = []
  # 開啟檔案取出資料並修改，然後存入變數
  with open(filepath,'r') as f:
    data = json.load(f)
    mask=data["MaskPolygonItem"]
    for zidian in mask:
      print(type(zidian))
      mask[zidian]["polygon"] = '354 221,355 310,729 318,733 236'
    after = data
  # 開啟檔案並覆蓋寫入修改後內容
  with open(filepath,'w') as f:
    #結構化輸出
    data = json.dump(after,f,sort_keys=True,indent=4,separators=(',',': '))
