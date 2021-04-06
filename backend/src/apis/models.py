from djongo import models
import json

class User(models.Model):

    objects = models.Manager()
    username = models.CharField(max_length=32, verbose_name="사용자명", unique=True)
    password = models.CharField(max_length=32, verbose_name="비밀번호")
    registered_dttm = models.DateTimeField(auto_now_add=True, verbose_name="등록시간")

    def __str__(self):
        return self.username

    class Meta:
        db_table = "Users"
        verbose_name = "user"
        verbose_name_plural ="Users"


class Strategy(models.Model):
    objects = models.Manager()
    # 기본 항목
    strategyName = models.CharField(max_length=128, verbose_name="전략명")
    strategyNumber = models.IntegerField(verbose_name="전략고유번호", unique=True)
    writerName = models.ForeignKey('User', on_delete=models.CASCADE, verbose_name="전략작성자명")
    strategyDescription = models.TextField(verbose_name="전략설명")
    strategyStar = models.IntegerField(verbose_name="별점")
        
    # Tab1 기본 항목
    investment = models.IntegerField(verbose_name="투자원금")
    investment_Start = models.IntegerField(verbose_name="투자 시작일")
    investment_End = models.IntegerField(verbose_name="투자 마감일")
    maxStockNumber = models.IntegerField(verbose_name="최대 보유 종목수")
    userMarketCap = models.IntegerField(verbose_name="대상기업 최소시가총액")

    # Tab2 퀄리티 지표
    userROE = models.IntegerField(verbose_name="최저 ROE", blank=True)
    userROA = models.IntegerField(verbose_name="최저 ROA", blank=True)
    userSalesPerProfit = models.IntegerField(verbose_name="매출액대비 순이익률", blank=True)
    userSalesPerMargin = models.IntegerField(verbose_name="매출액 대비 영업이익률", blank=True)
    userSalesIncrese = models.IntegerField(verbose_name="매출액 증가율", blank=True)
    userMarginIncrease = models.IntegerField(verbose_name="영업이익 증가율", blank=True)
    userProfitIncrease = models.IntegerField(verbose_name="순이익 증가율", blank=True)
    userDebtRatio = models.IntegerField(verbose_name="부채비율", blank=True)
    userCurrentRatio = models.IntegerField(verbose_name="유동비율", blank=True)
    userOperatingActivityCashFlow = models.BooleanField(verbose_name="영업활동현금흐름", blank=True)
    userInvestmentActivityCashFlow = models.BooleanField(verbose_name="투자활동현금흐름", blank=True)
    userFinancialActivityCashFlow = models.BooleanField(verbose_name="재무활동현금흐름", blank=True)
    # Tab3 벨류 지표

    # 주당 가치평가 지표
    userEPS_Start = models.IntegerField(verbose_name="주당순이익(min)", blank=True)
    userEPS_End = models.IntegerField(verbose_name="주당순이익(max)", blank=True)
    userBPS_Start = models.IntegerField(verbose_name="주당순자산(min)", blank=True)
    userBPS_End = models.IntegerField(verbose_name="주당순자산(max)", blank=True)
    userCFPS_Start = models.IntegerField(verbose_name="주당현금흐름(min)", blank=True)
    userCFPS_End = models.IntegerField(verbose_name="주당현금흐름(max)", blank=True)
    userSPS_Start = models.IntegerField(verbose_name="주당매출액(min)", blank=True)
    userSPS_End = models.IntegerField(verbose_name="주당매출액(max)", blank=True)
    userDPS_Start = models.IntegerField(verbose_name="주당배당금(min)", blank=True)
    userDPS_End = models.IntegerField(verbose_name="주당배당금(max)", blank=True)

    # 주가 가치평가 지표
    userPER_Start = models.IntegerField(verbose_name="주가수익배수(min)", blank=True)
    userPER_End = models.IntegerField(verbose_name="주가수익배수(max)", blank=True)
    userPBR_Start = models.IntegerField(verbose_name="주가순자산배수(min)", blank=True)
    userPBR_End = models.IntegerField(verbose_name="주가순자산배수(max)", blank=True)
    userPCR_Start = models.IntegerField(verbose_name="주가현금흐름배수(min)", blank=True)
    userPCR_End = models.IntegerField(verbose_name="주가현금흐름배수(max)", blank=True)
    userPSR_Start = models.IntegerField(verbose_name="주가매출액배수(min)", blank=True)
    userPSR_End = models.IntegerField(verbose_name="주가매출액배수(max)", blank=True)
    userMarketDiviend_Start = models.IntegerField(verbose_name="시가 배당률(min)", blank=True)
    userMarketDiviend_End = models.IntegerField(verbose_name="시가 배당률(max)", blank=True)

    # Tab4 매수 & 매도 조건
    purchaseCondition = models.IntegerField(verbose_name="매수조건(%)")
    targetPrice = models.IntegerField(verbose_name="목표가격")
    sellPrice = models.IntegerField(verbose_name="손절가격")
    revalancingPeriod = models.IntegerField(verbose_name="리벨런싱 주기 ( 0:분기별 | 1:연간 | 2:선택안함 )")

    # 추가 데이터들 ( 전략들의 현재상태 )
    strategyOpenedInPlatform = models.BooleanField(verbose_name="플랫폼에 오픈하기", blank=True)
    
    def __str__(self):
        return self.strategyName

    class Meta:
        db_table = "Strategy"
        verbose_name = "Strategy"
        verbose_name_plural ="Strategy"


class Result(models.Model):
    
    objects = models.Manager()
    # 기본 항목
    strategy_result = models.OneToOneField('Strategy', to_field="strategyNumber", on_delete=models.CASCADE, verbose_name="전략 고유번호당 결과")
    writer_name = models.ForeignKey('User',to_field="username", on_delete=models.CASCADE, verbose_name="전략 작성자명")

    # 결과 항목
    profit_all = models.IntegerField(verbose_name="총 손익")
    currentAsset = models.IntegerField(verbose_name="현재자산")
    Final_yield = models.IntegerField(verbose_name="최종수익률") 
    #m_cagr = models.IntegerField(verbose_name="월간수익률")

    # 선택된 종목들 리스트
    selected_companys = models.CharField(max_length=1024, verbose_name="선택된 종목 리스트") 
    # 추가된 항목들
    Current_assets_by_date = models.TextField(verbose_name="날짜별 현재 자산 정보", blank=True)
    Winning_rate = models.TextField(verbose_name="승률 (익절한 횟수와 손절한 횟수 정보)", blank=True)
    Reavalanced_code_name_list = models.TextField(verbose_name="리벨런싱한 종목 ( n번째 리벨런싱에 따른 종목 )", blank=True)


    def set_selected_companys(self, x):
        self.selected_companys = json.dumps(x)

    def get_selected_companys(self):
        return json.loads(self.selected_companys)

    def __str__(self):
        return str(self.strategy_result)

    class Meta:
        db_table = "Results"
        verbose_name = "result"
        verbose_name_plural ="Results"




