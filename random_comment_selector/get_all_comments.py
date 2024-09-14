import requests
import json
from dotenv import load_dotenv
import os

def get_comment_author(comment_id, access_token):
    base_url = f"https://graph.facebook.com/{comment_id}"
    params = {
        "fields": "from",
        "access_token": access_token
    }
    response = requests.get(base_url, params=params)
    data = response.json()
    author_data = data.get("from", {})
    return author_data.get("username", "")

def get_comments(post_id, access_token):
    base_url = f"https://graph.facebook.com/{post_id}/comments"
    params = {
        "access_token": access_token
    }
    all_comments = []
    
    while True:
        response = requests.get(base_url, params=params)
        data = response.json()
        comments = data.get("data", [])
        for comment in comments:
            comment["username"] = get_comment_author(comment["id"], access_token)
        all_comments.extend(comments)
        
        if "paging" in data and "next" in data["paging"]:
            next_page_url = data["paging"]["next"]
            params = None
            # Parse next page URL to get new params
            url_parts = next_page_url.split("?")
            if len(url_parts) == 2:
                params = dict(p.split("=") for p in url_parts[1].split("&"))
        else:
            break
    
    return all_comments

def remove_entries_after_timestamp(comments, timestamp_to_keep):
    filtered_comments = []
    for comment in comments:
        comment_timestamp = comment.get("timestamp")
        if comment_timestamp and comment_timestamp <= timestamp_to_keep:
            filtered_comments.append(comment)
    return filtered_comments


def enumerate_comments(comments):
    enumerated_comments = []
    for i, comment in enumerate(comments, start=1):
        comment_with_number = {"entry_number": i}
        comment_with_number.update(comment) 
        enumerated_comments.append(comment_with_number)
    return enumerated_comments

def filter_comments_fields(comments, fields):
    filtered_comments = []
    for comment in comments:
        filtered_comment = {}
        for field in fields:
            if field in comment:
                filtered_comment[field] = comment[field]
            else:
                print(f"Field '{field}' not found in comment: {comment}")
        filtered_comments.append(filtered_comment)
    return enumerate_comments(filtered_comments)




def export_to_json(comments, file_name):
    with open(file_name, 'w', encoding='utf-8') as json_file:
        json.dump(comments, json_file, ensure_ascii=False, indent=4)

def main():
    # Get Values from .env file
    load_dotenv()
    post_id = os.getenv("POST_ID")
    access_token = os.getenv("ACCESS_TOKEN")
    timestamp_to_keep = os.getenv("TIME_TO_REMOVE")
    selected_fields_str = os.getenv("LIST_OF_VALUES")
    selected_fields = selected_fields_str.split(",") if selected_fields_str else []   

    # Do something
    comments = get_comments(post_id, access_token)

    timed_comments = remove_entries_after_timestamp(comments, timestamp_to_keep)

    filtered_comments = filter_comments_fields(timed_comments, selected_fields)

    export_to_json(filtered_comments, "../output/comments_with_usernames.json")

if __name__ == "__main__":
    main()


