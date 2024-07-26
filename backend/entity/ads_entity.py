import datetime

class AdsEntity:
    def __init__(self, *args, **kwargs):
        if args:
            self.id = args[0]
            self.adname = args[1]
            self.creator = args[2]
            self.object_url = args[3]
            self.created_at = args[4]
            self.attributes = args[5]
            self.content = args[6]
            self.target_group = args[7]
            self.last_updated_at = args[8]
            self.is_active = args[9]
            self.aigc_image_gen_engine = args[10]
            self.aigc_text_gen_engine = args[11]
            self.aigc_sound_gen_engine = args[12]
            self.prompt_for_image_gen = args[13]
            self.like = args[14]
            self.dislike = args[15]
            self.advertiser_id = args[16]
        else:
            self.id = kwargs.get('id')
            self.adname = kwargs.get('adname')
            self.creator = kwargs.get('creator')
            self.object_url = kwargs.get('object_url')
            self.created_at = kwargs.get('created_at')
            self.attributes = kwargs.get('attributes')
            self.content = kwargs.get('content')
            self.target_group = kwargs.get('target_group')
            self.last_updated_at = kwargs.get('last_updated_at')
            self.is_active = kwargs.get('is_active')
            self.aigc_image_gen_engine = kwargs.get('aigc_image_gen_engine')
            self.aigc_text_gen_engine = kwargs.get('aigc_text_gen_engine')
            self.aigc_sound_gen_engine = kwargs.get('aigc_sound_gen_engine')
            self.prompt_for_image_gen = kwargs.get('prompt_for_image_gen')
            self.like = kwargs.get('like', 0)
            self.dislike = kwargs.get('dislike', 0)
            self.advertiser_id = kwargs.get('advertiser_id')
    def __repr__(self):
        return (f"Ad(id={self.id}, adname={self.adname}, creator={self.creator}, "
                f"object_url={self.object_url}, created_at={self.created_at}, "
                f"attributes={self.attributes}, content={self.content}, "
                f"target_group={self.target_group}, last_updated_at={self.last_updated_at}, "
                f"is_active={self.is_active}, aigc_image_gen_engine={self.aigc_image_gen_engine}, "
                f"aigc_text_gen_engine={self.aigc_text_gen_engine}, "
                f"aigc_sound_gen_engine={self.aigc_sound_gen_engine}, "
                f"prompt_for_image_gen={self.prompt_for_image_gen}, like={self.like}, "
                f"dislike={self.dislike}, advertiser_id={self.advertiser_id})")
    def to_dict(self):
        return {
            "id": self.id,
            "adname": self.adname,
            "creator": self.creator,
            "object_url": self.object_url,
            "created_at": self.created_at,
            "attributes": self.attributes,
            "content": self.content,
            "target_group": self.target_group,
            "last_updated_at": self.last_updated_at,
            "is_active": self.is_active,
            "aigc_image_gen_engine": self.aigc_image_gen_engine,
            "aigc_text_gen_engine": self.aigc_text_gen_engine,
            "aigc_sound_gen_engine": self.aigc_sound_gen_engine,
            "prompt_for_image_gen": self.prompt_for_image_gen,
            "like": self.like,
            "dislike": self.dislike,
            "advertiser_id": self.advertiser_id,
        }


# 示例：创建一个Ad对象，部分参数不传
# ad = Ad(
#     adname="Example Ad",
#     creator="John Doe",
#     object_url="https://example.com/image.png",
#     like=10,
#     dislike=2
# )

# print(ad)

def new_ads_entity(self, *args):
        # 确保传入的参数数量正确
        if len(args) != 17:
            raise ValueError("Incorrect number of arguments")
        self.id = args[0]
        self.adname = args[1]
        self.creator = args[2]
        self.object_url = args[3]
        self.created_at = args[4]
        self.attributes = args[5]
        self.content = args[6]
        self.target_group = args[7]
        self.last_updated_at = args[8]
        self.is_active = args[9]
        self.aigc_image_gen_engine = args[10]
        self.aigc_text_gen_engine = args[11]
        self.aigc_sound_gen_engine = args[12]
        self.prompt_for_image_gen = args[13]
        self.like = args[14]
        self.dislike = args[15]
        self.advertiser_id = args[16]