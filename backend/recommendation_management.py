import ad_management
import user_management
import random
from sklearn.metrics.pairwise import cosine_similarity
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

    '''
    # alg1: cosine similarity

    # Convert user and ad data to pandas DataFrames
    users_df = pd.DataFrame(users)
    ads_df = pd.DataFrame(ads)

    print(users_df)
    print(ads_df)

    # Calculate cosine similarity between user interests and ad keywords
    similarities = cosine_similarity(users_df["interests"], ads_df["keywords"])

    # Iterate through users and find their top matching ads
    for user_index, user in enumerate(users):
        # Get the similarity scores for the current user
        user_similarities = similarities[user_index]

        # Sort ads by similarity score in descending order
        sorted_ads = ads_df.sort_values(by=user_similarities, ascending=False)

        # Get the top 5 matching ads
        top_ads = sorted_ads[:5]

        # Create a match dictionary for the user and their top ads
        match = {
            "user_id": user["user_id"],
            "matched_ads": top_ads.to_dict(orient="records")
        }

        # Append the match to the matches list
        matches.append(match)

    return matches
    '''

