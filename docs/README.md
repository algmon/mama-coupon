# 妈妈折扣券产品设计及系统设计文档
## 生产者 - 消费者设计模式 The Producer Consumer Design Pattern
* 1. 折扣券生产者会不断向算法妈妈折扣券池中生产众多折扣券，这些折扣券按某种方式进行排序。这是折扣券公共资源池；
* 2. 折扣券消费者会不断从折扣券公共资源池中主动选择（通过搜索算法）或被动选择（通过推荐算法）准实时或实时获取源源不断的个性化折扣券；
* 3. 算法妈妈折扣券平台的核心职责在于（1）使折扣券生产者有利可图，促成商业闭环（2）使折扣券消费者有利可赚（3）算法妈妈折扣券平台背后的股东利益及稳定流量等
* The producer-consumer design pattern is a concurrent programming pattern that's often used in multi-threaded applications. It's used to improve data sharing between processes that produce and consume data at different rates. In the producer-consumer pattern, roles are designated as either producers or consumers. Producers add to a shared resource, while consumers remove from it. The tasks produced and consumed are kept in a shared public feed (queue) that's accessible to both producers and consumers. This pattern helps prevent data race conditions and ensures efficient data sharing.

## 推荐模块 Recommendation Module
* recommendation_management.py

## 重要技术路线约定
* 使用 nixpacks 作为后端Builder Tool

## 重要研发约定
* 我们 遵循 Google代码编写风格
* 我们的核心算法 适配 大数据及人工智能环境，遵循平台SLA性能规定
* 我们 采用 Git分支管理策略，并在此基础上作创新
* 我们 采用 MarsCode: AI Coding Assistant（国内）或Gemini Code Assist（国外）以辅助编程及算法设计
* 我们 采用 Github Issues 和 Github Projects（即产品与项目看板）以进行产品及项目进度管理
* 我们 设计并实现 RESTful API，并在此基础上作创新
* 我们 采用 Docker 以使得研发-测试-部署流程更顺畅
