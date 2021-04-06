export const stocks_getData = () => async dispatch => {
  try {
    dispatch({
      type: "AWAITING_STOCKS"
    })

    const response = await fetch("/api/stocks")
    const data = await response.json()

    console.log("selected_companys", data.selected_companys)
    const selected_companys = data.selected_companys
    console.log(typeof selected_companys) //string

    var selectedObj = eval("(" + selected_companys + ")") //object

    const selected_companys_data = selectedObj["0"]

    const stocks_data = []
    console.log("selected_companys_data", selected_companys_data)

    stocks_data.push(selected_companys_data)

    dispatch({
      type: "SUCCESS_STOCKS",
      payload: {
        stocks_data
      }
    })
  } catch (e) {
    dispatch({
      type: "REJECTED_STOCKS"
    })
  }
}
