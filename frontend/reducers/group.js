export const initialState = {
  strategyName: "test_strategy_front_2",
  strategyNumber: "12311",
  writerName: 1,
  strategyDescription: "front_api_test",

  investment: "0",
  investment_Start: "0",
  investment_End: "0",
  maxStockNumber: 5,
  userMarketCap: "0",

  userROE: 0,
  userROA: 0,
  userSalesPerProfit: 0,
  userSalesPerMargin: 0,
  userSalesIncrese: 0,
  userMarginIncrease: 0,
  userProfitIncrease: 0,
  userDebtRatio: 0,
  userCurrentRatio: 0,
  userOperatingActivityCashFlow: 0,
  userInvestmentActivityCashFlow: 0,
  userFinancialActivityCashFlow: 0,

  userEPS_Start: 0,
  userEPS_End: 0,
  userBPS_Start: 0,
  userBPS_End: 0,
  userCFPS_Start: 0,
  userCFPS_End: 0,
  userSPS_Start: 0,
  userSPS_End: 0,
  userDPS_Start: 0,
  userDPS_End: 0,

  userPER_Start: 0,
  userPER_End: 0,
  userPBR_Start: 0,
  userPBR_End: 0,
  userPCR_Start: 0,
  userPCR_End: 0,
  userPSR_Start: 0,
  userPSR_End: 0,
  userMarketDiviend_Start: 0,
  userMarketDiviend_End: 0,

  purchaseCondition: 0,
  targetPrice: 0,
  sellPrice: 0,
  revalancingPeriod: 0
}

export const ADD_PARAMETERS = "ADD_PARAMETERS"

export const addParametersAction = data => {
  return {
    type: ADD_PARAMETERS,
    data
  }
}

const groupReducer = (state = initialState, action) => {
  const { type, data } = action

  switch (type) {
    case ADD_PARAMETERS: {
      return {
        ...state,
        strategyNumber: data.strategyNumber,
        investment: data.investment,
        investment_Start: data.investment_Start,
        investment_End: data.investment_End,
        maxStockNumber: data.maxStockNumber,
        userMarketCap: data.userMarketCap,

        userROE: data.userROE,
        userROA: data.userROA,
        userSalesPerProfit: data.userSalesPerProfit,
        userSalesPerMargin: data.userSalesPerMargin,
        userSalesIncrese: data.userSalesIncrese,
        userMarginIncrease: data.userMarginIncrease,
        userProfitIncrease: data.userProfitIncrease,
        userDebtRatio: data.userDebtRatio,
        userCurrentRatio: data.userCurrentRatio,
        userOperatingActivityCashFlow: data.userOperatingActivityCashFlow,
        userInvestmentActivityCashFlow: data.userInvestmentActivityCashFlow,
        userFinancialActivityCashFlow: data.userFinancialActivityCashFlow,

        userEPS_Start: data.userEPS_Start,
        userEPS_End: data.userEPS_End,
        userBPS_Start: data.userBPS_Start,
        userBPS_End: data.userBPS_End,
        userCFPS_Start: data.userCFPS_Start,
        userCFPS_End: data.userCFPS_End,
        userSPS_Start: data.userSPS_Start,
        userSPS_End: data.userSPS_End,
        userDPS_Start: data.userDPS_Start,
        userDPS_End: data.userDPS_End,

        userPER_Start: data.userPER_Start,
        userPER_End: data.userPER_End,
        userPBR_Start: data.userPBR_Start,
        userPBR_End: data.userPBR_End,
        userPCR_Start: data.userPCR_Start,
        userPCR_End: data.userPCR_End,
        userPSR_Start: data.userPSR_Start,
        userPSR_End: data.userPSR_End,
        userMarketDiviend_Start: data.userMarketDiviend_Start,
        userMarketDiviend_End: data.userMarketDiviend_End,

        purchaseCondition: data.purchaseCondition,
        targetPrice: data.targetPrice,
        sellPrice: data.sellPrice,
        revalancingPeriod: data.revalancingPeriod
      }
    }

    default: {
      return {
        ...state
      }
    }
  }
}

export default groupReducer
