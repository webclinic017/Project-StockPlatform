
import win32com.client
import pythoncom
import os, sys
import inspect

import sqlite3

import pandas as pd
from pandas import DataFrame, Series, Panel

class XASessionEvents:
    상태 = False

    def OnLogin(self, code, msg):
        print("OnLogin : ", code, msg)
        XASessionEvents.상태 = True

    def OnLogout(self):
        pass

    def OnDisconnect(self):
        pass

class XAQueryEvents:
    상태 = False

    def OnReceiveData(self, szTrCode):
        print("OnReceiveData : %s" % szTrCode)
        XAQueryEvents.상태 = True

    def OnReceiveMessage(self, systemError, messageCode, message):
        print("OnReceiveMessage : ", systemError, messageCode, message)


def Login(url='demo.ebestsec.co.kr', port=200001, svrtype=0, id='userid', pwd='password', cert='공인인증 비밀번호'):
    session = win32com.client.DispatchWithEvents("XA_Session.XASession", XASessionEvents)
    session.SetMode("_XINGAPI7_","TRUE")
    result = session.ConnectServer(url, port)

    if not result:
        nErrCode = session.GetLastError()
        strErrMsg = session.GetErrorMessage(nErrCode)
        return (False, nErrCode, strErrMsg, None, session)

    session.Login(id, pwd, cert, svrtype, 0)

    while XASessionEvents.상태 == False:
        pythoncom.PumpWaitingMessages()

    계좌 = []
    계좌수 = session.GetAccountListCount()

    for i in range(계좌수):
        계좌.append(session.GetAccountList(i))

    return (True, 0, "OK", 계좌, session)


def t1302(단축코드='',작업구분='1',시간='',건수='900'):
    '''
    주식분별주가조회
    '''
    query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
    pathname = os.path.dirname(sys.argv[0])
    RESDIR = os.path.abspath(pathname)

    MYNAME = inspect.currentframe().f_code.co_name
    INBLOCK = "%sInBlock" % MYNAME
    OUTBLOCK = "%sOutBlock" % MYNAME
    OUTBLOCK1 = "%sOutBlock1" % MYNAME
    RESFILE = "%s\\Res\\%s.res" % (RESDIR, MYNAME)

    query.LoadFromResFile(RESFILE)
    query.SetFieldData(INBLOCK, "shcode", 0, 단축코드)
    query.SetFieldData(INBLOCK, "gubun", 0, 작업구분)
    query.SetFieldData(INBLOCK, "time", 0, 시간)
    query.SetFieldData(INBLOCK, "cnt", 0, 건수)
    query.Request(0)

    while XAQueryEvents.상태 == False:
        pythoncom.PumpWaitingMessages()

    result = []
    nCount = query.GetBlockCount(OUTBLOCK)
    for i in range(nCount):
        시간CTS = query.GetFieldData(OUTBLOCK, "cts_time", i).strip()

        lst = [시간CTS]
        result.append(lst)

    df = DataFrame(data=result, columns=['시간CTS'])

    result = []
    nCount = query.GetBlockCount(OUTBLOCK1)
    for i in range(nCount):
        시간 = query.GetFieldData(OUTBLOCK1, "chetime", i).strip()
        종가 = int(query.GetFieldData(OUTBLOCK1, "close", i).strip())
        전일대비구분 = query.GetFieldData(OUTBLOCK1, "sign", i).strip()
        전일대비 = int(query.GetFieldData(OUTBLOCK1, "change", i).strip())
        등락율 = float(query.GetFieldData(OUTBLOCK1, "diff", i).strip())
        체결강도 = float(query.GetFieldData(OUTBLOCK1, "chdegree", i).strip())
        매도체결수량 = int(query.GetFieldData(OUTBLOCK1, "mdvolume", i).strip())
        매수체결수량 = int(query.GetFieldData(OUTBLOCK1, "msvolume", i).strip())
        순매수체결량 = int(query.GetFieldData(OUTBLOCK1, "revolume", i).strip())
        매도체결건수 = int(query.GetFieldData(OUTBLOCK1, "mdchecnt", i).strip())
        매수체결건수 = int(query.GetFieldData(OUTBLOCK1, "mschecnt", i).strip())
        순체결건수 = int(query.GetFieldData(OUTBLOCK1, "rechecnt", i).strip())
        거래량 = int(query.GetFieldData(OUTBLOCK1, "volume", i).strip())
        시가 = int(query.GetFieldData(OUTBLOCK1, "open", i).strip())
        고가 = int(query.GetFieldData(OUTBLOCK1, "high", i).strip())
        저가 = int(query.GetFieldData(OUTBLOCK1, "low", i).strip())
        체결량 = int(query.GetFieldData(OUTBLOCK1, "cvolume", i).strip())
        매도체결건수시간 = int(query.GetFieldData(OUTBLOCK1, "mdchecnttm", i).strip())
        매수체결건수시간 = int(query.GetFieldData(OUTBLOCK1, "mschecnttm", i).strip())
        매도잔량 = int(query.GetFieldData(OUTBLOCK1, "totofferrem", i).strip())
        매수잔량 = int(query.GetFieldData(OUTBLOCK1, "totbidrem", i).strip())
        시간별매도체결량 = int(query.GetFieldData(OUTBLOCK1, "mdvolumetm", i).strip())
        시간별매수체결량 = int(query.GetFieldData(OUTBLOCK1, "msvolumetm", i).strip())
        
        lst = [시간,종가,전일대비구분,전일대비,등락율,체결강도,매도체결수량,매수체결수량,순매수체결량,매도체결건수,매수체결건수,순체결건수,거래량,시가,고가,저가,체결량,매도체결건수시간,매수체결건수시간,매도잔량,매수잔량,시간별매도체결량,시간별매수체결량]
        result.append(lst)

    df1 = DataFrame(data=result, columns=['시간','종가','전일대비구분','전일대비','등락율','체결강도','매도체결수량','매수체결수량','순매수체결량','매도체결건수','매수체결건수','순체결건수','거래량','시가','고가','저가','체결량','매도체결건수시간','매수체결건수시간','매도잔량','매수잔량','시간별매도체결량','시간별매수체결량'])

    XAQueryEvents.상태 = False

    return (df, df1)

def t1305(단축코드='',일주월구분='1',날짜='',IDX='',건수='900'):
    '''
    기간별주가
    '''
    query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
    pathname = os.path.dirname(sys.argv[0])
    RESDIR = os.path.abspath(pathname)

    MYNAME = inspect.currentframe().f_code.co_name
    INBLOCK = "%sInBlock" % MYNAME
    OUTBLOCK = "%sOutBlock" % MYNAME
    OUTBLOCK1 = "%sOutBlock1" % MYNAME
    RESFILE = "%s\\Res\\%s.res" % (RESDIR, MYNAME)

    query.LoadFromResFile(RESFILE)
    query.SetFieldData(INBLOCK, "shcode", 0, 단축코드)
    query.SetFieldData(INBLOCK, "dwmcode", 0, 일주월구분)
    query.SetFieldData(INBLOCK, "date", 0, 날짜)
    query.SetFieldData(INBLOCK, "idx", 0, IDX)
    query.SetFieldData(INBLOCK, "cnt", 0, 건수)
    query.Request(0)

    while XAQueryEvents.상태 == False:
        pythoncom.PumpWaitingMessages()

    result = []
    nCount = query.GetBlockCount(OUTBLOCK)
    for i in range(nCount):
        CNT = int(query.GetFieldData(OUTBLOCK, "cnt", i).strip())
        날짜 = query.GetFieldData(OUTBLOCK, "date", i).strip()
        IDX = int(query.GetFieldData(OUTBLOCK, "idx", i).strip())

        lst = [CNT,날짜,IDX]
        result.append(lst)

    df = DataFrame(data=result, columns=['CNT','날짜','IDX'])

    result = []
    nCount = query.GetBlockCount(OUTBLOCK1)
    for i in range(nCount):
        날짜 = query.GetFieldData(OUTBLOCK1, "date", i).strip()
        시가 = int(query.GetFieldData(OUTBLOCK1, "open", i).strip())
        고가 = int(query.GetFieldData(OUTBLOCK1, "high", i).strip())
        저가 = int(query.GetFieldData(OUTBLOCK1, "low", i).strip())
        종가 = int(query.GetFieldData(OUTBLOCK1, "close", i).strip())
        전일대비구분 = query.GetFieldData(OUTBLOCK1, "sign", i).strip()
        전일대비 = int(query.GetFieldData(OUTBLOCK1, "change", i).strip())
        등락율 = float(query.GetFieldData(OUTBLOCK1, "diff", i).strip())
        누적거래량 = int(query.GetFieldData(OUTBLOCK1, "volume", i).strip())
        거래증가율 = float(query.GetFieldData(OUTBLOCK1, "diff_vol", i).strip())
        체결강도 = float(query.GetFieldData(OUTBLOCK1, "chdegree", i).strip())
        소진율 = float(query.GetFieldData(OUTBLOCK1, "sojinrate", i).strip())
        회전율 = float(query.GetFieldData(OUTBLOCK1, "changerate", i).strip())
        외인순매수 = int(query.GetFieldData(OUTBLOCK1, "fpvolume", i).strip())
        기관순매수 = int(query.GetFieldData(OUTBLOCK1, "covolume", i).strip())
        종목코드 = query.GetFieldData(OUTBLOCK1, "shcode", i).strip()
        누적거래대금 = int(query.GetFieldData(OUTBLOCK1, "value", i).strip())
        개인순매수 = int(query.GetFieldData(OUTBLOCK1, "ppvolume", i).strip())
        시가대비구분 = query.GetFieldData(OUTBLOCK1, "o_sign", i).strip()
        시가대비 = int(query.GetFieldData(OUTBLOCK1, "o_change", i).strip())
        시가기준등락율 = float(query.GetFieldData(OUTBLOCK1, "o_diff", i).strip())
        고가대비구분 = query.GetFieldData(OUTBLOCK1, "h_sign", i).strip()
        고가대비 = int(query.GetFieldData(OUTBLOCK1, "h_change", i).strip())
        고가기준등락율 = float(query.GetFieldData(OUTBLOCK1, "h_diff", i).strip())
        저가대비구분 = query.GetFieldData(OUTBLOCK1, "l_sign", i).strip()
        저가대비 = int(query.GetFieldData(OUTBLOCK1, "l_change", i).strip())
        저가기준등락율 = float(query.GetFieldData(OUTBLOCK1, "l_diff", i).strip())
        시가총액 = int(query.GetFieldData(OUTBLOCK1, "marketcap", i).strip())

        lst = [날짜,시가,고가,저가,종가,전일대비구분,전일대비,등락율,누적거래량,거래증가율,체결강도,소진율,회전율,외인순매수,기관순매수,종목코드,누적거래대금,개인순매수,시가대비구분,시가대비,시가기준등락율,고가대비구분,고가대비,고가기준등락율,저가대비구분,저가대비,저가기준등락율,시가총액]
        result.append(lst)

    df1 = DataFrame(data=result, columns=['날짜','시가','고가','저가','종가','전일대비구분','전일대비','등락율','누적거래량','거래증가율','체결강도','소진율','회전율','외인순매수','기관순매수','종목코드','누적거래대금','개인순매수','시가대비구분','시가대비','시가기준등락율','고가대비구분','고가대비','고가기준등락율','저가대비구분','저가대비','저가기준등락율','시가총액'])

    XAQueryEvents.상태 = False

    return (df, df1)

def t1308(단축코드='069500',시작시간='',종료시간='',분간격='1'):
    '''
    주식시간대별체결조회차트
    '''
    query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
    pathname = os.path.dirname(sys.argv[0])
    RESDIR = os.path.abspath(pathname)

    MYNAME = inspect.currentframe().f_code.co_name
    INBLOCK = "%sInBlock" % MYNAME
    OUTBLOCK = "%sOutBlock" % MYNAME
    OUTBLOCK1 = "%sOutBlock1" % MYNAME
    RESFILE = "%s\\Res\\%s.res" % (RESDIR, MYNAME)

    query.LoadFromResFile(RESFILE)
    query.SetFieldData(INBLOCK, "shcode", 0, 단축코드)
    query.SetFieldData(INBLOCK, "starttime", 0, 시작시간)
    query.SetFieldData(INBLOCK, "endtime", 0, 종료시간)
    query.SetFieldData(INBLOCK, "bun_term", 0, 분간격)
    query.Request(0)

    while XAQueryEvents.상태 == False:
        pythoncom.PumpWaitingMessages()

    result = []
    nCount = query.GetBlockCount(OUTBLOCK1)
    for i in range(nCount):
        시간 = query.GetFieldData(OUTBLOCK1, "chetime", i).strip()
        현재가 = int(query.GetFieldData(OUTBLOCK1, "price", i).strip())
        전일대비구분 = query.GetFieldData(OUTBLOCK1, "sign", i).strip()
        전일대비 = int(query.GetFieldData(OUTBLOCK1, "change", i).strip())
        등락율 = float(query.GetFieldData(OUTBLOCK1, "diff", i).strip())
        체결수량 = int(query.GetFieldData(OUTBLOCK1, "cvolume", i).strip())
        체결강도거래량 = float(query.GetFieldData(OUTBLOCK1, "chdegvol", i).strip())
        체결강도건수 = float(query.GetFieldData(OUTBLOCK1, "chdegcnt", i).strip())
        거래량 = int(query.GetFieldData(OUTBLOCK1, "volume", i).strip())
        매도체결수량 = int(query.GetFieldData(OUTBLOCK1, "mdvolume", i).strip())
        매도체결건수 = int(query.GetFieldData(OUTBLOCK1, "mdchecnt", i).strip())
        매수체결수량 = int(query.GetFieldData(OUTBLOCK1, "msvolume", i).strip())
        매수체결건수 = int(query.GetFieldData(OUTBLOCK1, "mschecnt", i).strip())
        시가 = int(query.GetFieldData(OUTBLOCK1, "open", i).strip())
        고가 = int(query.GetFieldData(OUTBLOCK1, "high", i).strip())
        저가 = int(query.GetFieldData(OUTBLOCK1, "low", i).strip())

        lst = [시간,현재가,전일대비구분,전일대비,등락율,체결수량,체결강도거래량,체결강도건수,거래량,매도체결수량,매도체결건수,매수체결수량,매수체결건수,시가,고가,저가]
        result.append(lst)

    XAQueryEvents.상태 = False

    columns=['시간','현재가','전일대비구분','전일대비','등락율','체결수량','체결강도거래량','체결강도건수','거래량','매도체결수량','매도체결건수','매수체결수량','매수체결건수','시가','고가','저가']
    df = DataFrame(data=result, columns=columns)
    return df

def t1702(종목코드='069500',종료일자='',금액수량구분='0',매수매도구분='0',누적구분='0',CTSDATE='',CTSIDX=''):
    '''
    외인기관종목별동향
    '''
    query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
    pathname = os.path.dirname(sys.argv[0])
    RESDIR = os.path.abspath(pathname)

    MYNAME = inspect.currentframe().f_code.co_name
    INBLOCK = "%sInBlock" % MYNAME
    OUTBLOCK = "%sOutBlock" % MYNAME
    OUTBLOCK1 = "%sOutBlock1" % MYNAME
    RESFILE = "%s\\Res\\%s.res" % (RESDIR, MYNAME)

    query.LoadFromResFile(RESFILE)
    query.SetFieldData(INBLOCK, "shcode", 0, 종목코드)
    query.SetFieldData(INBLOCK, "todt", 0, 종료일자)
    query.SetFieldData(INBLOCK, "volvalgb", 0, 금액수량구분)
    query.SetFieldData(INBLOCK, "msmdgb", 0, 매수매도구분)
    query.SetFieldData(INBLOCK, "cumulgb", 0, 누적구분)
    query.SetFieldData(INBLOCK, "cts_date", 0, CTSDATE)
    query.SetFieldData(INBLOCK, "cts_idx", 0, CTSIDX)
    query.Request(0)

    while XAQueryEvents.상태 == False:
        pythoncom.PumpWaitingMessages()

    result = []
    nCount = query.GetBlockCount(OUTBLOCK)
    for i in range(nCount):
        CTSIDX = int(query.GetFieldData(OUTBLOCK, "cts_idx", i).strip())
        CTSDATE = query.GetFieldData(OUTBLOCK, "cts_date", i).strip()

        lst = [CTSIDX,CTSDATE]
        result.append(lst)

    df = DataFrame(data=result, columns=['CTSIDX','CTSDATE'])

    result = []
    nCount = query.GetBlockCount(OUTBLOCK1)
    for i in range(nCount):
        일자 = query.GetFieldData(OUTBLOCK1, "date", i).strip()
        종가 = int(query.GetFieldData(OUTBLOCK1, "close", i).strip())
        전일대비구분 = query.GetFieldData(OUTBLOCK1, "sign", i).strip()
        전일대비 = int(query.GetFieldData(OUTBLOCK1, "change", i).strip())
        등락율 = float(query.GetFieldData(OUTBLOCK1, "diff", i).strip())
        누적거래량 = int(query.GetFieldData(OUTBLOCK1, "volume", i).strip())
        사모펀드 = int(query.GetFieldData(OUTBLOCK1, "amt0000", i).strip())
        증권 = int(query.GetFieldData(OUTBLOCK1, "amt0001", i).strip())
        보험 = int(query.GetFieldData(OUTBLOCK1, "amt0002", i).strip())
        투신 = int(query.GetFieldData(OUTBLOCK1, "amt0003", i).strip())
        은행 = int(query.GetFieldData(OUTBLOCK1, "amt0004", i).strip())
        종금 = int(query.GetFieldData(OUTBLOCK1, "amt0005", i).strip())
        기금 = int(query.GetFieldData(OUTBLOCK1, "amt0006", i).strip())
        try:
            기타법인 = int(query.GetFieldData(OUTBLOCK1, "amt0007", i).strip())
        except Exception as e:
            기타법인 = 0
        개인 = int(query.GetFieldData(OUTBLOCK1, "amt0008", i).strip())
        등록외국인 = int(query.GetFieldData(OUTBLOCK1, "amt0009", i).strip())
        try:
            미등록외국인 = int(query.GetFieldData(OUTBLOCK1, "amt0010", i).strip())
        except Exception as e:
            미등록외국인 = 0
        국가외 = int(query.GetFieldData(OUTBLOCK1, "amt0011", i).strip())
        기관 = int(query.GetFieldData(OUTBLOCK1, "amt0018", i).strip())
        외인계 = int(query.GetFieldData(OUTBLOCK1, "amt0088", i).strip())
        기타계 = int(query.GetFieldData(OUTBLOCK1, "amt0099", i).strip())

        lst = [일자,종가,전일대비구분,전일대비,등락율,누적거래량,사모펀드,증권,보험,투신,은행,종금,기금,기타법인,개인,등록외국인,미등록외국인,국가외,기관,외인계,기타계]
        result.append(lst)

    XAQueryEvents.상태 = False

    columns=['일자','종가','전일대비구분','전일대비','등락율','누적거래량','사모펀드','증권','보험','투신','은행','종금','기금','기타법인','개인','등록외국인','미등록외국인','국가외','기관','외인계','기타계']
    df1 = DataFrame(data=result, columns=columns)
    return (df, df1)

# 외인기관종목별동향
def t1717(종목코드='069500',구분='0',시작일자='20170101',종료일자='20172131'):
    '''
    외인기관종목별동향
    '''
    query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQueryEvents)
    pathname = os.path.dirname(sys.argv[0])
    RESDIR = os.path.abspath(pathname)

    MYNAME = inspect.currentframe().f_code.co_name
    INBLOCK = "%sInBlock" % MYNAME
    OUTBLOCK = "%sOutBlock" % MYNAME
    OUTBLOCK1 = "%sOutBlock1" % MYNAME
    RESFILE = "%s\\Res\\%s.res" % (RESDIR, MYNAME)

    query.LoadFromResFile(RESFILE)
    query.SetFieldData(INBLOCK, "shcode", 0, 종목코드)
    query.SetFieldData(INBLOCK, "gubun", 0, 구분)
    query.SetFieldData(INBLOCK, "fromdt", 0, 시작일자)
    query.SetFieldData(INBLOCK, "todt", 0, 종료일자)
    query.Request(0)

    while XAQueryEvents.상태 == False:
        pythoncom.PumpWaitingMessages()

    result = []
    nCount = query.GetBlockCount(OUTBLOCK)
    for i in range(nCount):
        일자 = query.GetFieldData(OUTBLOCK, "date", i).strip()
        종가 = int(query.GetFieldData(OUTBLOCK, "close", i).strip())
        전일대비구분 = query.GetFieldData(OUTBLOCK, "sign", i).strip()
        전일대비 = int(query.GetFieldData(OUTBLOCK, "change", i).strip())
        등락율 = float(query.GetFieldData(OUTBLOCK, "diff", i).strip())
        누적거래량 = int(query.GetFieldData(OUTBLOCK, "volume", i).strip())
        사모펀드_순매수 = int(query.GetFieldData(OUTBLOCK, "tjj0000_vol", i).strip())
        증권_순매수 = int(query.GetFieldData(OUTBLOCK, "tjj0001_vol", i).strip())
        보험_순매수 = int(query.GetFieldData(OUTBLOCK, "tjj0002_vol", i).strip())
        투신_순매수 = int(query.GetFieldData(OUTBLOCK, "tjj0003_vol", i).strip())
        은행_순매수 = int(query.GetFieldData(OUTBLOCK, "tjj0004_vol", i).strip())
        종금_순매수 = int(query.GetFieldData(OUTBLOCK, "tjj0005_vol", i).strip())
        기금_순매수 = int(query.GetFieldData(OUTBLOCK, "tjj0006_vol", i).strip())
        기타법인_순매수 = int(query.GetFieldData(OUTBLOCK, "tjj0007_vol", i).strip())
        개인_순매수 = int(query.GetFieldData(OUTBLOCK, "tjj0008_vol", i).strip())
        등록외국인_순매수 = int(query.GetFieldData(OUTBLOCK, "tjj0009_vol", i).strip())
        미등록외국인_순매수 = int(query.GetFieldData(OUTBLOCK, "tjj0010_vol", i).strip())
        국가외_순매수 = int(query.GetFieldData(OUTBLOCK, "tjj0011_vol", i).strip())
        기관_순매수 = int(query.GetFieldData(OUTBLOCK, "tjj0018_vol", i).strip())
        외인계_순매수 = int(query.GetFieldData(OUTBLOCK, "tjj0016_vol", i).strip())
        기타계_순매수 = int(query.GetFieldData(OUTBLOCK, "tjj0017_vol", i).strip())
        사모펀드_단가 = int(query.GetFieldData(OUTBLOCK, "tjj0000_dan", i).strip())
        증권_단가 = int(query.GetFieldData(OUTBLOCK, "tjj0001_dan", i).strip())
        보험_단가 = int(query.GetFieldData(OUTBLOCK, "tjj0002_dan", i).strip())
        투신_단가 = int(query.GetFieldData(OUTBLOCK, "tjj0003_dan", i).strip())
        은행_단가 = int(query.GetFieldData(OUTBLOCK, "tjj0004_dan", i).strip())
        종금_단가 = int(query.GetFieldData(OUTBLOCK, "tjj0005_dan", i).strip())
        기금_단가 = int(query.GetFieldData(OUTBLOCK, "tjj0006_dan", i).strip())
        기타법인_단가 = int(query.GetFieldData(OUTBLOCK, "tjj0007_dan", i).strip())
        개인_단가 = int(query.GetFieldData(OUTBLOCK, "tjj0008_dan", i).strip())
        등록외국인_단가 = int(query.GetFieldData(OUTBLOCK, "tjj0009_dan", i).strip())
        미등록외국인_단가 = int(query.GetFieldData(OUTBLOCK, "tjj0010_dan", i).strip())
        국가외_단가 = int(query.GetFieldData(OUTBLOCK, "tjj0011_dan", i).strip())
        기관_단가 = int(query.GetFieldData(OUTBLOCK, "tjj0018_dan", i).strip())
        외인계_단가 = int(query.GetFieldData(OUTBLOCK, "tjj0016_dan", i).strip())
        기타계_단가 = int(query.GetFieldData(OUTBLOCK, "tjj0017_dan", i).strip())

        lst = [일자,종가,전일대비구분,전일대비,등락율,누적거래량,
        사모펀드_순매수,증권_순매수,보험_순매수,투신_순매수,은행_순매수,종금_순매수,기금_순매수,기타법인_순매수,개인_순매수,등록외국인_순매수,미등록외국인_순매수,국가외_순매수,기관_순매수,외인계_순매수,기타계_순매수,
        사모펀드_단가,증권_단가,보험_단가,투신_단가,은행_단가,종금_단가,기금_단가,기타법인_단가,개인_단가,등록외국인_단가,미등록외국인_단가,국가외_단가,기관_단가,외인계_단가,기타계_단가]

        result.append(lst)

    columns=['일자','종가','전일대비구분','전일대비','등락율','누적거래량','사모펀드_순매수','증권_순매수','보험_순매수','투신_순매수','은행_순매수','종금_순매수','기금_순매수','기타법인_순매수','개인_순매수','등록외국인_순매수','미등록외국인_순매수','국가외_순매수','기관_순매수','외인계_순매수','기타계_순매수','사모펀드_단가','증권_단가','보험_단가','투신_단가','은행_단가','종금_단가','기금_단가','기타법인_단가','개인_단가','등록외국인_단가','미등록외국인_단가','국가외_단가','기관_단가','외인계_단가','기타계_단가']
    df = DataFrame(data=result, columns=columns)

    XAQueryEvents.상태 = False

    return (df)


if __name__ == "__main__":
    계좌정보 = pd.read_csv("secret/passwords.csv", converters={'계좌번호': str, '거래비밀번호': str})
    주식계좌정보 = 계좌정보.query("구분 == '거래'")
    if len(주식계좌정보) == 0:
        print("secret디렉토리의 passwords.csv 파일에서 거래 계좌를 지정해 주세요")
    else:
        계좌번호 = 주식계좌정보['계좌번호'].values[0].strip()
        id = 주식계좌정보['사용자ID'].values[0].strip()
        pwd = 주식계좌정보['비밀번호'].values[0].strip()
        cert = 주식계좌정보['공인인증비밀번호'][0].strip()
        거래비밀번호 = 주식계좌정보['거래비밀번호'].values[0].strip()
        url = 주식계좌정보['url'][0].strip()

        result, code, msg, 계좌, session = Login(url=url, port=200001, svrtype=0,id=id, pwd=pwd,cert=cert)
        if result == False:
            sys.exit(0)

        # df0, df = t1305(단축코드='069500',일주월구분='1',날짜='',IDX='',건수='1000')
        # with sqlite3.connect('data/Darjeeling.sqlite') as conn:
        #     df.to_sql('기간별주가', con=conn, if_exists='replace', index=False)

        # df0, df = t1302(단축코드='069500',작업구분='1',시간='',건수='900')
        # with sqlite3.connect('data/Darjeeling.sqlite') as conn:
        #     df.to_sql('주식분별주가조회', con=conn, if_exists='replace', index=False)

        # df = t1308(단축코드='069500',시작시간='0900',종료시간='1000',분간격='')
        # with sqlite3.connect('data/Darjeeling.sqlite') as conn:
        #     df.to_sql('주식시간대별체결조회', con=conn, if_exists='replace', index=False)
        

        # df0, df = t1702(종목코드='069500',종료일자='',금액수량구분='0',매수매도구분='0',누적구분='0',CTSDATE='',CTSIDX='')

        df = t1717(종목코드='069500',구분='0',시작일자='20170101',종료일자='20172131')
        print(df)