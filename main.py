# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool
# windows, actions, and settings.
import json
import csv
from os import makedirs, path
from environs import Env


import requests


def main():
    env = Env()
    env.read_env()
    base_url = 'https://www.codewars.com/api/v1'
    usernames = get_usernames(env('USERNAMES_CSV'))
    api_key = 'zuz793X919sYiwHxNyoB'

    get_user_data(api_key, base_url, usernames)

    get_completed_challenges(
        api_key,
        base_url,
        usernames)


def get_usernames(usernames_file):
    with open(usernames_file, 'r') as f:
        return [user['username'] for user in csv.DictReader(f)]


def get_user_data(api_key, base_url, usernames):
    for username in usernames:
        print(username)
        response = requests.get(
            f'{base_url}/users/{username}',
            headers={
                'Authorization': api_key})
        student_data = response.json()
        user_dir = f'output/{username}'
        if not path.isdir(user_dir):
            makedirs(user_dir)
        with open(f'{user_dir}/userdata.json', 'w') as f:
            f.write(json.dumps(student_data))


def get_completed_challenges(api_key, base_url, usernames):
    for username in usernames:
        print(username)
        response = requests.get(
            f'{base_url}/users/{username}/code-challenges/completed',
            headers={
                'Authorization': api_key})
        user_data = response.json()
        user_dir = f'output/{username}'
        if not path.isdir(user_dir):
            makedirs(user_dir)
        with open(f'{user_dir}/completed_challenges.json', 'w') as f:
            f.write(json.dumps(user_data))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
