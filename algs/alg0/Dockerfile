FROM python:3.9.7
LABEL maintainer="haoyu@suanfamama.com"

COPY . /work

# 设置工作目录
WORKDIR /work

# 安装依赖
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 配置环境变量
ENV LINKAI_KEY Link_QD0sBpxMnEfswdoTZkh7EYU9IIzt2PywnWytt9qhnz
ENV LINKAI_HOST https://api.link-ai.tech/v1/chat/completions
ENV LINKAI_CODE_2 iGpUvtoQ

# 设置外部连接端口
EXPOSE 3000

#
CMD ["python", "Person_register.py"]
