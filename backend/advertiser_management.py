import os
from gradio_client import Client
from fastapi import FastAPI, HTTPException
import requests

from common.exception import exception


def get_active_advertisers_from_db(db_path: str, start_date: str = None, end_date: str = None):
    """
    TODO: Gets a list of active advertisers from a SQLite database within a specified date range.

    Args:
        db_path: The path to the SQLite database file.
        start_date: Optional start date in YYYY-MM-DD format.
        end_date: Optional end date in YYYY-MM-DD format.

    Returns:
        A list of active advertisers, where each advertiser is a dictionary with the following keys:
        - id: The advertiser's ID.
        - advertisername: The advertiser's advertisername.
        - last_active: The advertiser's last active date and time.
    """
    pass

def get_total_advertisers_from_db(db_path: str):
    """
    TODO: Gets the total number of advertisers from a SQLite database.

    Args:
        db_path: The path to the SQLite database file.

    Returns:
        An integer representing the total number of advertisers.
    """
    pass

def get_advertisers_from_db(db_path: str):
    """
    TODO: Gets a list of advertisers from a SQLite database.

    Args:
        db_path: The path to the SQLite database file.

    Returns:
        A list of advertisers, where each advertiser is a dictionary with the following keys:
        - id: The advertiser's ID.
        - advertisername: The advertiser's advertisername.
        - password: The advertiser's password (hashed).
        - last_active: The advertiser's last active date and time.
    """
    pass

def register_advertiser_to_db(db_path: str, advertisername: str, password: str):
    """
    TODO: Registers a new advertiser to the database with improved security..

    Args:
        db_path: The path to the SQLite database file.
        advertisername: The advertisername of the new advertiser.
        password: The password of the new advertiser.

    Returns:
        True if the registration is successful, False otherwise.
    """
    pass

def login_advertiser_to_db(db_path: str, advertisername: str, password: str):
    """
    TODO: Logs in a advertiser on the platform using the database.

    Args:
        advertisername: The advertisername of the advertiser.
        password: The password of the advertiser.

    Returns:
        A tuple containing a boolean indicating success and a token if successful, otherwise None.
    """
    pass

def get_spcific_advertiser_from_db(db_path: str, advertiser_id: int):
    """
    TODO: Gets a specific advertiser from a SQLite database based on its ID.

    Args:
        db_path: The path to the SQLite database file.
        advertiser_id: The ID of the advertiser to retrieve.

    Returns:
        A dictionary representing the advertiser, or None if the advertiser is not found.
    """
    pass

def send_generation_request(host, params,):
    """
    TODO: 
    """
    STABILITY_API_KEY = os.environ["STABILITY_API_KEY"]

    headers = {
        "Accept": "image/*",
        "Authorization": f"Bearer {STABILITY_API_KEY}"
    }

    # Encode parameters
    files = {}
    image = params.pop("image", None)
    mask = params.pop("mask", None)
    if image is not None and image != '':
        files["image"] = open(image, 'rb')
    if mask is not None and mask != '':
        files["mask"] = open(mask, 'rb')
    if len(files)==0:
        files["none"] = ''

    # Send request
    print(f"Sending REST request to Suanfamama AIGC Ad Generation Engine ...")
    response = requests.post(
        host,
        headers=headers,
        files=files,
        data=params
    )
    if not response.ok:
        raise Exception(f"HTTP {response.status_code}: {response.text}")

    return response

def create_an_ad(prompt: str, negative_prompt: str, seed: int, aspect_ratio = "16:9"):
    """
    TODO: Make more parameters avaiable in the API
    """
    #seed = 9 #@param {type:"integer"} TODO: to be configurable
    #aspect_ratio = "16:9" #@param ["21:9", "16:9", "3:2", "5:4", "1:1", "4:5", "2:3", "9:16", "9:21"]
    output_format = "png" #@param ["jpeg", "png"]

    host = os.environ["STABILITY_HOST"]
    model = os.environ["STABILITY_MODEL"]

    params = {
        "prompt" : prompt,
        "negative_prompt" : negative_prompt,
        "aspect_ratio" : aspect_ratio,
        "seed" : seed,
        "output_format" : output_format,
        "model" : model,
        "mode" : "text-to-image"
    }

    response = send_generation_request(
        host,
        params
    )

    # Decode response
    output_image = response.content
    finish_reason = response.headers.get("finish-reason")
    seed = response.headers.get("seed")

    # Check for NSFW classification
    if finish_reason == 'CONTENT_FILTERED':
        raise Warning("Generation failed NSFW classifier")

    # Save and display result
    generated = "./ads/" + f"Suanfamama_AIGC_Ad_{seed}.{output_format}"
    with open(generated, "wb") as f:
        f.write(output_image)
    print(f"Saved image {generated}")

    return output_image