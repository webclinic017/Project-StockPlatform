import React from "react"
import { useSelector, useDispatch } from "react-redux"
import { stocks_getData } from "../../actions/stocksActions"

const Items = () => {
  const dispatch = useDispatch()
  const stocksState = useSelector(state => state.stocksReducer)
  console.log("!!!!!!!!!!", stocksState)
  // console.log("길이!!!", stocksState.stocks[0].length)
  // console.log("첫번째 요소!!!", stocksState.stocks[0][0])

  const stocksDatas = stocksState.stocks
  console.log("stocksDatas", stocksDatas)
  let stocksDataList

  if (stocksDatas.length != 0) {
    console.log("없다고 나옴!")
    const revalancing_count = stocksState.stocks.length
    console.log("리밸런싱 횟수", revalancing_count)

    const stocks_count = stocksState.stocks[0]
    console.log("첫번째 리밴런싱이 준 종목갯수:", stocks_count)

    stocksDataList = stocksDatas[0].map(stocksData => <div>{stocksData}</div>)

    // for (var i = 0; i < revalancing_count; i++) {
    //   stocksDataList = stocksDatas[i].map(stocksData => <div>{stocksData}</div>)
    // }
  } else {
    //없을 때
    stocksDataList = ""
  }

  // const fetchData = () => {
  //   dispatch(stocks_getData())
  // }
  // console.log(stocksState)

  return (
    <>
      <div>{stocksState.loading}</div>
      <div className="items-stockList">{stocksDataList}</div>
      {/* <div className="items-stockList"></div> */}
    </>
  )
}

export default Items
