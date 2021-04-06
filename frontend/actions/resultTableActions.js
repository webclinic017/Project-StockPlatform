export const resultTable_getData = () => async dispatch => {
  try {
    dispatch({
      type: "AWAITING_RESULTTABLE"
    })

    var resultTableData = []
    console.log("resultTableData", resultTableData)

    // result에서 가져오는 데이터
    const response_results = await fetch("/api/results")
    const data_results = await response_results.json()

    // console.log("result로 부터 온 데이터:", data_results)
    const result_length = data_results.length
    const results_target_data = data_results[result_length - 1]

    const currentAsset = results_target_data.currentAsset //현재 총 자산

    resultTableData["currentAsset"] = currentAsset

    // console.log("resultTableData", resultTableData)

    // resultTableData.push(currentAsset)
    // console.log("resultTableData222222", resultTableData)

    const Final_yield = results_target_data.Final_yield // 최종 수익률
    resultTableData["Final_yield"] = Final_yield

    // strategy에서 가져오는 데이터
    const response_strategy = await fetch("/api/strategy")
    const data_strategy = await response_strategy.json()

    const strategy_length = data_strategy.length

    const strategy_target_data = data_strategy[strategy_length - 1]
    // console.log(strategy_target_data, "dfdfdffffffffffff")

    const investment = strategy_target_data.investment // 투자원금
    // console.log(investment, "!!!!!!!!!!!!!!!!!")
    resultTableData["investment"] = investment
    // console.log("ok")
    // console.log("resultTableData", resultTableData)

    const totalIncome = currentAsset - investment //총 손익
    resultTableData["totalIncome"] = totalIncome

    console.log("resultTableData", resultTableData)

    dispatch({
      type: "SUCCESS_RESULTTABLE",
      payload: {
        resultTableData
      }
    })
  } catch (e) {
    dispatch({
      type: "REJECTED_RESULTTABLE"
    })
  }
}
