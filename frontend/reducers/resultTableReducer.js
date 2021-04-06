const initialState = {
  loading: false,
  result_table: [
    { investment: 0, currentAsset: 0, totalIncome: 0, Final_yield: 0 }
  ]
}

const resultTableReducer = (state = initialState, action) => {
  const { type, payload } = action
  // console.log(type)
  // console.log(payload)

  switch (type) {
    case "AWAITING_RESULTTABLE":
      console.log("awaiting result_table")
      return {
        ...state,
        loading: true
      }
    case "REJECTED_RESULTTABLE":
      return {
        ...state,
        loading: false
      }
    case "SUCCESS_RESULTTABLE":
      return {
        ...state,
        loading: false,
        result_table: payload.resultTableData
      }
    default:
      return {
        ...state
      }
  }
}

export default resultTableReducer
