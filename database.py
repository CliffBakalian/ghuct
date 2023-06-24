import re
from datetime import date,timedelta,datetime,time
from dotenv import dotenv_values
from sys import exit
import glob,pickle

def get_dates(assignment):
  start = None
  end = None
  try:
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
  except:
    print("config file needs to be written. Was this init?")
    exit(1)
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
def init_data_base(assignment):
  days,due = get_dates(assignment)
  times = get_times()
  cpd = {}
  cd = {}
  cph  = {}
  fc = {}
  tc = {}
  for x in days:
    cpd[x] = 0
    cd[x] = 0
    fc[x] = 0
  for x in times:
    cph[x] = 0
  return cpd,cd,cph,fc,tc

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
  first_commit = None
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
        if count == 1:
          first_commit = d
          database['fc'][d] += 1
        hour = int(matched.group(4))
        mins = int(matched.group(5))
        t = time(hour=hour,minute=(mins//30)*30,second=0)
        database['cph'][t] += 1
        personal_times[t] +=1
        count += 1
    database['cd'][d] += 1
    database['tc'][repo] = count
    checkout_day = d
    days_worked = (last_day - checkout_day).days
    if first_commit:
      days_testing= (last_day - first_commit).days
    else:
      days_testing=1
  return checkout_day,count,days_worked,personal_times,days_testing

def mkDataBase(assignment):
  database = {}
  a,b,c,d,e = init_data_base(assignment)
  database['cpd'] = a
  database['cd'] = b
  database['cph'] = c
  database['fc'] = d
  database['tc'] = e
  
  ext = ".history"
  soffset = len(assignment)
  eoffset = len(ext)

  for person in glob.glob(assignment+"/*"+ext):
    process_person(person[soffset:-eoffset],assignment,database)  
  return database

def save(assignment,database):
  with open(assignment+'.pickle', 'wb') as handle:
    pickle.dump(database, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load(assignment):
  with open(assignment+'.pickle', 'rb') as handle:
    database = pickle.load(handle)
  return database

def getCPD(assignment):
  db = load(assignment)
  return db['cpd']

def getCD(assignment):
  db = load(assignment)
  return db['cd']

def getCPH(assignment):
  db = load(assignment)
  return db['cph']

def getFC(assignment):
  db = load(assignment)
  return db['fc']

def getTC(assignment):
  db = load(assignment)
  return db['tc']

def update(assignment):
  db = mkDataBase(assignment)
  save(assignment,db)
