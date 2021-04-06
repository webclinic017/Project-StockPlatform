import { combineReducers } from "redux"
import user from "./user"
import group from "./group"
import lineYieldReducer from "./lineYieldReducer"
import winRateReducer from "./winRateReducer"
import capitalGrowthReducer from "./capitalGrowthReducer"
import stocksReducer from "./stocksReducer"
import resultTableReducer from "./resultTableReducer"

const rootReducer = combineReducers({
  user,
  group,
  lineYieldReducer,
  winRateReducer,
  capitalGrowthReducer,
  resultTableReducer,

  stocksReducer
})

export default rootReducer
