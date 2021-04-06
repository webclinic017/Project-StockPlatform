// import axios from 'axios';

// const response = axios.get('api/hello');
// console.log(response)

const idNumber = "1"

export const initialState = {
  isLoggedIn: false,
  user: null,
  loginData: {}
}

export const LOG_IN = "LOG_IN"
export const LOG_OUT = "LOG_OUT"

export const loginAction = data => {
  return {
    type: LOG_IN,
    data
  }
}

export const logoutAction = {
  type: LOG_OUT
}

export default (state = initialState, action) => {
  switch (action.type) {
    case LOG_IN: {
      return {
        ...state,
        isLoggedIn: true,
        userId: idNumber
      }
    }
    case LOG_OUT: {
      return {
        ...state,
        isLoggedIn: false,
        user: null
      }
    }

    default: {
      return {
        ...state
      }
    }
  }
}
