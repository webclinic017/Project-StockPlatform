import React from "react"
import Head from "next/head"

// style
import "../styles/utils.scss"

// index style
import "../styles/index/index.scss"

// backtest style
import "../styles/backtest/backtest.scss"
import "../styles/backtest/filterform.scss"
import "../styles/backtest/maingraph.scss"
import "../styles/backtest/subgraph.scss"
import "../styles/backtest/items.scss"
import "../styles/backtest/resultTable.scss"

// mypage style
import "../styles/mypage/mypage.scss"
import "../styles/mypage/mypage_strategyList.scss"

//community style
import "../styles/community/community.scss"

// layout style
import "../styles/layout/dashboardLayout.scss"

// reducer와 react-redux(react, redux연결), next-redux-wrapper(송골매컴포넌트에 store props로 넣어줌)
import reducer from "../reducers"
import { Provider } from "react-redux"
import withRedux from "next-redux-wrapper"
import { createStore, compose, applyMiddleware } from "redux"

// 동주 수정사항 redux-thunk 추가
import ReduxThunk from "redux-thunk"

const Songgolmae = ({ Component, store }) => {
  return (
    <Provider store={store}>
      <Head>
        <title>송골메</title>
        <script
          src="https://kit.fontawesome.com/0178baa171.js"
          crossorigin="anonymous"
        ></script>
        {/* <link rel="stylesheet" href="https://use.typekit.net/mel0thu.css"></link> */}
      </Head>
      <Component />
    </Provider>
  )
}

// import ReduxThunk from 'redux-thunk';

export default withRedux((initialState, options) => {
  // const middleware = [ReduxThunk];
  const middleware = [ReduxThunk]
  const enhance = compose(
    applyMiddleware(...middleware),
    !options.isServer &&
      typeof window !== "undefined" &&
      typeof window.__REDUX_DEVTOOLS_EXTENSION__ !== "undefined"
      ? window.__REDUX_DEVTOOLS_EXTENSION__()
      : f => f
  )
  const store = createStore(reducer, initialState, enhance)
  return store
})(Songgolmae) //고차컴포넌트 -> 기존컴포넌트 기능 확장
