import json
import boto3
# 读取配置

def init_s3():
    config = read_config_file('config.json')
    s3_config = config['s3']
    # 配置S3的访问信息
    access_key = s3_config['access_key']
    secret_key = s3_config['secret_key']

    # 创建S3资源对象
    s3 = boto3.resource('s3', aws_access_key_id=access_key, aws_secret_access_key=secret_key)
    return s3

    
def read_config_file(filepath):
    with open(filepath, 'r') as file:
        return json.load(file)

def upload_file(file_path,file_name: str):
    s3=init_s3()
# 获取桶对象
    bucket = s3.Bucket('fashion-imgs')
    # path = r".\ads\Suanfamama_AIGC_Ad_New.png"
    # 上传文件
    # bucket.upload_file(file_path , "Suanfamama_file_name")
     # 获取当前时间戳
    # 将时间戳转换为可读的日期和时间
    bucket.upload_file(file_path , file_name)

    # 获取对象的元数据
    obj = s3.Object('fashion-imgs', file_name)
    metadata = obj.head()
    print("对象元数据：", metadata)

    print("已上传s3文件："+file_name)


def generate_presigned_url(bucket_name, object_key):
    s3_client = boto3.client('s3')
    try:
        # 生成预签名URL，ExpiresIn指定URL的有效期（秒）
        presigned_url = s3_client.generate_presigned_url('get_object',
                                                          Params={'Bucket': bucket_name, 'Key': object_key},
                                                          ExpiresIn=3600)  # URL有效期1小时
        return presigned_url    
    except Exception as e:
        print("生成预签名URL失败：", e)
        return None


def get_file(file_name):
    s3=init_s3()
    # 获取对象的元数据
    obj = s3.Object('fashion-imgs', file_name)
    metadata = obj.head()
    print("对象元数据：", metadata)

    # 生成预签名URL
    url = generate_presigned_url('fashion-imgs', file_name)
    print("已上传s3文件：" + file_name)
    print("文件URL：", url)
    return url


