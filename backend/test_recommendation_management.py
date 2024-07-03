from user_management import get_users_from_db
from ad_management import get_ads_from_db
from recommendation_management import match

print("Hello World")
users_db_path = "users.db"
ads_db_path = "ads.db"

users = get_users_from_db(users_db_path)
ads = get_ads_from_db(ads_db_path)

matches = match(users, ads) # 认知计算广告

# output the matches
for match in matches:
    print(match["user_id"], match["matched_ads"])