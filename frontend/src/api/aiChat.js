import request from '@/utils/request'

export function fetchAnswer(data) {
  return request({
    url: '/aiChat/answer',
    method: 'post',
    data
  })
}
