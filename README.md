# 妈妈折扣券 2.0
## 简介
* 产品名称：妈妈折扣券
* 所属行业：Cognitive Computational Advertising & Cognitive Computational Fashion

## 核心功能
1. 用户 沉浸 在探索与使用折扣券的愉快体验中
2. 商家 沉浸 在创作折扣券和响应服务的愉快赚钱体验

## 产品设计思维导图
![](./docs/ProductDesign.png)

## 技术选型
1. FastAPI for the Python backend API.
2. SQLModel for the Python SQL database interactions (ORM).
3. Pydantic, used by FastAPI, for the data validation and settings management.
4. MySQL as the SQL database.
5. Vue for the frontend.
  - Using TypeScript, hooks, Vite, and other parts of a modern frontend stack.
  - Chakra UI for the frontend components.
  - An automatically generated frontend client.
  - Dark mode support.
  - Docker Compose for development and production.
  - Secure password hashing by default.
  - JWT token authentication.
  - Email based password recovery.
6. Tests with Pytest.
7. Nginx / Traefik as a reverse proxy / load balancer.
8. Deployment instructions using Docker Compose, including how to set up a frontend Traefik proxy to handle automatic HTTPS certificates.
9. CI (continuous integration) and CD (continuous deployment) based on GitHub Actions.

## 主创团队
* Wei Jiang, wei@suanfamama.com
* Mama Xiao, mama.xiao@suanfamama.com
