import requests
import json
import re
from dotenv import dotenv_values
from datetime import datetime,timedelta
from sys import exit
from pathlib import Path

config = dotenv_values(".env")
token = config['GITHUB_TOKEN']
url = config['BASE_ORG_URL']

headers = {
  "Accept":"application/vnd.github+json",
  "Authorization":"Bearer "+token,
  "X-GitHub-Api-Version":"2022-11-28"}

parameters = {"per_page":'100'}
r = requests.head(url, headers=headers, params=parameters)
pages = int((re.search(r'=(\d+)$', r.links['last']['url']).group(1)))

time_re = re.compile('(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})T(?P<hour>\d{2}):(?P<minu>\d{2}):(?P<sec>\d{2})Z')

OFFSET = 4

def check_rate_limit():
  r = requests.get("https://api.github.com/rate_limit", headers=headers).json()
  return int(r["rate"]["remaining"]) 

def commit_histories(name,assignment):
  comurl = config['BASE_COMMIT_URL']+name+"/commits"
  if not check_rate_limit() > 0:
    print("Rate Limit exceeded, try again later")
    exit(1)
  r = requests.get(comurl, headers=headers).json()
  commits = []
  for commit in r:
    time = (commit['commit']['author']['date']) 
    commits.append(str(convertTime(time)))


  Path(assignment).mkdir(exist_ok=True, parents=True)
  with open(assignment+"/"+name+".history", 'w') as f: 
      for time in commits: 
          f.write('%s:%s\n' % (name, time))
  return commits
  
def convertTime(a):
  data = re.search(time_re,a)
  init = datetime(int(data.group('year')),int(data.group('month')),int(data.group('day')),int(data.group('hour')),int(data.group('minu')),int(data.group('sec')))
  td = timedelta(hours=OFFSET)
  return init - td

def start():
  repos = {}
  for i in range(pages):
    page = {'page':i+1}
    page.update(parameters)
    if not check_rate_limit() > 0:
      print("Rate Limit exceeded, try again later")
      exit(1)
    r = requests.get(url, headers=headers, params=page).json()
    for repo in r:
      user = repo['name']
      checkedout = repo['created_at']
      # forgot to convert to edt
      newtime = convertTime(checkedout)      
      repos[user] = str(newtime)

  with open("checkout.txt", 'w') as f: 
    for key, value in repos.items(): 
      #commit_histories(key)
      f.write('%s:%s\n' % (key, value))
#start()

def project_histories(assignment):
  assign_len = len(assignment)
  with open("checkout.txt", 'r') as f: 
    for line in f:
      if assignment+"-" == line[:assign_len+1]:
        commit_histories(line.split(":")[0],assignment)

#project_histories("project-1")
