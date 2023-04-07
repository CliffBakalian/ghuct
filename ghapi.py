import requests
import json
import re
from dotenv import dotenv_values

config = dotenv_values(".env")
token = config['GITHUB_TOKEN']
url = config['BASE_URL']

headers = {
  "Accept":"application/vnd.github+json",
  "Authorization":"Bearer "+token,
  "X-GitHub-Api-Version":"2022-11-28"}

parameters = {"per_page":'100'}
r = requests.head(url, headers=headers, params=parameters)
pages = int((re.search(r'=(\d+)$', r.links['last']['url']).group(1)))

repos = {}
for i in range(pages):
  page = {'page':i+1}
  page.update(parameters)
  r = requests.get(url, headers=headers, params=page).json()
  for repo in r:
    user = repo['name']
    checkedout = repo['created_at']
    repos[user] = checkedout

