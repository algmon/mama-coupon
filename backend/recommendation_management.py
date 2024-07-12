import ad_management
import user_management
import random
# from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

def get_users(db_path: str):
    """
    Retrieves a list of users from the database.

    Args:
        db_path (str): Path to the database file.

    Returns:
        list: A list of user dictionaries.
    """
    users = user_management.get_users_from_db(db_path)
    return users

def get_ads(db_path: str):
    """
    Retrieves a list of ads from the database.

    Args:
        db_path (str): Path to the database file.

    Returns:
        list: A list of ad dictionaries.
    """
    ads = ad_management.get_ads_from_db(db_path)
    return ads

def match(users: list, ads: list):
    """
    Matches(认知) users with ads based on 用户动态画像 and 计算广告动态画像.
    TODO: In the context of big data, too slow. Needs to be optimized.

    Args:
        users (list): A list of user dictionaries.
        ads (list): A list of ad dictionaries.

    Returns:
        list: A list of user-ad matches.
    """
    # Create a list to store user-ad matches
    matches = []

    # alg0: random assignment: for each user, recommend 2 ads, randomly
    for user in users:
        # Randomly select 2 ads from the list of ads
        random_ads = random.sample(ads, 2)
        random_ads_ids = [ad["id"] for ad in random_ads]

        # Create a match dictionary for the user and their randomly selected ads
        match = {
            "user_id": user["id"],
            "matched_ads": random_ads_ids
        }

        # Append the match to the matches list
        matches.append(match)

    return matches

def match_for_specific_user(user_id: str, total_num_ads_avaiable: int, num_ads_recommend: int):
    """
    Matches(认知) a specific user with ads based on 用户动态画像 and 计算广告动态画像.

    Args:
        user_id:
        total_num_ads_avaiable:
        recommend:

    Returns:
        list: A list of user-ad matches.
    """
    # Create a list to store user-ad matches
    matches = []
    random_ads_ids = []

    # alg0: recommend ads, randomly
    random_ads_ids = random.sample(range(1, total_num_ads_avaiable + 1), num_ads_recommend)
    random_ads_ids = [str(ad_id) for ad_id in random_ads_ids]  # Convert to string

    # Create a match dictionary for the user and their randomly selected ads
    match = {
        "user_id": user_id,
        "matched_ads": random_ads_ids,
        "num_ads_returned": num_ads_recommend
    }

    # Append the match to the matches list
    matches.append(match)

    return matches