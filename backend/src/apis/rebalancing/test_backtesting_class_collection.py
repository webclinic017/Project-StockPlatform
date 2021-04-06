# 사용하기 편하기 위해 만든 class  
# 객체 f
class Init_data:
    def __init__(self):
        self.test=0
        self.is_buy = []                                                # 구매했는지 구매 안했는지 확인하는 변수
        self.buy_count = []                                             # 가지고 있는 주식수
        self.enterprise_list=[]                                         # 기업 리스트
        self.rebalancing_date_list=[]                                   # 리벨런싱 지표에 따라 저장할 날짜 ex 2019_12 2019_09 형식으로 저장됨
        self.int_rebalancing_date_list=[]
        self.code_date_clasifyed_list=[]                                # 분류된 데이터
        self.partition_invertment_principal = []
        self.investment_principal=0
        self.rebalancing_index=1
        self.check_win_lose_price=0


# 유저 입력 데이터 
# 객체 user_input
# 주의점 : backtesting 가능한 date 데이터 범위 : 20110101~ 20200101
class User_input_data:
    def __init_(self):
        self.INDICATOR_NUM= 0                                           # 선택할 지표 수
        self.INDICATOR_LIST=[]                                          # 지표 리스트
        self.INDICATOR_MIN_LIST = []                                    # 지표별 최솟값
        self.INDICATOR_MAX_LIST = []                                    # 지표별 최댓값
        self.INVESTMENT_PRINCIPAL_COPY = 0   # 초기 자본
        self.DATE_START= 0                                              # 백테스팅 시작 날짜
        self.DATE_END= 0                                                # 백테스팅 종료 날짜
        self.THE_NUMBER_OF_MAXIMUM_EVENT= 2                             # 최대 선택 종목 수
        self.BUYING_CONDITION= 1                                        # 매수 조건
        self.sales_profit = 1                                           # 매도조건1 익절
        self.sales_loss = 1                                             # 매도조건2 손절
        self.REBALANCING = ""                                           # 리벨런싱 지표
        print("세팅을 하려면 indicator_list 3개, indicator_min 3개, indicator_max 3개, 투자원금, ")

#   조건1. 지표조건
    def set_indicator_data(self,INDICATOR_LIST=[],INDICATOR_MIN_LIST = [],INDICATOR_MAX_LIST = []):
        self.INDICATOR_NUM = 3
        self.INDICATOR_LIST=[]
        for indicator in INDICATOR_LIST:
            self.INDICATOR_LIST.append(indicator)
        self.INDICATOR_MIN_LIST=[]
        for min_value in INDICATOR_MIN_LIST:
            self.INDICATOR_MIN_LIST.append(min_value)
        self.INDICATOR_MAX_LIST=[]
        for max_value in INDICATOR_MAX_LIST:
            self.INDICATOR_MAX_LIST.append(max_value)
#   조건2. 초기 자본, 백테스팅 시작, 백테스팅 끝 날짜
    def set_basic_data(self,investment_principal=1000000,DATE_START=20140101,DATE_END=20180701,THE_NUMBER_OF_MAXIMUM_EVENT=4):
        self.INVESTMENT_PRINCIPAL_COPY = investment_principal           # 초기 자본
        self.DATE_START = DATE_START                    # 백테스팅 시작 날짜
        self.DATE_END = DATE_END                      # 백테스팅 종료 날짜
        self.THE_NUMBER_OF_MAXIMUM_EVENT = THE_NUMBER_OF_MAXIMUM_EVENT          # 최대 선택 종목 수
#   조건3. 사는 조건, 파는 조건, 리벨런싱 주기
    def set_backtesting_data(self,BUYING_CONDITION=0.8,sales_profit=1.2,sales_loss=0.7,REBALANCING="2"):
        self.BUYING_CONDITION= BUYING_CONDITION                   # 매수 조건
        self.sales_profit = BUYING_CONDITION * sales_profit   # 매도조건1 익절
        self.sales_loss = BUYING_CONDITION * sales_loss    # 매도조건2 손절
        self.REBALANCING = str(REBALANCING)                      # 리벨런싱 지표

# 임의의 전략 1
    # def strategy1(self):
    #     self.INDICATOR_NUM=3
    #     self.INDICATOR_LIST=["PER","PBR","ROE"]
    #     self.INDICATOR_MIN_LIST = ['1','1','10']
    #     self.INDICATOR_MAX_LIST = ["10","10","100"]
    #     self.INVESTMENT_PRINCIPAL_COPY = self.investment_principal=1000000
    #     self.DATE_START=20110101
    #     self.DATE_END=20190101
    #     self.THE_NUMBER_OF_MAXIMUM_EVENT=4
    #     self.BUYING_CONDITION=0.9
    #     self.sales_profit = self.BUYING_CONDITION* 1.2
    #     self.sales_loss = self.BUYING_CONDITION * 0.6
    #     self.REBALANCING = "2"

# 객체 trade
class Stock_trading_indicator:
    def __init__(self):
        self.buing_price=0
        self.sales_profit_price=0
        self.sales_loss_price=0

# 결과 class
# 객체 
class Result:
   def __init__(self,writer_id_input=0):
        self.strategy_number=0                  # 전략 번호
        self.writer_id=writer_id_input          # 유저 이름
        # result value
        self.profit_all =0                      # 최종 수익
        self.currentAsset =0                    # 현재 자산
        self.cagr = 0                           # 누적 수익률
        self.quarter_cagr =[]                   # 분기별 수익률
        # 승률
        self.win = 0                            # 이익을 보고 판 횟수
        self.lose = 0                           # 손해를 보고 판 횟수
        # 일별 자산
        self.Assets_by_date_list=[]             # 일별 자산 list
        self.Reavalanced_code_name_dic={}       # 리벨런싱한 기업을 저장하는 dictionary
        self.Reavalanced_code_name_dic_index=0  # 리벨런싱한 기업 index
# 로깅 만드는 함수
# 객체 l
class Loging:
    def __init__(self):
        self.routine=0
        self.date_index=0
        self.saved_k=9999

