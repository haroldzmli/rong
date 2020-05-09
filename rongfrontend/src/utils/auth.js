import Cookies from 'js-cookie'

const TokenKey = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImFkbWluIiwiZXhwIjoxNTkxNTgxNDI1LC' +
  'JlbWFpbCI6ImFkbWluQHFxLmNvbSJ9.5rfBfgi4kaPUYEF0__6x1-WG8Z0_0_rFaB0vOvRG9t0'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}
