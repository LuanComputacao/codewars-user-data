import csv
import json
from os import makedirs, path

import requests
from environs import Env


def main():
    env = Env()
    env.read_env()
    base_url = 'https://www.codewars.com/api/v1'
    usernames = get_usernames(env('USERNAMES_CSV'))
    api_key = 'zuz793X919sYiwHxNyoB'

    if env.bool('DOWNLOAD_DATA'):
        get_user_data(api_key, base_url, usernames)
        get_completed_challenges(api_key, base_url, usernames)

    process_users_completed_challanges(usernames, env('LANGUAGE'))


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
            f.write(json.dumps(student_data, indent=2))


def get_completed_challenges(api_key, base_url, usernames):
    for username in usernames:
        response = requests.get(
            f'{base_url}/users/{username}/code-challenges/completed',
            headers={
                'Authorization': api_key})
        user_data = response.json()
        user_dir = f'output/{username}'
        if not path.isdir(user_dir):
            makedirs(user_dir)
        with open(f'{user_dir}/completed_challenges.json', 'w') as f:
            f.write(json.dumps(user_data, indent=2))


def process_users_completed_challanges(usernames, language):
    challenges_ids_set = set()
    ranking = []
    clean_codewars_file()

    for username in usernames:
        with open(f'output/{username}/completed_challenges.json') as f:
            challenges_data = json.loads(f.read())
            challenges_data = [challenge for challenge in challenges_data['data']
                               if language in challenge['completedLanguages']]
            ranking.append((username, len(challenges_data)))
            for challenge in challenges_data:
                if challenge['id'] not in challenges_ids_set:
                    challenges_ids_set.add(challenge['id'])
                    store_codewar(
                        challenge['id'],
                        challenge['slug'],
                        challenge['name'],
                        language)

    store_ranking(ranking)

def store_ranking(ranking):
    ranking.sort(key=lambda x: x[1])
    ranking.reverse()
    fieldnames = ['username', 'katas']

    with open('output/ranking.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for line in ranking:
           writer.writerow(dict(zip(fieldnames, line)))

def clean_codewars_file():
    with open('output/codewars.csv', 'w') as f:
        f.write('id,slug,name,link')


def store_codewar(id, slug, name, language):
    fieldnames = ['id', 'slug', 'name', 'link']
    base_url = 'https://www.codewars.com/kata'
    data = [
        id,
        slug,
        name,
        f'{base_url}/{slug}/{language}'
    ]
    with open('output/codewars.csv', 'a+') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(dict(zip(fieldnames, data)))


if __name__ == '__main__':
    main()
