#coding=utf-8
import telnetlib
import sys
import time
import os

host = 'ptt.cc'


def telnetLogin(host, userID ,password) :
    global telnet
    telnet = telnetlib.Telnet(host) # telnet connection
    time.sleep(1)
    content = telnet.read_very_eager().decode('big5','ignore')
    if u"系統過載" in content :
        print u"系統過載, 請稍後再來"
        sys.exit(0)
        

    if u"請輸入代號" in content:
        print u"機器人輸入帳號中..."
        telnet.write(userID + "\r\n" )
        time.sleep(1)
        print u"機器人輸入密碼中..."
        telnet.write(password + "\r\n")
        time.sleep(1)
        content = telnet.read_very_eager().decode('big5','ignore')
        if u"密碼不對" in content:
           print u"密碼不對或無此帳號。程式結束"
           sys.exit()
           content = telnet.read_very_eager().decode('big5','ignore')
        if u"您想刪除其他重複登入" in content:
           print u'刪除其他重複登入的連線....'
           telnet.write("y\r\n")
           time.sleep(8)
           content = telnet.read_very_eager().decode('big5','ignore')
        if u"請按任意鍵繼續" in content:
           print u"資訊頁面，按任意鍵繼續..."
           telnet.write("\r\n" )
           time.sleep(2)
           content = telnet.read_very_eager().decode('big5','ignore')
        if u"您要刪除以上錯誤嘗試" in content:
           print u"刪除以上錯誤嘗試..."
           telnet.write("y\r\n")
           time.sleep(2)
           content = telnet.read_very_eager().decode('big5','ignore')
        if u"您有一篇文章尚未完成" in content:
           print u'刪除尚未完成的文章....'
           # 放棄尚未編輯完的文章
           telnet.write("q\r\n")   
           time.sleep(2)   
           content = telnet.read_very_eager().decode('big5','ignore')
        print "----------------------------------------------"
        print u"------------------ 登入完成 ------------------"
        print "----------------------------------------------"
        
    else:
        print u"沒有可輸入帳號的欄位，網站可能掛了"

def disconnect() :
    print u"機器人登出中..."
    # q = 上一頁，直到回到首頁為止，g = 離開，再見
    telnet.write("qqqqqqqqqg\r\ny\r\n" )
    time.sleep(3)
    #content = telnet.read_very_eager().decode('big5','ignore')
    #print content
    print "----------------------------------------------"
    print u"------------------ 登出完成 ------------------"
    print "----------------------------------------------"
    telnet.close()


def readToPaying():
    telnet.write('\r\n');
    time.sleep(1)      
    print u"進入首頁"                          
    telnet.write("q") ;   
    time.sleep(1)

    print u"進入娛樂與休閒"
    telnet.write("P\r\n")
    time.sleep(1)

    print u"進入PTT量販店"
    telnet.write("P\r\n")
    time.sleep(1)



def payMoney(targetID, money, password) :
    

    print u"選擇給其他人P幣"
    telnet.write("0\r\n")
    time.sleep(1)

    print u"輸入Target ID : " + targetID
    telnet.write(targetID + '\r\n')
    # time.sleep(1)

    print u"輸入金額 : {}".format(money)
    telnet.write("{}\r\n".format(money))
    time.sleep(1)

    content = telnet.read_very_eager().decode('big5','ignore')

    if u"確定進行交易嗎？ (y/N):" in content:
        print u'認證尚未過期，可以直接進行交易'
        telnet.write("y\r\n")
        time.sleep(3)
        content = telnet.read_very_eager().decode('big5','ignore')


    if u"請輸入您的密碼:" in content:
        print u'防惡意驗證，需輸入密碼進行驗證'
        telnet.write(password + "\r\n")
        time.sleep(3)
        content = telnet.read_very_eager().decode('big5','ignore')

    if u"交易已完成，要修改紅包袋" in content:
        print u'選擇不修改紅包袋內容'
        telnet.write("n\r\n")
        time.sleep(2)
        content = telnet.read_very_eager().decode('big5','ignore')


    print u"付款完成，回到量販店"

    telnet.write("\r\n")
    time.sleep(1)

def multiTarget(listFile, money, password):
    f = open(os.path.join("", listFile), 'r')
    for entry in f:
       payMoney(entry, money, password)

    f.close()

        
def main():
    if len(sys.argv) != 6:
      print "============ Usage ============"
      print u"Single   Target: python PttAutoPay.py -s [帳號] [密碼] [對象] [稅前金額]"
      print u"Multiple Target: python PttAutoPay.py -m [帳號] [密碼] [對象清單] [稅前金額]"
      print "==============================="
      print "python PttAutoPay.py -s|-m  userID password  targetID|targetList moneyBeforeTax"
      print "===============================\n"
      sys.exit()

    else:
      # get system arguments as variables
      type, userID, password, targetID, money = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]);

      # 進行付款
      if type == '-s':
        print "發錢--選擇單人模式"
        telnetLogin(host, userID ,password)   # 登入
        readToPaying() # 進入到ptt量販店
        payMoney(targetID, money, password);
        disconnect(); # 登出帳號

      elif type == '-m':
        print "發錢--選擇多人模式"
        telnetLogin(host, userID ,password)   # 登入
        readToPaying() # 進入到ptt量販店
        multiTarget(targetID, money, password);
        disconnect(); # 登出帳號

      else:
        print "請選擇發錢模式  單人 -s || 多人 -m\n"
        print "============ Usage ============"
        print u"Single   Target: python PttAutoPay.py -s [帳號] [密碼] [對象] [稅前金額]"
        print u"Multiple Target: python PttAutoPay.py -m [帳號] [密碼] [對象清單] [稅前金額]"
        print "==============================="
        print "python PttAutoPay.py -s|-m  userID password  targetID|targetList moneyBeforeTax"
        print "===============================\n"
        sys.exit()
       

if __name__=="__main__" :
   main();