import sys
import time
import PTTTelnetCrawlerLibrary
import PTTTelnetCrawlerLibraryErrorCode
import os.path
try:
    sys.path.append("../IDPassword")
    import IDPassword

    ID = IDPassword.ID
    Password = IDPassword.Password
except ModuleNotFoundError:
    #Define your id password here
    ID = 'Your ID'
    Password = 'Your Password'

KickOtherLogin = False

BoardList = ['Wanted', 'Gossiping', 'Test']
PostIDList = ['1PC1YXYj', '1PCBfel1', '1D89C0oV']

PTTCrawler = None

def PostDemo():
    #發文類別       1
    #簽名檔        	0
    for i in range(3):
        
        #ErrorCode = PTTCrawler.post('Test', '連續自動PO文測試 ' + str(i), '自動PO文測試\r\n\r\n使用PTT Telnet Crawler Library 測試\r\n\r\nhttps://goo.gl/qlDRCt', 1, 0)
        ErrorCode = PTTCrawler.post('Test', '連續自動PO文測試 ' + str(i), '自動PO文測試\r\n\r\n(羞', 1, 0)
        if ErrorCode == PTTTelnetCrawlerLibraryErrorCode.Success:
            PTTCrawler.Log('Post in Test success')
        else:
            PTTCrawler.Log('Post in Test fail')                

def GetNewestPostIndexDemo():

    for i in range(3):
        for Board in BoardList:
            ErrorCode, NewestIndex = PTTCrawler.getNewestPostIndex(Board)
            if ErrorCode == PTTTelnetCrawlerLibraryErrorCode.Success:
                PTTCrawler.Log(str(i) + ' Get ' + Board + ' get newest post index success: ' + str(NewestIndex))
            else:
                PTTCrawler.Log(str(i) + ' Get ' + Board + ' get newest post index fail')
                return False
            #time.sleep(1)

def GetPostInfoDemo():

    ErrorCode, NewestIndex = PTTCrawler.getNewestPostIndex('Gossiping')
    if ErrorCode != PTTTelnetCrawlerLibraryErrorCode.Success:
        PTTCrawler.Log('Get newest post index fail')
        return False
    TryPost = 3
    if NewestIndex == -1:
        PTTCrawler.Log('Get newest post index fail')
        return False
        
    for i in range(TryPost):
        
        ErrorCode, Post = PTTCrawler.getPostInfoByIndex('Gossiping', NewestIndex - i)
        if ErrorCode == PTTTelnetCrawlerLibraryErrorCode.PostDeleted:
            PTTCrawler.Log('Post has been deleted')
            continue
        if ErrorCode == PTTTelnetCrawlerLibraryErrorCode.WebFormatError:
            PTTCrawler.Log('Web structure error')
            continue
        if ErrorCode != PTTTelnetCrawlerLibraryErrorCode.Success:
            PTTCrawler.Log('Get post by index fail')
            return False
        PTTCrawler.Log(str(int(((i + 1) * 100) / TryPost)) + ' % ' + str(NewestIndex - i) + ' Title: ' + Post.getTitle())
        ErrorCode, Post = PTTCrawler.getPostInfoByID('Gossiping', Post.getPostID())
        if ErrorCode != PTTTelnetCrawlerLibraryErrorCode.Success:
            PTTCrawler.Log('Get post by ID fail error code: ' + str(ErrorCode))
            return False
        PTTCrawler.Log(str(int(((i + 1) * 100) / TryPost)) + ' % ' + Post.getPostID() + ' Title: ' + Post.getTitle())
        
def GetNewPostIndexListDemo():
    ErrorCode, NewestIndex = PTTCrawler.getNewestPostIndex('Wanted')
    if ErrorCode != PTTTelnetCrawlerLibraryErrorCode.Success:
        return False
    
    LastIndex = NewestIndex - 5
    for i in range(3):
        #Return new post list LastIndex ~ newest without LastIndex
        ErrorCode, LastIndexList = PTTCrawler.getNewPostIndexList('Wanted', LastIndex)
        if ErrorCode != PTTTelnetCrawlerLibraryErrorCode.Success:
            return False
        if not len(LastIndexList) == 0:
            for NewPostIndex in LastIndexList:
                PTTCrawler.Log('Detected new post: ' + str(NewPostIndex))
            LastIndex = LastIndexList.pop()
def PushDemo():
    ErrorCode, NewestIndex = PTTCrawler.getNewestPostIndex('Test')
    if ErrorCode != PTTTelnetCrawlerLibraryErrorCode.Success:
        PTTCrawler.Log('getNewestPostIndex ErrorCode: ' + str(ErrorCode))
        return False
    PTTCrawler.Log('NewestIndex: ' + str(NewestIndex))
    for i in range(3):
        ErrorCode = PTTCrawler.pushByIndex('Test', PTTCrawler.PushType_Push, 'https://goo.gl/qlDRCt by post index', NewestIndex)
        if ErrorCode == PTTTelnetCrawlerLibraryErrorCode.Success:
            PTTCrawler.Log('pushByIndex Push success')
        else:
            PTTCrawler.Log('pushByIndex Push fail')
    ErrorCode, NewPost = PTTCrawler.getPostInfoByIndex('Test', NewestIndex)
    if ErrorCode != PTTTelnetCrawlerLibraryErrorCode.Success:
        PTTCrawler.Log('getPostInfoByIndex ErrorCode: ' + str(ErrorCode))
        return False
    if NewPost == None:
        PTTCrawler.Log('getPostInfoByIndex fail')
        return False
    for i in range(3):
        
        ErrorCode = PTTCrawler.pushByID('Test', PTTCrawler.PushType_Push, 'https://goo.gl/qlDRCt by post id', NewPost.getPostID())
        if ErrorCode == PTTTelnetCrawlerLibraryErrorCode.Success:
            PTTCrawler.Log('pushByID Push success')
        else:
            PTTCrawler.Log('pushByID Push fail')
def MainDemo():
    #0 不加簽名檔
    for i in range(1):
        ErrorCode = PTTCrawler.mail(ID, '自動寄信測試標題', '自動測試 如有誤寄打擾 抱歉QQ', 0)
        if ErrorCode == PTTTelnetCrawlerLibraryErrorCode.Success:
            PTTCrawler.Log('Mail to ' + ID + ' success')
        else:
            PTTCrawler.Log('Mail to ' + ID + ' fail')
def GiveMoneyDemo():

    WhoAreUwantToGiveMoney = 'CodingMan'
    
    for i in range(3):
        ErrorCode = PTTCrawler.giveMoney(WhoAreUwantToGiveMoney, 2, Password)
        
        if ErrorCode == PTTTelnetCrawlerLibraryErrorCode.Success:
            PTTCrawler.Log('Give money to ' + WhoAreUwantToGiveMoney + ' success')
        else:
            PTTCrawler.Log('Give money to ' + WhoAreUwantToGiveMoney + ' fail')

def GetTimeDemo():

    for i in range(1):
        ErrorCode, Time = PTTCrawler.getTime()
        if ErrorCode != PTTTelnetCrawlerLibraryErrorCode.Success:
            PTTCrawler.Log('Get time error')
            return False
        PTTCrawler.Log('Ptt time: ' + Time + '!')
        time.sleep(1)
            
if __name__ == '__main__':
    print('Welcome to PTT Telnet Crawler Library Demo')

    PTTCrawler = PTTTelnetCrawlerLibrary.PTTTelnetCrawlerLibrary(ID, Password, KickOtherLogin)
    if not PTTCrawler.isLoginSuccess():
        PTTCrawler.Log('Login fail')
        sys.exit()

    GetNewestPostIndexDemo()
    PostDemo()
    PushDemo()
    GetPostInfoDemo()
    GetNewPostIndexListDemo()
    #MainDemo()
    #GiveMoneyDemo()
    GetTimeDemo()
    
    PTTCrawler.logout()
    
    