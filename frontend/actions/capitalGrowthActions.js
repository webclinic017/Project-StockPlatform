export const capitalGrowth_getData = () => async dispatch => {
    try {
      dispatch({
        type: "AWAITING_CAPITALGROWTH"
      })
  
      const res = await fetch('http://localhost:3000/api/kospi')
      const doc = await res.json()
      //console.log(doc);
  
      const labels = [];
      const kospi_data = [];
  
      //length 기본 예시로 100개만 뽑아봄
      var length = 100;
      //mongodb 접속해서
      for(var i = 0; i < length; i++){
          var counter = doc[0].kospi[i];
          
          var Date = counter.Date;
          var Close = counter.End;
          var standard_Close = doc[0].kospi[length - 1].End;
  
          //( ( 현재 종가 / 기준날짜 종가 ) -1 )*100
          // 알고리즘 수익률 또한 위와 같은 식으로 수익률 계산 가능
          var Yield = ((Close-standard_Close)/standard_Close) * 100;
  
          kospi_data.unshift(Yield);
          labels.unshift(Date);
  
      }
  
  
      dispatch({
        type: "SUCCESS_CAPITALGROWTH",
        payload: {
          kospi_data,
          labels
        }
      })
    } catch (e) {
      dispatch({
        type: "REJECTED_CAPITALGROWTH",
      })
    }
  }
  