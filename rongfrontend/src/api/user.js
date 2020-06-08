import request from '@/utils/request'

export function login(data) {
  return request({
    // alert('ddata,', data)
    // url: '/vue-element-admin/user/login',
    url: '/cstddataplat/api/v0.1/account/token/',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    // url: '/vue-element-admin/user/info',
    url: '/cstddataplat/api/v0.1/account/user/',
    method: 'get',
    params: { token }
  })
}

export function logout() {
  return request({
    // url: '/cstddataplat/api/v0.1/account/logout',
    url: '/cstddataplat/api/v0.1/account/logout/',
    method: 'post'
  })
}
