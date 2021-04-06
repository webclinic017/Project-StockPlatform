import Axios from "axios"

export const winRate_getData = () => async dispatch => {
  try {
    dispatch({
      type: "AWAITING_WINRATE"
    })

    const res = await fetch("/api/winRatetest")
    const doc = await res.json()
    let win = doc[doc.length - 1].Winning_rate
    let lose = 10 - win
    console.log("win", win)

    console.log("res", res)
    console.log("doc", doc)

    const winRate_data = []

    winRate_data.push(win)
    winRate_data.push(lose)

    dispatch({
      type: "SUCCESS_WINRATE",
      payload: {
        winRate_data
      }
    })
  } catch (e) {
    dispatch({
      type: "REJECTED_WINRATE"
    })
  }
}

export default winRate_getData
