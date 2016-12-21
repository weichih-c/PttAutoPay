# PttAutoPay
PTT自動發錢機器人(Python) For Linux and Windows

# 參考來源：
https://github.com/twtrubiks/PttAutoPush

## 特色
* 可以自動對指定ID發錢
* 可選擇對單一對象或是指定清單內的所有對象

# 使用方法 （Usage）
```
$ python PttAutoPay.py [目標數量] [帳號] [密碼] [目標ID或檔案清單] [發錢金額]

單一對象(Single Target)
$ python PttAutoPay.py -s UserPttID Password TargetPttID MoneyAmount(beforeTax)

多個對象(Multiple Target)
$ python PttAutoPay.py -m UserPttID Password IDListFile MoneyAmount(beforeTax)

```

說明:

[目標數量] 
* -s 代表要給單一對象
* -m 代表要給多個清單

[帳號] : 要用來發錢的ptt帳號

[密碼] : 發錢帳號的密碼

[目標ID或檔案清單] : 
* 若[目標數量]填入-s，則此處必須填寫一名被發錢對象的pttID

* 若[目標數量]填入-m，則此處必須填寫電腦上一個指定的文字檔案，檔案內放有一連串的pttID

檔案內容格式如下
```
pttABC
123ptt
iamAnID
ThisIsAPttID

```
[發錢金額] : 輸入要發多少錢給每個目標ID

## Environment
* Python 2.7.3

