const initalState = {
  loading: false,
  data: {
    labels: [],
    datasets: [
      {
        label: "Kospi Yield",
        data: [],
        fill: false,
        backgroundColor: "#3B75DB",
        borderColor: "#3B75DB",
        pointBorderColor: "#3B75DB",
        pointRadius: 0.3
      },
      {
        label: "Algorithm Yield",
        data: [],
        fill: false,
        backgroundColor: "#FF7031",
        borderColor: "#FF7031",
        pointBorderColor: "#FF7031",
        pointRadius: 0.3
      }
    ]
  },
  options: {
    responsive: false
  }
}

const lineYieldReducer = (state = initalState, action) => {
  const { type, payload } = action

  switch (type) {
    case "AWAITING_LINEYILD":
      return {
        ...state,
        loading: true
      }
    case "REJECTED_LINEYIELD":
      return {
        ...state,
        loading: false
      }
    case "SUCCESS_LINEYIELD":
      return {
        ...state,
        loading: false,
        data: {
          labels: payload.labels,
          datasets: [
            {
              label: "Kospi Yield",
              data: payload.kospi_data,
              fill: false,
              backgroundColor: "#3B75DB",
              borderColor: "#3B75DB",
              pointBorderColor: "#3B75DB",
              pointRadius: 0.3
            },
            {
              label: "Algorithm Yield",
              data: payload.my_data,
              fill: false,
              backgroundColor: "#FF7031",
              borderColor: "#FF7031",
              pointBorderColor: "#FF7031",
              pointRadius: 0.3
            }
          ]
        }
      }
    default:
      return state
  }
  return state
}

export default lineYieldReducer
