import Cookies from 'js-cookie'

const TokenKey = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwiaWF0IjoxNTkxMzQ0ODI4LCJleHAiOjE1OTM5MzY4MjgsInVzZXJfaWQiOjF9.zxIUq88SZqu_c_bekaNLU94vjuqgw2ctz9w2cGhrgUI'

export function getToken() {
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}
