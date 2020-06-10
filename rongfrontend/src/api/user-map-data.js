import request from '@/utils/request'

export function getUserMapData(query) {
  return request({
    url: '/cstddataplat/api/v0.1/maps/data/user/',
    method: 'get',
    params: { query }
  })
}

export function detailUserMapData(token) {
  return request({
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
