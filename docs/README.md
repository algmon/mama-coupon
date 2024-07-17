# 系统设计文档
## User Management Module
* 不存储用户密码明文，但存储密码的哈希值用于平台登录逻辑

## Ad Management Module
* 广告本身以对象存储于主流厂商Key-Value对中

## Recommendation Module
* 核心算法适配大数据环境，由SLA规定平台性能

## APIs
* 我们不使用put操作，只使用get post delete

## Common HTTP status codes used in Suanfamama APIs
### Success Codes
* 200 OK
* 201 Created
* 202 Accepted
* 204 No Content
### Client Error Codes
* 400 Bad Request
* 401 Unauthorized
* 403 Forbidden
* 404 Not Found
* 405 Method Not Allowed
* 409 Conflict
### Server Error Codes
* 500 Internal Server Error
* 503 Service Unavailable
