import boto3
from datetime import datetime

def get_total_ads_from_db(db_path: str):
    """
    Retrieves the total number of ads from the database.

    Args:
        db_path (str): Path to the database file.

    Returns:
        int: The total number of ads.
    """
    total_ads = 0
    if db_path == "ads.db":
        s3 = boto3.resource('s3')
        bucket_name = "fashion-videos"
        bucket = s3.Bucket(bucket_name)
        for obj in bucket.objects.all():
            total_ads += 1    
    return total_ads

def get_ads_from_db(db_path: str):
    """
    Retrieves all ads from the database.

    Args:
        db_path (str): Path to the database file.

    Returns:
        list: A list of all ads.
    """
    ads = []
    if db_path == "ads.db":
        s3 = boto3.resource('s3')
        bucket_name = "fashion-videos"
        bucket = s3.Bucket(bucket_name)
        for obj in bucket.objects.all():
            ads.append(obj.key)
    return ads
