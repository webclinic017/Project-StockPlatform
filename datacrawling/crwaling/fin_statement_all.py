# test용
# 로그인을 위한 모듈 추출
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import datetime

import time
from tqdm import tqdm
from tqdm import trange

# input output 파일
inputfile="../txt_file/code_kospi.txt"
outputfile="../json_file/find_state.json"


# 자본잠식률은 제외했음 총 25개
indicator_list_num=[3,2,4,5,6,7,8,9,10,11,12,14,15,16,17,18,19,20,22,23,24,25,27,28,29]
indicator_list_num2=[1,51,81]
indicator_list_num3=[170]

indicator_list=["EPS_connect","EPS_individual","PER","BPS","PBR","CFPS","PCR","SPS","PSR","DPS","Market_odds","ROE","ROS","S/A","A/E","ROA","Net_Profit_Margin","Sales_Operating_Margin","Sales_Growth_Rate","Operating_Profit_Growwth_Rate","Net_Profit_Growth_Rate","Equity_Capital_Growth_Rate","Debt_Ratio","Current_Ratio","Interest_Compensation_Magnification(Times)"]
# http://www.itooza.com/vclub/y10_page.php?cmp_cd=034730&mode=dcy&ss=10&sv=4
indicator_list2=["Operating_Activity_Cash_Flow","Investment_Activity_Cash_Flow","Financial_Activity_Cash_Flow"]
# http://www.itooza.com/vclub/y10_page.php?cmp_cd=034730&mode=dcy&ss=10&sv=2
indicator_list3=["Market_cap"]
# 2020_03~ 2010_03까지 41개  --> sk바이오팜은2011년 6월까지 있음
day_list = ["2020_03","2019_12","2019_09","2019_06","2019_03","2018_12","2018_09","2018_06","2018_03","2017_12","2017_09","2017_06","2017_03","2016_12","2016_09","2016_06","2016_03","2015_12","2015_09","2015_06","2015_03","2014_12","2014_09","2014_06","2014_03","2013_12","2013_09","2013_06","2013_03","2012_12","2012_09","2012_06","2012_03","2011_12","2011_09","2011_06","2011_03","2010_12","2010_09","2010_06","2010_03"]


# 데이터베이스에 넣을 지표
doc_content=""
DAY_LIST_END=40
break_value=0

# 아이디와 비밀번호 지정
USER = "pphm00"
PASS = "00mhpp4321"

def data_refine(doc_content,soup,add,indicator_list,indicator_list_num,day_list):
    manu_value=""
    for i,v in enumerate(indicator_list):
        #print(str(i+1)+"번째 지표 가져오는중\n")
        doc_content+=' , "'+v+'" : {'

        for j,w in enumerate(day_list):
            value=soup.select_one("#node-"+str(indicator_list_num[i]) +" > td:nth-child("+str(j+add)+")")
            # 지표 데이터가 2010_03까지 없으면 다음 종목으로
            if value is not None: 
                value=value.get_text()
            else:
                breakvalue=1
                doc_content+=" }"
                break
            for k in value:
                if k==',': continue
                manu_value+=k
            # N/A일때 예외처리
            if manu_value=="N/A" or manu_value=="N/A":
                manu_value="0"

            if j !=DAY_LIST_END and j!=0:
                doc_content+=" , "+ '"'+ w + '"'+" : "+ manu_value
            elif j==0:
                doc_content+='"'+w + '"' + " : "+ manu_value
            else:
                doc_content+=", " + '"'+ w+ '"'+" : "+ manu_value +" } "
            manu_value=""
    return doc_content

def go_url(url_getinfo):
    res = session.get(url_getinfo)
    res.raise_for_status()
    soup=BeautifulSoup(res.text,"html.parser")
    return soup

def crawling(code,add,soup):
# 재무비율, 가치평가  # node-3 > td:nth-child(1)부터시작
    url_getinfo1 = "http://www.itooza.com/vclub/y10_page.php?ss=10&sv=10&cmp_cd="+code
    soup=go_url(url_getinfo1)
    manu_value=""
    # 데이터정제 시작부분
    doc_content='{ "code" : '+'"'+code+'"'
    doc_content=data_refine(doc_content,soup,add,indicator_list,indicator_list_num,day_list)
        # 재무제표가 3월부터 시작해도 손익계산서와 현금흐름표는 6월부터 나온다.
    add=3
    
    #현금흐름표  # node-3 > td:nth-child(2) 부터시작
    url_getinfo2 = "http://www.itooza.com/vclub/y10_page.php?mode=dcy&ss=10&sv=4&cmp_cd="+code
    soup=go_url(url_getinfo2)
    doc_content=data_refine(doc_content,soup,add,indicator_list2,indicator_list_num2,day_list)
    #add=3
    # 손익계산서  # #node-170 > td:nth-child(2) 
    url_getinfo3 = "http://www.itooza.com/vclub/y10_page.php?mode=dcy&ss=10&sv=2&cmp_cd="+code
    soup=go_url(url_getinfo3)
    doc_content=data_refine(doc_content,soup,add,indicator_list3,indicator_list_num3,day_list)
    doc_content+=" }"+"\n"
    #print(doc_content)
    f2.write(doc_content)

if __name__=="__main__":
    # 세션 시작 --- (※2)
    session = requests.session()
    # 로그인 --- (※3)
    login_info = {
        "txtUserId": USER,  # 아이디 지정
        "txtPassword": PASS  # 비밀번호 지정
    }
    url_login = "https://login.itooza.com/login_process.php?data="
    res = session.post(url_login, data=login_info)
    res.raise_for_status() # 오류가 발생하면 예외가 발생
    now = datetime.datetime.now()
    #print(now)

    f = open(inputfile, 'r')
    f2 = open(outputfile, 'w')

    lines = f.readlines()
    for line in tqdm(lines):
        code=line[:-1]
        url_getinfo1 = "http://www.itooza.com/vclub/y10_page.php?ss=10&sv=10&cmp_cd="+code
        soup=go_url(url_getinfo1)

        # 에러떠서 check_date도 is not None을 넣었다.
        check_date=soup.select_one('#y10_tb_1 > thead > tr > th:nth-child(1) > span')
        if soup.select_one("#node-3 > td:nth-child(1)") is not None and check_date is not None:
            check_date=check_date.get_text()
            #2019.12의 데이터부터 데이터 가져옴 (2020.06 인것도 있고 2020.03부터 인것도 있어서 2020.03부터로 통일, 둘다 아니라면 버림 )
            if check_date=="2020.06":
                add=2
                crawling(code,add,soup)
            elif check_date=="2020.03":
                add=1
                crawling(code,add,soup)

    f.close()
    f2.close()
    now = datetime.datetime.now()
    #print(now)