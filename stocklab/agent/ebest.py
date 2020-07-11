import configparser
import win32com.client
import pythoncom
from datetime import datetime
import time

class XASession:
    #로그인 상태를 확인하기 위한 클래스변수
    login_state = 0

    def OnLogin(self, code, msg):
        """
        로그인 시도 후 호출되는 이벤트.
        code가 0000이면 로그인 성공
        """
        if code == "0000":
            print(code, msg)
            XASession.login_state = 1
        else:
            print(code, msg)

    def OnDisconnect(self):
        """
        서버와 연결이 끊어지면 발생하는 이벤트
        """
        print("Session disconntected")
        XASession.login_state = 0


class XAQuery:
    RES_PATH ="C:\\eBEST\\xingAPI\\Res\\"
    tr_run_state = 0

    def OnReceiveData(self, code):
        print("OnReceiveData", code)
        XAQuery.tr_run_state = 1

    def OnReceiveMessage(self, error, code, message):
        print("OnReceiveMessage", error, code, message, XAQuery.tr_run_state)

class XAReal:
    RES_PATH = "C:\\eBEST\\xingAPI\\Res\\"

    def register_code(self, code):
        print("register code", code)
        self.LoadFromResFile(XAReal.RES_PATH + "K3_.res")
        self.SetFieldData("InBlock", "shcode", code)
        self.AdviseRealData()

    def OnReceiveRealData(self, tr_code):
        print("tr_code", tr_code)
        result = []
        for field in ["chetime", "sign", "change", "drate", "price", "opentime", "open",
                      "hightime", "high", "lowtime", "low", "cgubun", "cvolume", "volume",
                      "mdvolume", "mdchecnt", "msvolume", "mschecnt", "cpower", "w_avrg",
                      "offerho", "bidho", "status", "jnilvolume", "shcode"]:
            value = self.GetFieldData("OutBlock", field)
            item[field] = value
            result.append(item)
        print(result)

class EBest:
    QUERY_LIMIT_10MIN = 200
    LIMIT_SECONDS = 600 #10min

    def __init__(self, mode=None):
        """
        config.ini 파일을 로드해 사용자, 서버정보 저장
        query_cnt는 10분당 200개 TR 수행을 관리하기 위한 리스트
        xa_session_client는 XASession 객체
        :param mode:str - 모의서버는 DEMO 실서버는 PROD로 구분
        """
        if mode not in ["PROD", "DEMO", "ACE"]:
            raise Exception("Need to run_mode(PROD or DEMO or ACE)")

        run_mode = "EBEST_" + mode
        config = configparser.ConfigParser()
        config.read('conf/config.ini')
        self.user = config[run_mode]['user']
        self.passwd = config[run_mode]['password']
        self.cert_passwd = config[run_mode]['cert_passwd']
        self.host = config[run_mode]['host']
        self.port = config[run_mode]['port']
        self.account = config[run_mode]['account']

        self.xa_session_client = win32com.client.DispatchWithEvents("XA_Session.XASession", XASession)

        self.query_cnt = []

    def login(self):
        self.xa_session_client.ConnectServer(self.host, self.port)
        self.xa_session_client.Login(self.user, self.passwd, self.cert_passwd, 0, 0)
        while XASession.login_state == 0:
            pythoncom.PumpWaitingMessages()

    def logout(self):
        XASession.login_state = 0
        self.xa_session_client.DisconnectServer()

    def _execute_query(self, res, in_block_name, out_block_name, *out_fields, **set_fields):
        """TR코드를 실행하기 위한 메소드입니다.
        :param res:str 리소스명(TR)
        :param in_block_name:str 인블록명
        :param out_blcok_name:str 아웃블록명
        :param out_params:list 출력필드 리스트
        :param in_params:dict 인블록에 설정할 필드 딕셔너리
        :return result:list 결과를 list에 담아 반환 
        """
        time.sleep(1)
        print("current query cnt:", len(self.query_cnt))
        print(res, in_block_name, out_block_name)
        while len(self.query_cnt) >= EBest.QUERY_LIMIT_10MIN:
            time.sleep(1)
            print("waiting for execute query... current query cnt:", len(self.query_cnt))
            self.query_cnt = list(filter(lambda x: (datetime.today() - x).total_seconds() < EBest.LIMIT_SECONDS, self.query_cnt))

        xa_query = win32com.client.DispatchWithEvents("XA_DataSet.XAQuery", XAQuery)
        xa_query.LoadFromResFile(XAQuery.RES_PATH + res+".res")

        #in_block_name 셋팅
        for key, value in set_fields.items():
            xa_query.SetFieldData(in_block_name, key, 0, value)
        errorCode = xa_query.Request(0)

        #요청 후 대기
        waiting_cnt = 0
        while xa_query.tr_run_state == 0:
            waiting_cnt +=1
            if waiting_cnt % 1000000 == 0 :
                print("Waiting....", self.xa_session_client.GetLastError())
            pythoncom.PumpWaitingMessages()

        #결과블럭 
        result = []
        count = xa_query.GetBlockCount(out_block_name)

        for i in range(count):
            item = {}
            for field in out_fields:
                value = xa_query.GetFieldData(out_block_name, field, i)
                item[field] = value
            result.append(item)

        """
        print("IsNext?", xa_query.IsNext)
        while xa_query.IsNext == True:
            time.sleep(1)
            errorCode = xa_query.Request(1)
            print("errorCode", errorCode)
            if errorCode < 0:
                break
            count = xa_query.GetBlockCount(out_block_name)
            print("count", count)
            if count == 0:
                break
            for i in range(count):
                item = {}
                for field in out_fields:
                    value = xa_query.GetFieldData(out_block_name, field, i)
                    item[field] = value
                print(item)
                result.append(item)
        """
        XAQuery.tr_run_state = 0
        self.query_cnt.append(datetime.today())

        #영문필드를 한글필드명으로 변환
        for item in result:
            for field in list(item.keys()):
                if getattr(Field, res, None):
                    res_field = getattr(Field, res, None)
                    if out_block_name in res_field:
                        field_hname = res_field[out_block_name]
                        if field in field_hname:
                            item[field_hname[field]] = item[field]
                            item.pop(field)
        return result

    def get_tick_size(self, price):
        """호가 단위 조회 메소드
        참고:    
        http://regulation.krx.co.kr/contents/RGL/03/03010100/RGL03010100.jsp#8339ae36256c1f6cffd910cd71e4dc85=3
        http://regulation.krx.co.kr/contents/RGL/03/03020100/RGL03020100.jsp
 
        :param price:int 가격
        :return 호가 단위
        """
        if price < 1000: return 1
        elif price >=1000 and price < 5000: return 5
        elif price >=5000 and price < 10000: return 10
        elif price >=10000 and price < 50000: return 50
        elif price >=50000 and price < 100000: return 100
        elif price >=100000 and price < 500000: return 500
        elif price >=500000: return 1000

    def get_current_call_price_by_code(self, code=None):
        """TR: t1101 주식 현재가 호가 조회
        :param code:str 종목코드
        """
        tr_code = "t1101"
        in_params = {"shcode": code}
        out_params =["hname", "price", "sign", "change", "diff", "volume", 
            "jnilclose", "offerho1","bidho1", "offerrem1", "bidrem1",
            "offerho2","bidho2", "offerrem2", "bidrem2",
            "offerho3","bidho3", "offerrem3", "bidrem3",
            "offerho4","bidho4", "offerrem4", "bidrem4",
            "offerho5","bidho5", "offerrem5", "bidrem5",
            "offerho6","bidho6", "offerrem6", "bidrem6",
            "offerho7","bidho7", "offerrem7", "bidrem7",
            "offerho8","bidho8", "offerrem8", "bidrem8",
            "offerho9","bidho9", "offerrem9", "bidrem9",
            "offerho10","bidho10", "offerrem10", "bidrem10",
            "preoffercha10", "prebidcha10", "offer", "bid",
            "preoffercha", "prebidcha", "hotime", "yeprice", "yevolume",
            "yesign", "yechange", "yediff", "tmoffer", "tmbid", "ho_status",
            "shcode", "uplmtprice", "dnlmtprice", "open", "high", "low"]

        result = self._execute_query("t1101", 
                                "t1101InBlock", 
                                "t1101OutBlock",
                                *out_params,
                                **in_params)

        for item in result:
            item["code"] = code

        return result
 
    def get_stock_price_by_code(self, code=None, cnt="1"):
        """TR: t1305 현재 날짜를 기준으로 cnt 만큼 전일의 데이터를 가져온다
        :param code:str 종목코드
        :param cnt:str 데이터 범위
        :return result:list 종목의 최근 가격 정보
        """
        tr_code = "t1305"
        in_params = {"shcode":code, "dwmcode": "1", "date":"", "idx":"", "cnt":cnt}
        out_params =['date', 'open', 'high', 'low', 'close', 'sign', 
                    'change', 'diff', 'volume', 'diff_vol', 'chdegree', 
                    'sojinrate', 'changerate', 'fpvolume', 'covolume', 
                    'value', 'ppvolume', 'o_sign', 'o_change', 'o_diff', 
                    'h_sign', 'h_change', 'h_diff', 'l_sign', 'l_change', 
                    'l_diff', 'marketcap'] 
        #t8413
        #in_params = {"shcode":code, "qrycnt": "1", "gubun":"2", "sdate":start, "cts_date":"", "edate":end, "comp_yn":"N"}    
        #out_params =['date', 'open', 'high', 'low', 'close', 'jdiff_vol', 'sign'] 
        result = self._execute_query("t1305", 
                                "t1305InBlock", 
                                "t1305OutBlock1",
                                *out_params,
                                **in_params)

        for item in result:
            item["code"] = code

        return result
        
    def get_code_list(self, market=None):
        """TR: t8436 코스피, 코스닥의 종목 리스트를 가져온다
        :param market:str 전체(0), 코스피(1), 코스닥(2)
        :return result:list 시장 별 종목 리스트
        """
        if market not in ["ALL", "KOSPI", "KOSDAQ"]:
            raise Exception("Need to market param(ALL, KOSPI, KOSDAQ)")

        market_code = {"ALL":"0", "KOSPI":"1", "KOSDAQ":"2"}
        in_params = {"gubun":market_code[market]}
        out_params =['hname', 'shcode', 'expcode', 'etfgubun', 'memedan', 'gubun', 'spac_gubun'] 
        result = self._execute_query("t8436", 
                                "t8436InBlock", 
                                "t8436OutBlock",
                                *out_params,
                                **in_params)
        return result

    def get_credit_trend_by_code(self, code=None, date=None):
        """TR: t1921 신용거래동향 
        :param code:str 종목코드
        :param date:str 날짜 8자리 ex) 20190222
        """
        in_params = {"gubun":"0", "shcode":code, "date":date, "idx":"0"}
        out_params =["mmdate", "close", "sign", "jchange", "diff", "nvolume",
                    "svolume", "jvolume", "price", "change", "gyrate", "jkrate"
                    "shcode"]

        result = self._execute_query("t1921",
                                    "t1921InBlock",
                                    "t1921OutBlock1",
                                    *out_params,
                                    **in_params)
        for item in result:
            item["code"] = code

        return result


    def get_agent_trend_by_code(self, code=None ,fromdt=None, todt=None):
        """TR: t1717 외인기관별 종목별 동향
        :param code:str 종목코드
        :param fromdt:str 조회 시작 날짜
        :param todt:str 조회 종료 날짜
        :return result:list 시장 별 종목 리스트
        """
        in_params = {"gubun":"0", "fromdt":fromdt, "todt":todt, "shcode":code}
        out_params =["date", "close", "sign", "change", "diff", "volume", 
                    "tjj0000_vol", "tjj0001_vol", "tjj0002_vol", "tjj0003_vol",
                    "tjj0004_vol", "tjj0005_vol","tjj0006_vol", "tjj0007_vol",
                    "tjj0008_vol", "tjj0009_vol", "tjj0010_vol", "tjj0011_vol",
                    "tjj0018_vol", "tjj0016_vol", "tjj0017_vol", "tjj0001_dan",
                    "tjj0002_dan", "tjj0003_dan", "tjj0004_dan", "tjj0005_dan",
                    "tjj0006_dan", "tjj0007_dan", "tjj0008_dan", "tjj0009_dan",
                    "tjj0010_dan", "tjj0011_dan", "tjj0018_dan", "tjj0016_dan",
                    "tjj0017_dan" ] 
        result = self._execute_query("t1717",
                                    "t1717InBlock",
                                    "t1717OutBlock",
                                    *out_params,
                                    **in_params)
        for item in result:
            item["code"] = code

        return result

    def get_short_trend_by_code(self, code=None, sdate=None, edate=None):
        """TR: t1927 공매도일별추이
        :param code:str 종목코드
        :param sdate:str 시작일자 
        :param edate:str 종료일자
        :return result:list 시장 별 종목 리스트
        """
        in_params = {"date":sdate, "sdate":sdate, "edate":edate, "shcode":code}
        out_params =["date", "price", "sign", "change", "diff", "volume", "value", 
                    "gm_vo", "gm_va", "gm_per", "gm_avg", "gm_vo_sum"]

        result = self._execute_query("t1927",
                                    "t1927InBlock",
                                    "t1927OutBlock1",
                                    *out_params,
                                    **in_params)

        for item in result:
            item["code"] = code

        return result

    def get_theme_by_code(self, code):
        if code is None:
            raise Exception("Need to code param")

        in_params = {"shcode":code}
        out_params =['tmname', 'tmcode'] 
        result = self._execute_query("t1532", 
                                "t1532InBlock", 
                                "t1532OutBlock",
                                *out_params,
                                **in_params)
        return result

    def get_theme_list(self):
        in_params = {"dummy":"1"}
        out_params =['tmname', 'tmcode'] 
        result = self._execute_query("t8425", 
                                "t8425InBlock", 
                                "t8425OutBlock",
                                *out_params,
                                **in_params)
        return result

    def get_category_list(self):
        in_params = {"gubun1":"1"}
        out_params =['hname', 'upcode'] 
        result = self._execute_query("t8424", 
                                "t8424InBlock", 
                                "t8424OutBlock",
                                *out_params,
                                **in_params)
        return result
    
    def get_price_by_category(self, upcode=None):
        if upcode is None:
            raise Exception("Need to upcode")
        in_params = {"gubun":"0", "upcode":upcode}
        out_params =['hname', 'price', 'sign', 'change', 'diff', 
                    'volume', 'open', 'high', 'low', 'perx', 
                    'frgsvolume', 'orgsvolume', 'diff_vol', 'total', 
                    'value', 'shcode'] 
        result = self._execute_query("t1516",
                                    "t1516InBlock",
                                    "t1516OutBlock1",
                                    *out_params,
                                    **in_params)
        return result

    def get_price_by_theme(self, tmcode=None):
        if tmcode is None:
            raise Exception("Need to tmcode")
        in_params = {"tmcode":tmcode}
        out_params =['hname', 'price', 'sign', 'change', 'diff', 'shcode'
                    'volume', 'open', 'high', 'low', 'value'] 
        result = self._execute_query("t1537",
                                    "t1537InBlock",
                                    "t1537OutBlock1",
                                    *out_params,
                                    **in_params)
        return result




    def get_event_by_code(self, code=None, date=None):
        if code is None:
            raise Exception("Need to tmcode")
        in_params = {"shcode":code, "date":date}
        out_params =["recdt", "tableid", "upgu", 
                    "custno", "custnm", "shcode", "upnm" ]
        result = self._execute_query("t3202",
                                    "t3202InBlock",
                                    "t3202OutBlock",
                                    *out_params,
                                    **in_params)
        return result

    def get_trade_history(self, count=None):
        in_params = {"RecCnt": count, "AcntNo": self.account, "Pwd": self.passwd,
                     "QrySrtDt":"20181201", "QryEndDt":"20181205"}
        out_params =["recdt", "tableid", "upgu", 
                    "custno", "custnm", "shcode", "upnm" ]
        result = self._execute_query("CDPCQ04700",
                                    "CDPCQ04700InBlock1",
                                    "CDPCQ04700OutBlock1",
                                    *out_params,
                                    **in_params)
        return result

    def get_account_info(self):
        """TR: CSPAQ12200 현물계좌 예수금/주문가능금액/총평가
        :return result:list Field CSPAQ12200 참고
        """
        in_params = {"RecCnt":"1", "AcntNo": self.account, "Pwd": self.passwd}
        out_params =["MnyOrdAbleAmt", "BalEvalAmt", "DpsastTotamt", 
                    "InvstOrgAmt", "InvstPlAmt", "Dps"]
        result = self._execute_query("CSPAQ12200",
                                    "CSPAQ12200InBlock1",
                                    "CSPAQ12200OutBlock2",
                                    *out_params,
                                    **in_params)
        return result

    def get_account_stock_info(self):
        """TR: CSPAQ12300 현물계좌 잔고내역 조회
        :return result:list 계좌 보유 종목 정보
        """
        in_params = {"RecCnt": "1", "AcntNo": self.account, "Pwd": self.passwd, "BalCreTp": "0", "CmsnAppTpCode": "0", "D2balBaseQryTp": "0", "UprcTpCode": "0"}
        out_params =["IsuNo", "IsuNm", "BnsBaseBalQty", "SellPrc", "BuyPrc", "NowPrc", "AvrUprc", "PnlRat", "BalEvalAmt"]
        result = self._execute_query("CSPAQ12300",
                                    "CSPAQ12300InBlock1",
                                    "CSPAQ12300OutBlock3",
                                    *out_params,
                                    **in_params)
        return result


    def order_check(self, order_no=None):
        """TR: t0425 주식 체결/미체결
        :param code:str 종목코드
        :param order_no:str 주문번호
        :return result:dict 주문번호의 체결상태
        """
        in_params = {"accno": self.account, "passwd": self.passwd, "expcode": "", 
                    "chegb":"0", "medosu":"0", "sortgb":"1", "cts_ordno":" "}
        out_params = ["ordno", "expcode", "medosu", "qty", "price", "cheqty", "cheprice", "ordrem", "cfmqty", "status", "orgordno", "ordgb", "ordermtd", "sysprocseq", "hogagb", "price1", "orggb", "singb", "loandt"]
        result_list = self._execute_query("t0425",
                                    "t0425InBlock",
                                    "t0425OutBlock1",
                                    *out_params,
                                    **in_params)
        
        result = {}
        if order_no is not None:
            for item in result_list:
                if item["주문번호"] == order_no:
                    result = item
            return result
        else:
            return result_list

    def order_check2(self, date, code, order_no=None):
        #CSPAQ13700
        print("get_order_check, ", order_no)
        in_params = {"RecCnt":"1", "AcntNo":self.account, "InptPwd":self.passwd, "OrdMktCode":"00", 
                    "BnsTpCode":"0", "IsuNo":code, "ExecYn":"0", "OrdDt":date, "SrtOrdNo2":"0", 
                    "BkseqTpCode":"0", "OrdPtnCode":"00"}

        out_params_3 = ["OrdDt", "OrdMktCode", "OrdNo", "OrgOrdNo", "IsuNo", 
                     "IsuNm", "BnsTpCode", "BnsTpNm", "OrdPtnCode", "OrdPtnNm", 
                     "MrcTpCode", "OrdQty", "OrdPrc", "ExecQty", "ExecPrc", "LastExecTime", 
                     "OrdprcPtnCode", "OrdprcPtnNm", "AllExecQty", "OrdTime"]
        result_list = self._execute_query("CSPAQ13700",
                                    "CSPAQ13700InBlock1",
                                    "CSPAQ13700OutBlock3",
                                    *out_params_3,
                                    **in_params)
        
        result = {}
        print("get_order_check result len", len(result_list))
        if order_no is not None:
            for item in result_list:
                if item["주문번호"] == order_no:
                    result = item
            return result
        else:
            return result_list

    def order_stock(self, code, qty, price, bns_type, order_type="00"):
        """TR: CSPAT00600 현물 정상 주문
        :param bns_type:str 매매타입, 1:매도, 2:매수
        :prarm order_type:str 호가유형, 
            00:지정가, 03:시장가, 05:조건부지정가, 07:최우선지정가
            61:장개시전시간외 종가, 81:시간외종가, 82:시간외단일가
        :return result:dict 주문 관련정보
        """
        in_params = {"AcntNo":self.account, "InptPwd":self.passwd, "IsuNo":code, "OrdQty":qty,
                    "OrdPrc":price, "BnsTpCode":bns_type, "OrdprcPtnCode":order_type, "MgntrnCode":"000",
                    "LoanDt":"", "OrdCndiTpCode":"0"}
        out_params = ["OrdNo", "OrdTime", "OrdMktCode", "OrdPtnCode", "ShtnIsuNo", "MgempNo", "OrdAmt", "SpotOrdQty", "IsuNm"]

        result = self._execute_query("CSPAT00600",
                                    "CSPAT00600InBlock1",
                                    "CSPAT00600OutBlock2",
                                    *out_params,
                                    **in_params)
        return result

    def order_cancel(self, order_no, code, qty):
        """TR: CSPAT00800 현물 취소주문
        :param order_no:str 주문번호
        :param code:str 종목코드
        :param qty:str 취소 수량
        :return result:dict 취소 결과
        """
        in_params = {"OrgOrdNo":order_no,"AcntNo":self.account, "InptPwd":self.passwd, "IsuNo":code, "OrdQty":qty}
        out_params = ["OrdNo", "PrntOrdNo", "OrdTime", "OrdPtnCode", "ShtnIsuNo", "IsuNm"]

        result = self._execute_query("CSPAT00800",
                                    "CSPAT00800InBlock1",
                                    "CSPAT00800OutBlock2",
                                    *out_params,
                                    **in_params)
        return result

    def get_price_n_min_by_code(self, date, code, tick=None):
        """TR: t8412 주식차트(N분) 
        :param code:str 종목코드
        :param date:str 시작시간
        :return result:dict 하루치 분당 가격 정보
        """
        in_params = {"shcode":code,"ncnt":"1", "qrycnt":"500", "nday":"1", "sdate":date, 
                "stime":"090000", "edate":date, "etime":"153000", "cts_date":"00000000", 
                "cts_time":"0000000000", "comp_yn":"N"}
        out_params = ["date", "time", "open", "high", "low", "close", "jdiff_vol", "value"]

        result_list = self._execute_query("t8412",
                                    "t8412InBlock",
                                    "t8412OutBlock1",
                                    *out_params,
                                    **in_params)
        result = {}
        for idx, item in enumerate(result_list):
            result[idx] = item
        if tick is not None:
            return result[tick]
        return result

class Field:

    CSPAQ12300 = {
        "CSPAQ12300OutBlock3":{
            "IsuNo":"종목번호",
            "IsuNm":"종목명",
            "BnsBaseBalQty":"매매기준잔고수량",
            "NowPrc":"현재가",
            "AvrUprc":"평균단가"
        }
    }

    t8412 = {
        "t8412OutBlock1":{
            "date":"날짜",
            "time":"시간",
            "open":"시가",
            "high":"고가",
            "low":"저가",
            "close":"종가",
            "jdiff_vol":"거래량",
            "value":"거래대금",
            "jongchk":"수정구분",
            "rate":"수정비율",
            "sign":"종가등락구분"
        }
    }

        
