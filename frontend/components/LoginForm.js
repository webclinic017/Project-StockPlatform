import React, { useCallback, useState } from "react"
import { loginAction, logoutAction } from "../reducers/user"
import { useDispatch, useSelector } from "react-redux"
import Link from "next/link"

export const useInput = (initValue = null) => {
  const [value, setter] = useState(initValue)
  const handler = useCallback(e => {
    setter(e.target.value)
  }, [])
  return [value, handler]
}

const LoginForm = () => {
  const user = useSelector(state => state.user.user)
  const isLoggedIn = useSelector(state => state.user.isLoggedIn)

  const [id, onChangeId] = useInput("")
  const [password, onChangePassword] = useInput("")

  const dispatch = useDispatch()

  const onLogout = useCallback(() => {
    dispatch(logoutAction)
  }, [])

  const onSubmitForm = useCallback(e => {
    e.preventDefault()
    dispatch(
      loginAction({
        id,
        password
      })
    )
  })

  return (
    <>
      <form onSubmit={onSubmitForm}>
        <div>
          <label>아이디</label>
          <br />
          <input name="user-id" value={id} onChange={onChangeId} required />
        </div>
        <div>
          <label>비밀번호</label>
          <br />
          <input
            name="user-password"
            value={password}
            onChange={onChangePassword}
            required
          />
        </div>
        <div>
          {isLoggedIn ? (
            <button onClick={onLogout}>로그아웃</button>
          ) : (
            <div>
              <button type="submit">로그인</button>
              <Link href="">
                <a>
                  <button>회원가입</button>
                </a>
              </Link>
            </div>
          )}
        </div>
      </form>
    </>
  )
}

export default LoginForm
