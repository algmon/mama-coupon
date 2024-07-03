# AIGC认知计算广告平台设计文档
## User Management Module
* 不存储用户密码明文，但存储密码的哈希值用于平台登录逻辑

## Ad Management Module
* 广告本身以对象存储于主流厂商Key-Value对中

## Recommendation Module
* 核心算法适配大数据环境，由SLA规定平台性能