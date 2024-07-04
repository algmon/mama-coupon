from ad_management import get_total_ads_from_db, get_ads_from_db, update_ad

db_path = "./db/ads.db"
#print("total # of ads available:", get_total_ads_from_db(db_path))
#print(get_ads_from_db("ads.db"))

ad_id = 99
ad_data = {
    "adname": "Google Gemini - the Multimodal Transformer",
    "creator": "Google",
    "object_url": "https://res.cloudinary.com/djba6ta1n/image/upload/v1708589440/algmon/algmon-company-website/talk/wei/1.multimodal",
    "ad_id": ad_id
}
print(update_ad(db_path, ad_data))

ad_id = 100
ad_data = {
    "adname": "Microsoft Bing - the Balance between Search & Chat",
    "creator": "Microsoft",
    "object_url": "https://res.cloudinary.com/djba6ta1n/image/upload/v1708589440/algmon/algmon-company-website/talk/wei/2.rag",
    "ad_id": ad_id
}
print(update_ad(db_path, ad_data))

ad_id = 101
ad_data = {
    "adname": "LinkAI - the leading AI Agent platform",
    "creator": "LinkAI",
    "object_url": "https://res.cloudinary.com/djba6ta1n/image/upload/v1708589440/algmon/algmon-company-website/talk/wei/3.platform.and.edges",
    "ad_id": ad_id
}
print(update_ad(db_path, ad_data))

ad_id = 102
ad_data = {
    "adname": "AI Powered Fashion Store",
    "creator": "Suanfamama",
    "object_url": "https://res.cloudinary.com/djba6ta1n/image/upload/v1708589440/algmon/algmon-company-website/talk/wei/7.store",
    "ad_id": ad_id
}
print(update_ad(db_path, ad_data))

ad_id = 103
ad_data = {
    "adname": "We are inventing transformer, transformer is reinventing the world",
    "creator": "Google",
    "object_url": "https://res.cloudinary.com/djba6ta1n/image/upload/v1708589440/algmon/algmon-company-website/talk/wei/5.transformer",
    "ad_id": ad_id
}
print(update_ad(db_path, ad_data))

ad_id = 104
ad_data = {
    "adname": "AI Powered Self Study Space",
    "creator": "Suanfamama",
    "object_url": "https://res.cloudinary.com/djba6ta1n/image/upload/v1708589440/algmon/algmon-company-website/talk/wei/6.selfstudyroom",
    "ad_id": ad_id
}
print(update_ad(db_path, ad_data))

ad_id = 105
ad_data = {
    "adname": "AI Design Artwork Showcase",
    "creator": "Suanfamama",
    "object_url": "https://res.cloudinary.com/djba6ta1n/image/upload/v1709644025/AI%20Yuanyoushe%20Men%20Spring%202024/Look.01.SS.2024.8.png",
    "ad_id": ad_id
}
print(update_ad(db_path, ad_data))