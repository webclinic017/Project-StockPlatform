const initalState = {
  loading: false,
  data: {
    labels: ["Win", "Lose"],
    datasets: [
      {
        data: [5, 5],
        backgroundColor: ["#FF7031", "#224ABA"],
        borderColor: ["#FF7031", "#224ABA"],
        hoverBackgroundColor: ["#FF7031", "#224ABA"]
      }
    ]
  }
}

const winRateReducer = (state = initalState, action) => {
  const { type, payload } = action

  switch (type) {
    case "AWAITING_WINRATE":
      return {
        ...state,
        loading: true
      }
    case "REJECTED_WINRATE":
      return {
        ...state,
        loading: false
      }
    case "SUCCESS_WINRATE":
      console.log("success실행됨")
      return {
        ...state,
        loading: false,
        data: {
          labels: ["Win", "Lose"],
          datasets: [
            {
              data: payload.winRate_data,
              backgroundColor: ["#FF7031", "#224ABA"],
              borderColor: ["#FF7031", "#224ABA"],
              hoverBackgroundColor: ["#FF7031", "#224ABA"]
            }
          ]
        }
      }
    default:
      return state
  }
  return state
}

export default winRateReducer
