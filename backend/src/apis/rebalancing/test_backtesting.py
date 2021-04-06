# pymongo 사용 모듈 추출
import pymongo
import json

#from test_backtesting_class_collection import Init_data, User_input_data, Stock_trading_indicator, Result
# Function1 : rebalancing_date_data
# 함수 설명 : 리벨런싱하는 주기별 날짜 데이터 가공 및 반환
# clear
def rebalancing_date_data(f,user_input):
    start_data_year = user_input.DATE_START//10000
    start_data_month = user_input.DATE_START%10000
    if start_data_month<301:
        start_data_month="12"
        start_data_year=start_data_year-1
    elif start_data_month<601:
        start_data_month="03"
    elif start_data_month<901:
        start_data_month="06"
    elif start_data_month<1201:
        start_data_month="09"
    start_data_int=int(str(start_data_year)+start_data_month)
    start_data=str(start_data_year)+"_"+start_data_month
    f.rebalancing_date_list.append(start_data)
    YEAR_LIST= [20100000,20110000,20120000,20130000,20140000,20150000,20160000,20170000,20180000,20190000,20200000]
    MONTH_LIST=[301,601,901,1201]
    # 분기별 데이터 가공
    temp=""
    temp2= 0
    print(user_input.DATE_START)
    print(user_input.DATE_END)
    if user_input.REBALANCING=="0":
        for i in YEAR_LIST:
            for j in MONTH_LIST:
                if user_input.DATE_START<=i+j and i+j<=user_input.DATE_END:
                    if j!=1201:
                        temp=str(i//10000)+"_"+"0"+str(j//100)
                        f.rebalancing_date_list.append(temp)
                    else :
                        temp=str(i//10000)+"_"+str(j//100)
                        f.rebalancing_date_list.append(temp)
    # 1년 주기별 데이터 가공
    elif user_input.REBALANCING=="1":
        for i in YEAR_LIST:
            if user_input.DATE_START//10000<=i//10000 and i//10000<user_input.DATE_END//10000:
                temp = str(i//10000)+"_"+start_data_month
                temp2 = i+int(start_data_month)*100
                f.rebalancing_date_list.append(temp)
    f.rebalancing_date_list.append(temp) 
    f.rebalancing_date_list.append(temp) 
    f.rebalancing_date_list.append(temp) 
    f.rebalancing_date_list.append(temp) 
    f.rebalancing_date_list.append(temp) 
    
    #print(f.rebalancing_date_list)

# Function2 : search_rebalanced_enterprise
# explain : 리벨런싱할때 바꿔주는 기업 코드를 리턴하는 함수 
def search_rebalanced_enterprise(db,f,user_input,r,j):
    start_data=""
    f.enterprise_list=[]
    #print("f.rebalancing_date_list : "+f.rebalancing_date_list[j])              # 여기에서 문제가 발생
    start_data=f.rebalancing_date_list[j]
    for i,indicator in enumerate(user_input.INDICATOR_LIST):
        user_input.INDICATOR_LIST[i]=user_input.INDICATOR_LIST[i]+"."+start_data
    print('MongoDB Connected.')
    # 여러개 받을 수 있는 코드
    mk_find_dic="{ \"$and\":["
    for i in range(len(user_input.INDICATOR_LIST)):
        mk_find_dic +="{ \""+user_input.INDICATOR_LIST[i]+"\" : { \"$gte\" : "+str(int(user_input.INDICATOR_MIN_LIST[i])/100)+ "  , \"$lte\": "+str(int(user_input.INDICATOR_MAX_LIST[i])/100)+"}"+"}"
        if i!=len(user_input.INDICATOR_LIST)-1:
            mk_find_dic += " , "
        else:
            mk_find_dic +="] }"
    json_find_dic=json.loads(mk_find_dic)
    #print(json_find_dic)
    r.Reavalanced_code_name_dic[str(r.Reavalanced_code_name_dic_index)]=[]
    for doc in db.stock_parameters.find(json_find_dic,{"_id":False,"code":True}).sort([("Market_cap",-1)]).limit(user_input.THE_NUMBER_OF_MAXIMUM_EVENT):
        f.enterprise_list.append(doc["code"])
        r.Reavalanced_code_name_dic[str(r.Reavalanced_code_name_dic_index)].append(doc["code"])

    r.Reavalanced_code_name_dic_index+=1    
    for i,indicator in enumerate(user_input.INDICATOR_LIST):
        user_input.INDICATOR_LIST[i]=user_input.INDICATOR_LIST[i][:-8]
    #print(f.enterprise_list)

# Function3 : make_code_date_clasifyed_list
# explain : 리벨런싱한 기업의 데이터를 리벨런싱 주기별로 바꿔줄 때 사용
# 여기서 문제점은 분기별이 함수가 실행되는데, 리벨런싱 할때마다 전체 데이터를 저장하는 것이다. 그래서 이를
# 리벨런싱 분기만큼의 데이터만 저장하게 해야한다. 나중에 갈아엎자
# 또 리벨런싱지표와 date범위를 알았으면 맨 처음에 리벨런싱을 미리 다 해놓고, 기업을 뽑아놓은 다음 그 기업의 데이터를 미리 받아온다.
def make_code_date_clasifyed_list(db,f,user_input,r):
    
    date_change=user_input.DATE_START
    REBALANCING_YEAR_GAP=10000
    REBALANCING_QUARTER_GAP=300
    times=0
    f.code_date_clasifyed_list=[]
    for k in range(0,user_input.THE_NUMBER_OF_MAXIMUM_EVENT+1):
        f.code_date_clasifyed_list.append([])
    for k in range(0,user_input.THE_NUMBER_OF_MAXIMUM_EVENT):
        code1= f.enterprise_list[k]
        date_change=user_input.DATE_START
        for i in range(len(f.rebalancing_date_list)+1):      # 이건 문제가 아님
            f.code_date_clasifyed_list[k].append([])
        times=0
        f.test+=1
        log1=0
        for i in db.stock_priceInfo.find({"code":code1}):
            for j in i['data']:
                # 범위별로 저장하기 위한 코드
                if j['Date']>=user_input.DATE_START and j['Date']<=user_input.DATE_END:
                    if f.test==1:
                        #print("asset log1 : "+str(log1))
                        log1+=1
                        r.Assets_by_date_list.append({"Date":j["Date"],"Asset":0})
                    #분기별 리벨런싱
                    if user_input.REBALANCING=="0" and (j['Date']-date_change>=REBALANCING_QUARTER_GAP):      # 여기가 문제
                        date_change = j['Date'] 
                        times=times+1
                    #연도별 리벨런싱
                    elif user_input.REBALANCING=="1"and (j['Date']-date_change>=REBALANCING_YEAR_GAP):
                        date_change=j['Date'] # date_change + REBALANCING_YEAR_GAP
                        times=times+1
                    f.code_date_clasifyed_list[k][times].append({"Date" : j["Date"], "Close":j["Close"]})
    
        
    times+=1
    return times

# Function4 : init_list_condiiton(f,user_input)
# Explain : make list space
def init_list_condiiton(f,user_input):
    for i in range(0,user_input.THE_NUMBER_OF_MAXIMUM_EVENT+1):
        f.is_buy.append(0)
        f.buy_count.append(0)

# Function5 : set_buy_sell_price(user_input,close_price,j)
# Expalin : set buy sell price
def set_buy_sell_price(f,user_input,trade,k,j):
    close_price=0
    for data in f.code_date_clasifyed_list[k][j]:
        close_price=float(data['Close'])              #이거 데이터 순서가 날짜 정방향 순서대로인지 확인해야함
        '''
        print("========================revalancing========================")
        print("change : close price :"+ str(data['Close']) )
        '''
        break
    trade.buying_price = close_price * user_input.BUYING_CONDITION    # 매수 조건
    trade.sales_profit_price = close_price * float(user_input.sales_profit)  # 익절가격
    trade.sales_loss_price = close_price * float(user_input.sales_loss)      # 손절 가격
    '''
    print("revalancing try : " + str(j))
    print("buying_price : "+ str(trade.buying_price))
    print("sales_profit_price : "+ str(trade.sales_profit_price))
    print("sales_loss_price : "+ str(trade.sales_loss_price))
    '''

# Function6 : buying_stock(f,user_input,data,partition_invertment_principal,k,sales_profit_price,sales_loss_price)
# Explain : selling stock
def buying_stock(f,user_input,trade,data,k):
    f.buy_count[k] = f.partition_invertment_principal[k] // trade.buying_price
    f.partition_invertment_principal[k]-= f.buy_count[k]*trade.buying_price
    '''
    print("========================buy=============================")
    print("1. date : "+str(data['Date']))
    print("2. f.buy_count : "+str(f.buy_count[k]))
    print("3. buying_price : "+ str(data["Close"]))
    print("4. buy after rest_investment_principal : "+str(f.partition_invertment_principal[k]))
    '''
    trade.sales_profit_price = trade.buying_price * float(user_input.sales_profit)  # 익절가격
    trade.sales_loss_price = trade.buying_price * float(user_input.sales_loss)      # 손절 가격
    f.check_win_lose_price=trade.buying_price
    f.is_buy[k]=1

# Function7 : selling_stock(f,user_input,data,partition_invertment_principal,k,buying_price)
# Explain : selling stock
def selling_stock_profit(f,user_input,trade,r,data,k):
    f.partition_invertment_principal[k] += f.buy_count[k]*trade.sales_profit_price
    '''
    print("========================sell=============================")
    print("1. date : "+str(data['Date']))
    print("2. sell_count : "+str(f.buy_count[k]))
    print("3. sell_price : "+ str(data["Close"]))
    print("4. sell after rest_investment_principal : "+str(f.partition_invertment_principal[k]))
    '''
    trade.buying_price = trade.sales_profit_price * user_input.BUYING_CONDITION    # 매수 조건
    f.buy_count[k]=0
    f.is_buy[k]=0
    r.win+=1

def selling_stock_loss(f,user_input,trade,r,data,k):
    f.partition_invertment_principal[k] += f.buy_count[k]*trade.sales_loss_price
    '''
    print("========================sell=============================")
    print("1. date : "+str(data['Date']))
    print("2. sell_count : "+str(f.buy_count[k]))
    print("3. sell_price : "+ str(data["Close"]))
    print("4. sell after rest_investment_principal : "+str(f.partition_invertment_principal[k]))
    '''
    trade.buying_price = trade.sales_loss_price* user_input.BUYING_CONDITION    # 매수 조건
    f.buy_count[k]=0
    f.is_buy[k]=0
    r.lose+=1

# Function8 : lastday_sell_all(f,user_input,)
def lastday_sell_all(f,user_input,r,k,data):
    f.partition_invertment_principal[k] += f.buy_count[k]*data["Close"]
    
    if f.is_buy[k]==1:
        if f.check_win_lose_price > data["Close"]:
            r.lose+=1
        else:
            r.win+=1
    
    '''
    print("====================last day, sell all============================")
    print("1. date : "+str(data['Date']))
    print("2. sell_count : "+str(f.buy_count[k]))
    print("3. lastday close_price : "+ str(data["Close"]))
    print("4. sell after rest_investment_principal : "+str(f.partition_invertment_principal[k]))
    '''
    f.buy_count[k]=0
    f.is_buy[k]=0
    f.investment_principal+=f.partition_invertment_principal[k]
    f.partition_invertment_principal[k]=0

# Function9 : set_result(r,user_input)
# Parameter :
# 1) r : Result Class`s object
# 2) user_input : User_input_data Class`s object
def set_result(f,user_input,r):
    r.profit_all = int(f.investment_principal - user_input.INVESTMENT_PRINCIPAL_COPY)
    r.currentAsset = int(f.investment_principal)
    r.cagr= int(r.profit_all/user_input.INVESTMENT_PRINCIPAL_COPY * 100)


def current_investment_asset(f,data,k):
    return int(data["Close"] * f.buy_count[k] + f.partition_invertment_principal[k])

# 로그 만드는 함수 
# clear
def loging(f,user_input,r,l,data,k):
    if l.saved_k!=k:
        l.date_index=l.routine
        l.saved_k=k
    #print("l.date_index : "+str(l.date_index))
    r.Assets_by_date_list[l.date_index]["Asset"]+=current_investment_asset(f,data,k)
    l.date_index+=1
    if k==(user_input.THE_NUMBER_OF_MAXIMUM_EVENT-1):
        l.routine= l.routine + 1


# function10 :    
def backtesting(initData,userInputData,stockTradingIndicator,result,log):
    # 초기 CLASS 세팅
    f = initData
    user_input=userInputData
    trade = stockTradingIndicator
    l=log
    r = result
    count=0                          # 리벨런싱 횟수 정해주는 변수
    f.investment_principal = user_input.INVESTMENT_PRINCIPAL_COPY
    client = pymongo.MongoClient("mongodb+srv://admin:admin@cluster0.kjrlb.mongodb.net/<pnu_sgm_stockdata>?retryWrites=true&w=majority")    # 파이몽고 사용해서
    db = client.pnu_sgm_stockdata
    # init setting
    rebalancing_date_data(f,user_input)
    init_list_condiiton(f,user_input)
    search_rebalanced_enterprise(db,f,user_input,r,0)
    count=make_code_date_clasifyed_list(db,f,user_input,r)
    #r.Assets_by_date_list.append({"Date":0,"Asset":0})
    count2=count
    # count2 = 리벨런싱한 총 횟수 + 1
    for j in range(0,count2):
        if j!=0:
            search_rebalanced_enterprise(db,f,user_input,r,j)
            count=make_code_date_clasifyed_list(db,f,user_input,r)
        f.partition_invertment_principal=[]
        for ttt in range(user_input.THE_NUMBER_OF_MAXIMUM_EVENT):
            f.partition_invertment_principal.append(f.investment_principal//user_input.THE_NUMBER_OF_MAXIMUM_EVENT)
        f.investment_principal-=f.partition_invertment_principal[0]*user_input.THE_NUMBER_OF_MAXIMUM_EVENT
        for k in range(0,user_input.THE_NUMBER_OF_MAXIMUM_EVENT):
            #print("change enterprise")
            #print("code : "+ f.enterprise_list[k])
            set_buy_sell_price(f,user_input,trade,k,j)
            for i, data in enumerate(f.code_date_clasifyed_list[k][j]):
                # 매수 조건
                if f.is_buy[k]==0:
                    if data["Close"]<=int(trade.buying_price):
                        buying_stock(f,user_input,trade,data,k)
                # 매도 조건
                elif f.is_buy[k]==1:
                    # 익절
                    if data["Close"]>=trade.sales_profit_price:
                        selling_stock_profit(f,user_input,trade,r,data,k)
                    # 손절
                    elif data["Close"] <= trade.sales_loss_price:
                        selling_stock_loss(f,user_input,trade,r,data,k)
                loging(f,user_input,r,l,data,k)
            # 리벨런싱 전에는 가지고 있는 주식을 다 판다.
                if i==len(f.code_date_clasifyed_list[k][j])-1:
                    lastday_sell_all(f,user_input,r,k,data)
    #print("##########################################")

    #print(r.Assets_by_date_list)
    set_result(f,user_input,r)


    #print("profit_all   : " + str(r.profit_all))
    #print("currentAsset : " +str(r.currentAsset))
    #print("cagr         : " + str(r.cagr)+" %")

    #print("##########################################")
    # r.Assets_by_date_list에 dic list형식으로 날짜와 날짜별 자산이 저장됨
    #print("r.Reavalanced_code_name_dic : ")
    #print(r.Reavalanced_code_name_dic)

    #print("##########################################")
    #print(str(r.Assets_by_date_list))
    #print("win : "+str(r.win))
    #print("lose : "+str(r.lose))
    
    return r
