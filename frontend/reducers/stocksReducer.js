const initialState = {
  loading: false,
  stocks: []
}

const stocksReducer = (state = initialState, action) => {
  const { type, payload } = action
  console.log(type)
  console.log(payload)

  switch (type) {
    case "AWAITING_STOCKS":
      console.log("awaiting stocks")
      return {
        ...state,
        loading: true
      }
    case "REJECTED_STOCKS":
      return {
        ...state,
        loading: false
      }
    case "SUCCESS_STOCKS":
      return {
        ...state,
        loading: false,
        stocks: payload.stocks_data
      }
    default:
      return {
        ...state
      }
  }
}

export default stocksReducer
