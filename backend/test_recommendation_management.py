from user_management import get_users_from_db
from ad_management import get_ads_from_db, get_total_ads_from_db
from recommendation_management import match_for_specific_user

user_id = "1000009"
ads_db_path = "ads.db"

total_num_ads = get_total_ads_from_db(ads_db_path)
num_ads_recommend = 7

matches = match_for_specific_user(user_id, total_num_ads, num_ads_recommend) # 认知计算广告

# output the matches
for match in matches:
    print(match["user_id"], match["matched_ads"])