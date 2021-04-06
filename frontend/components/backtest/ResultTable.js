import React from "react"
import { useSelector, useDispatch } from "react-redux"
import { resultTable_getData } from "../../actions/resultTableActions"

const ResultTable = () => {
  const dispatch = useDispatch()
  const resultTableState = useSelector(state => state.resultTableReducer)

  const fetchData = () => {
    dispatch(resultTable_getData())
  }
  console.log(resultTableState)

  return (
    <>
      {/* <button onClick={() => fetchData()}>BUTTON</button> */}
      <section className="resultTable-contents">
        <table>
          <tbody>
            <tr>
              <td>investment</td>
              <td>{resultTableState.result_table.investment} Won</td>
            </tr>
            <tr>
              <td>TOTAL INCOME</td>
              <td>{resultTableState.result_table.totalIncome} Won</td>
            </tr>
            <tr>
              <td>CURRENT ASSET</td>
              <td>{resultTableState.result_table.currentAsset} Won</td>
            </tr>
            <tr>
              <td>FINAL YIELD(CAGR)</td>
              <td>{resultTableState.result_table.Final_yield} %</td>
            </tr>
          </tbody>
        </table>
      </section>
    </>
  )
}

export default ResultTable
