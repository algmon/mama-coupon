import Cookies from 'js-cookie'

const TokenKey = 'Admin-Token'
const Token = 'token'
export function getToken() {
  return Cookies.get('token')
}

export function setToken(token) {
  console.log('TokenKey:', token)
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}
