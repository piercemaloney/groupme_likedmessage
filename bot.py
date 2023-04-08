"""
Created by Pierce Maloney

Bot to get a list of users that liked a particular message.
"""

import requests
from hidden import access_token

def get_group_id(access_token, group_name):
    url = "https://api.groupme.com/v3/groups"
    params = {"token": access_token}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()["response"]
        for group in data:
            if group["name"] == group_name:
                return group["id"]
    else:
        print("Error retrieving group list: {}".format(response.text))
    
    # If no group with the given name was found, return None
    return None

def get_message_id(access_token, group_id, search_string):
    """
    Returns the message id of the most recent msg containing search_string
    """
    url = f'https://api.groupme.com/v3/groups/{group_id}/messages'
    params = {"token": access_token, "limit": 100}  # Limit to 100 messages to reduce response size
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()["response"]["messages"]
        for message in data:
            if search_string in message["text"]:
                return message["id"]
    else:
        print("Error retrieving messages: {}".format(response.text))
    
    # If no message containing the search string was found, return None
    return None

def get_favorited_userids(access_token, group_id, message_id):
    url = "https://api.groupme.com/v3/groups/{}/messages/{}".format(group_id, message_id)
    params = {"token": access_token}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()["response"]["message"]["favorited_by"]
        return data
    else:
        print("Error retrieving favorited user ids: {}".format(response.text))
        return None

def get_group_members_dict(access_token, group_id):
    url = "https://api.groupme.com/v3/groups/{}".format(group_id)
    params = {"token": access_token}
    response = requests.get(url, params=params)

    if response.status_code == 200:
        members = {}
        for member in response.json()["response"]['members']:
            members[member["user_id"]] = member["nickname"]
        return members
    else:
        print("Error retrieving member data: {}".format(response.text))
        return None

# final function
def get_liked_by(access_token, group_name, message_text):
    group_id = get_group_id(access_token, group_name)
    message_id = get_message_id(access_token, group_id, message_text)
    user_ids = get_favorited_userids(access_token, group_id, message_id)
    members = get_group_members_dict(access_token, group_id)
    nicknames = []
    for user_id in user_ids:
        nicknames.append(members.get(user_id, 'unknown'))
    return nicknames


def main():
    group_name = 'Dudes 2k22'
    
    # Get the message text from the user
    message_text = input("Enter the message text: ")

    # Get a list of nicknames of people who liked the message
    nicknames = get_liked_by(access_token, group_name, message_text)

    # Print the list of nicknames
    print("People who liked the message:")
    for nickname in nicknames:
        print(nickname)

if __name__ == '__main__':
    main()