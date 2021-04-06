export const lineYield_getData = () => async dispatch => {
  try {
    dispatch({
      type: "AWAITING_LINEYIELD"
    })

    const labels = []
    const my_data = []

    const res_my = await fetch("/api/results")
    const doc_my = await res_my.json()

    console.log("length", doc_my.length)
    const current_count = doc_my.length - 1

    var length = doc_my[current_count].Current_assets_by_date.length
    var start_date = doc_my[current_count].Current_assets_by_date[0].Date
    var end_date = doc_my[current_count].Current_assets_by_date[length - 1].Date

    console.log(length)
    console.log(start_date)
    console.log(end_date)

    for (var i = 0; i < length; i++) {
      var counter = doc_my[current_count].Current_assets_by_date[i]

      var Asset = counter.Asset
      var standard_Asset = doc_my[current_count].Current_assets_by_date[0].Asset

      //( ( 현재 종가 / 기준날짜 종가 ) -1 )*100
      // 알고리즘 수익률 또한 위와 같은 식으로 수익률 계산 가능
      var my_Yield = ((Asset - standard_Asset) / standard_Asset) * 100

      my_data.push(my_Yield)
      labels.push(counter.Date)
    }

    // ------>  코스피 그래프

    const res = await fetch("/api/kospi")
    const doc = await res.json()
    const kospi_data = []
    //console.log(doc);
    var find_date_index = 0
    while (1) {
      if (doc[0].kospi[find_date_index].Date == end_date) {
        var end_index = find_date_index
      }
      if (doc[0].kospi[find_date_index].Date == start_date) {
        var start_index = find_date_index
        break
      }
      find_date_index++
    }
    //start_index = 1058, end_index = 348
    for (var i = start_index; i >= end_index; --i) {
      var counter = doc[0].kospi[i]

      var Close = counter.End
      var standard_Close = doc[0].kospi[start_index].End

      //( ( 현재 종가 / 기준날짜 종가 ) -1 )*100
      // 알고리즘 수익률 또한 위와 같은 식으로 수익률 계산 가능
      var kospi_Yield = ((Close - standard_Close) / standard_Close) * 100

      kospi_data.push(kospi_Yield)
    }

    //length 기본 예시로 100개만 뽑아봄
    //var length = 100;

    dispatch({
      type: "SUCCESS_LINEYIELD",
      payload: {
        labels,
        kospi_data,
        my_data
      }
    })
  } catch (e) {
    console.log(e)
    dispatch({
      type: "REJECTED_LINEYIELD"
    })
  }
}
