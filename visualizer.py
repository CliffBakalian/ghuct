import re
from datetime import date,timedelta,datetime,time
from dotenv import dotenv_values
from sys import exit

def get_dates(assignment):
  start = None
  end = None
  with open(assignment+"/config") as f:
    for line in f:
      matched1 = re.search(r'Release: (\d\d)-(\d\d)-(\d{4})',line)
      matched2 = re.search(r'Due: (\d\d)-(\d\d)-(\d{4})',line)
      matched3 = re.search(r'Late: (\d\d)-(\d\d)-(\d{4})',line)
      if matched1:
        month = int(matched1.group(1))
        day   = int(matched1.group(2))
        year  = int(matched1.group(3))
        start = date(month=month,day=day,year=year)
      elif matched2:
        month = int(matched2.group(1))
        day   = int(matched2.group(2))
        year  = int(matched2.group(3))
        if not end:
          end = date(month=month,day=day,year=year)
        due = date(month=month,day=day,year=year)
      elif matched3:
        month = int(matched3.group(1))
        day   = int(matched3.group(2))
        year  = int(matched3.group(3))
        end = date(month=month,day=day,year=year)
  if not(start and end):
    print("malformed config file")
    exit(1)     
  ret = [start]
  curr = start
  while (curr != end):
    curr = curr + timedelta(days=1)
    ret.append(curr)
  return (ret,due)

def get_times():
  ret = []
  now =datetime.now()
  curr = datetime(year=now.year,month=1,day=1,hour=0,minute=0,second=0)
  for x in range(48):
    ret.append(curr.time())
    curr = curr + timedelta(minutes=30)
  return ret

'''
returns commits_per_day [day] -> count x commits occured this day
returns checkout_day [day] -> count x people checked out on this day
returns commits_per_hr [time] -> count x commits occured within 30 mins of time
'''
def mkDataBase(assignment):
  days,due = get_dates(assignment)
  times = get_times()
  cpd = {}
  cd = {}
  cph  = {}
  for x in days:
    cpd[x] = 0
    cd[x] = 0
  for x in times:
    cph[x] = 0
  return cpd,cd,cph

'''
for each person 
  + add their checkout day to database
  + add their commits per day to databse
  + add thier commits per hour to database
  + make personal database of commits per hour
  + figure out how when they started
  + figure out how many days they worked
  + figure out how many commits they made total
'''
def process_person(repo,assignment,database):
  a = get_times()
  personal_times = {}
  for x in a:
    personal_times[x] = 0
  count = 0
  checkout_day = None
  last_day = None
  count = 0
  with open(assignment+"/"+repo+".history") as f:
    for line in f:
      matched = re.search(r':(\d{4})-(\d\d)-(\d\d).(\d\d):(\d\d)',line)
      if matched:
        year  = int(matched.group(1))
        month = int(matched.group(2))
        day   = int(matched.group(3))
        d = date(month=month,day=day,year=year)
        database['cpd'][d] += 1
        if count == 0:
          last_day = d

        hour = int(matched.group(4))
        mins = int(matched.group(5))
        t = time(hour=hour,minute=(mins//30)*30,second=0)
        database['cph'][t] += 1
        personal_times[t] +=1
        count += 1
    database['cd'][d] += 1
    checkout_day = d
    days_worked = (last_day - checkout_day).days
  return checkout_day,count,days_worked,personal_times

#project-1-CliffBakalian:2023-06-10 23:36:18

def testCliff():
  database = {}
  assignment="project-1"
  repo = "project-1-CliffBakalian"
  a,b,c = mkDataBase(assignment)
  database['cpd'] = a
  database['cd'] = b
  database['cph'] = c
  checkout_day,commits,days_worked,d = process_person(repo,assignment,database)
  #print(database['cpd'])
  #print(database['cd'])
  #print(database['cph'])
  assert(checkout_day == date(year=2023,day=6,month=6))
  assert(commits == 3)
  assert(days_worked == 4)
  #print(d)
  
def test():
  times = get_times()
  start1 = times[0]
  end1 = times[1]
  assert (start1 < time(hour=0,minute=23,second=0) < end1 )
  assert not (start1 < time(hour=1,minute=23,second=0) < end1 )

test()
testCliff()
