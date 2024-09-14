import json
import random

def select_random_comment(file_name):
    with open(file_name, 'r', encoding='utf-8') as json_file:
        comments = json.load(json_file)
        return random.choice(comments)

def main():
    random_comment = select_random_comment("comments_with_usernames.json")
    if random_comment:
        print("Random Comment:", random_comment)
    else:
        print("There was no random comment selected.")

if __name__ == "__main__":
    main()
