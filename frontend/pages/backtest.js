import React from "react"
import DashboardLayout from "../components/layout/DashboardLayout"
import FilterForm from "../components/backtest/FilterForm"
import Items from "../components/backtest/Items"
import ResultTable from "../components/backtest/ResultTable"
import MainGraph from "../components/backtest/MainGraph"

import OddsGraph from "../components/backtest/OddsGraph"

const BackTest = () => {
  return (
    <div>
      <DashboardLayout>
        <div className="backtest-contents">
          {/* 결과section */}
          <section className="result-section">
            <div className="result-firstLine-title">BACKTESTING RESULT</div>
            <div className="result-firstLine-detail">
              맥스턴은 코스피 주식을 기반으로, 거래 수수료0, 거래세0, 거래
              가격은 당일 종가를 기본으로 설정하고 있습니다.
            </div>
            <div className="result-firstLine">
              <div className="result-box">
                <div className="item-result-box">
                  <article className="items">
                    <Items />
                  </article>
                  <article className="result">
                    <ResultTable />
                  </article>
                </div>
                <article className="subGraph1">
                  {/* 임의의 승률 보여줌*/}
                  <OddsGraph />
                </article>
              </div>
            </div>
            <div className="result-secondLine">
              <article className="mainGraph">
                <MainGraph />
              </article>
            </div>
          </section>

          {/* 파라미터 section */}
          <section className="parameter-section">
            <div className="parameter-title">PARAMETER</div>
            <div className="parameter-detail">
              맥스턴은 코스피 주식을 기반으로, 거래 수수료0, 거래세0, 거래
              가격은 당일 종가를 기본으로 설정하고 있습니다.
            </div>
            <article className="filterContainer">
              <FilterForm />
            </article>
          </section>
        </div>
      </DashboardLayout>
    </div>
  )
}

export default BackTest
