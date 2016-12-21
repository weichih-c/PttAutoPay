#coding=utf-8
import telnetlib
import sys
import time

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
    readToPaying()

    print u"選擇給其他人P幣"
    telnet.write("0\r\n")
    time.sleep(1)

    print u"輸入Target ID : " + targetID
    telnet.write(targetID + '\r\n')
    time.sleep(1)

    print u"輸入金額 : {}".format(money)
    telnet.write("{}\r\n".format(money))
    time.sleep(1)

    content = telnet.read_very_eager().decode('big5','ignore')

    if u"請輸入您的密碼:" in content:
        print u'輸入驗證密碼'
        telnet.write(password + "\r\n")
        time.sleep(5)
        content = telnet.read_very_eager().decode('big5','ignore')

    if u"交易已完成，要修改紅包袋" in content:
        print u'選擇不修改紅包袋'
        telnet.write("n\r\n")
        time.sleep(3)
        content = telnet.read_very_eager().decode('big5','ignore')

    print "付款完成，回到首頁"
    telnet.write("\r\n")
    time.sleep(1)


        
def main():
    # get system arguments
    userID, password, targetID, money = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4]);

    telnetLogin(host, userID ,password)    

# ======================   Usage  ============================
#python PttAutoPay.py [帳號] [密碼] [對象] [稅前金額]
#python PttAutoPay.py account password target amountBeforeTax
# ============================================================

    payMoney(targetID, money, password);

    disconnect();
       

if __name__=="__main__" :
   main();