const initalState = {
    loading: false,
    data: {
      labels: [],
      datasets: [{
        label: "BTC",
        data: [],
        backgroundColor: 'rgba(238,175,0, 0.4)',
        borderColor: 'rgba(238,175,0, 0.5)',
        pointBorderColor: 'rgba(238,175,0, 0.7)'
      }]
    }
  };
  
  const capitalGrowthReducer = (state = initalState, action) => {
    const { type, payload } = action;
  
    switch (type) {
      case "AWAITING_CAPITALGROWTH":
        return {
          ...state,
          loading: true
        }
      case "REJECTED_CAPITALGROWTH":
        return {
          ...state,
          loading: false,
        }
      case "SUCCESS_CAPITALGROWTH":
        return {
          ...state,
          loading: false,
          data: {
            labels: payload.labels,
            datasets: [
            {
              label: "BTC",
              data: payload.kospi_data,
              fill: false,
              backgroundColor: '#FF7031',
              borderColor: '#FF7031',
              pointBorderColor: 'rgba(238,175,0, 0.7)'
            }
            ]
          }
        }
      default:
        return state;
    }
    return state;
  }
  
  export default capitalGrowthReducer;
  