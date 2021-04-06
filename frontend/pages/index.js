import React, { useState } from "react"
import Link from "next/link"
// import Head from "next/head"
import { useDispatch, useSelector } from "react-redux"
// import {LOG_IN, LOG_OUT} from '../reducers/user';
// import { loginAction, logoutAction } from "../reducers/user"
// import LoginForm from "../components/LoginForm"

const Home = () => {
  // const dispatch = useDispatch()
  // const {isLoggedIn, user} = useSelector(state => state.user)
  const user = useSelector(state => state.user.user)
  const isLoggedIn = useSelector(state => state.user.isLoggedIn)
  // const { mainGroups } = useSelector(state => state.group)
  console.log(isLoggedIn)
  console.log(user)

  let { menuState, setMenuState } = useState(false)

  const show_menubar = () => {
    setMenuState(!menuState)
  }

  return (
    <div className="index">
      <nav>
        <span className="logo">
          <Link href="/">
            <a></a>
          </Link>
        </span>
        <span className="linkBtn-container">
          <li className="linkBtn">
            <Link href="/backtest">
              <a>BACKTEST</a>
            </Link>
          </li>
          <li className="linkBtn">
            <Link href="">
              <a>LOGIN</a>
            </Link>
          </li>
          <li className="linkBtn">
            <Link href="">
              <a>SIGNUP</a>
            </Link>
          </li>
          {/* <li className="linkBtn"><Link href=""><a>
            
            </a></Link></li>
          {user ? <div>로그인했습니다. {user.nickname}</div> : <div>로그아웃 했습니다</div>} */}
        </span>

        <span className="profile">
          <Link href="/profile">
            <a></a>
          </Link>
        </span>
      </nav>
      <i class="fas fa-bars"></i>

      {/* <LoginForm/> */}
      <section className="main">
        {/* main */}
        <article>
          <div>Welcome!</div>
          <div>
            Maxturn - 수익률을 확인하고 투자하세요.
            <br></br>
            맥스턴은 백테스트를 진행하고, 이에 대한 전략을 수립하고 유저들과
            공유하는 플랫폼입니다.
          </div>
          <div>맥스턴은 여러분의 시간, 노력을 절감시켜줄 수 있습니다.</div>
        </article>
      </section>

      <section className="introduction">
        {/* introduction */}
        <div className="introduction_title">INTRODUCTION</div>
        <article>
          <div className="introduction_content1">
            <figure>photo1</figure>
            <figcaption>
              백테스팅 서비스를 제공합니다. 특정 기간을 설정하고, 사용자가
              선택한 전략대로 과거 시뮬레이션을 진행합니다. 과거 주가 데이터를
              활용하여 불확실성을 줄이고, 자신만의 투자 전략을 수립합니다.
              실제처럼 실행하고 모든 결과를 기록해 분석합니다. 전략의 성과를
              평가합니다.
            </figcaption>
          </div>
          <div className="introduction_content2">
            <figure>photo2</figure>
            <figcaption>
              플랫폼 자체 커뮤니티로 투자자간 정보 공유 서비스를 제공합니다.
              자신의 전략에 대한 다른 사람의 의견을 듣기 위해 백테스팅 데이터를
              커뮤니티에 공유할 수 있습니다. 커뮤니티에서 의견을 주고받으며
              투자에 관한 다양한 지식을 쌓을 수 있습니다. 또한, 전략을 평가받고
              부족한 것이나 잘못된 것을 고칠 수 있습니다. 백테스팅으로 구한
              수익률 데이터를, 다양한 측면을 반영한 수치로 분석하여 나에게
              적합한 전략인지 아닌지 판가름 해줍니다.{" "}
            </figcaption>
          </div>
          {/* <div className="introduction_content3">
            <figure>photo3</figure>
            <figcaption>설명3</figcaption>
          </div> */}
        </article>
      </section>

      <section className="login">
        <div className="login_title">LOGIN</div>

        {/* 로그인 */}
        <article>
          <form>
            {/* <div>LOG IN</div> */}
            <div className="idBox">
              <label for="user_id">ID</label>
              <input type="text" id="user_id"></input>
            </div>
            <div className="pwBox">
              <label for="user_password">PW</label>
              <input type="password"></input>
            </div>
            <button type="submit">
              <Link href="/backtest">
                <a>BACKTESTING</a>
              </Link>
            </button>
          </form>
        </article>
      </section>
      {/* <footer></footer> */}
    </div>
  )
}

export default Home
