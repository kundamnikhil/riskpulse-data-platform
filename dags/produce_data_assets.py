import logging
import requests
import json
from airflow.sdk import Asset, asset

posts_asset = Asset("dbfs:/data-platform/raw/posts.json")
users_asset = Asset("dbfs:/data-platform/raw/users.json")

@asset.multi(schedule="@daily", outlets=[posts_asset, users_asset])
def produce_data_assets():
    # Fetch posts from JSONPlaceholder API
    logging.info("Fetching posts from JSONPlaceholder API")
    posts_response = requests.get("https://jsonplaceholder.typicode.com/posts")
    posts_response.raise_for_status()
    posts = posts_response.json()

    # Fetch users from JSONPlaceholder API
    logging.info("Fetching users from JSONPlaceholder API")
    users_response = requests.get("https://jsonplaceholder.typicode.com/users")
    users_response.raise_for_status()
    users = users_response.json()

    logging.info(f"Fetched {len(posts)} posts and {len(users)} users")
    logging.info("Assets marked as updated - Databricks jobs will now trigger")

    return {
        "posts_count": len(posts),
        "users_count": len(users)
    }
