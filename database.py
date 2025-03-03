import re
from datetime import date,timedelta,datetime,time
from dotenv import dotenv_values
from sys import exit
import glob,pickle
DAYLIGHTS=True

def get_dates(assignment):
  start = None
  end = None
  staff_commits=[]
  try:
    with open(assignment+"/config") as f:
      for line in f:
        matched1 = re.search(r'Release: (\d\d)-(\d\d)-(\d{4})',line)
        matched2 = re.search(r'Due: (\d\d)-(\d\d)-(\d{4})',line)
        matched3 = re.search(r'Late: (\d\d)-(\d\d)-(\d{4})',line)
        matched4 = re.search(r'STAFF: (\d{4})-(\d\d)-(\d\d) (\d{2}):(\d{2}):(\d{2})',line)
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
        elif matched4:
          '''
          month = int(matched4.group(2))
          day   = int(matched4.group(3))
          year  = int(matched4.group(1))
          hour  = int(matched4.group(4))
          minute= int(matched4.group(5))
          sec   = int(matched4.group(6))
          staff_commits.append(datetime(year,month,day,hour,minute,sec))
          '''
          staff_commits.append(line[7:].strip())
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
  return (ret,due,staff_commits)

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
  days,due,staff = get_dates(assignment)
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
  return cpd,cd,cph,fc,tc,staff

'''
for each person 
  + add their commits per day to databse
  + add thier commits per hour to database
  + make personal database of commits per hour
  + figure out how when they started
  + figure out how many days they worked
  + figure out how many commits they made total
'''
def process_person(repo,assignment,database,staff=[]):
  a = get_times()
  personal_times = {}
  for x in a:
    personal_times[x] = 0
  count = 0
  first_commit = None
  checkout_day = None
  last_day = None
  count = 0
  with open(assignment+"/"+repo+".history") as f:
    d = None
    for line in f:
      matched = re.search(r'created:(\d{4})-(\d\d)-(\d\d).(\d\d):(\d\d)',line)
      if matched:
        year  = int(matched.group(1))
        month = int(matched.group(2))
        day   = int(matched.group(3))
        hour  = int(matched.group(4))
        minute= int(matched.group(5))
        d = date(month=month,day=day,year=year)
        if DAYLIGHTS:
          dt = datetime(year,month,day,hour,minute,0)
          new_d = dt - timedelta(hours=1)
          d = date(new_d.year,new_d.month,new_d.day)
        try:
          database['cd'][d] += 1
        except:
          database['cd'][d] = 1
      else:
        matched = re.search(r':(\d{4})-(\d\d)-(\d\d).(\d\d):(\d\d):(\d\d)',line)
        if matched:
          year  = int(matched.group(1))
          month = int(matched.group(2))
          day   = int(matched.group(3))
          hour  = int(matched.group(4))
          minute= int(matched.group(5))
          d = date(month=month,day=day,year=year)
          if matched.group(0)[1:] in staff:
            continue
          if DAYLIGHTS:
            dt = datetime(year,month,day,hour,minute,0)
            new_d = dt - timedelta(hours=1)
            d = date(new_d.year,new_d.month,new_d.day)
          try:
            database['cpd'][d] += 1
          except KeyError:
            d = None
          if count == 0:
            last_day = d
          if count == 1:
            try:
              database['fc'][d] += 1
            except KeyError:
              #print("Ignoring date:" + str(date(month=month,day=day,year=year)))
              3
          hour = int(matched.group(4))
          mins = int(matched.group(5))
          t = time(hour=hour,minute=(mins//30)*30,second=0)
          if DAYLIGHTS:
            dt = datetime.combine(date.today(), t) - timedelta(hours=1)
            t = dt.time()
          database['cph'][t] += 1
          personal_times[t] +=1
          count += 1
    '''
    if d and last_day: 
      database['cd'][d] += 1
      days_worked = 0
    else:
      days_worked = 0
    '''
    days_worked = 0
    database['tc'][repo] = count
    if first_commit and last_day:
      days_testing= (last_day - first_commit).days
    else:
      days_testing=1
  return count,days_worked,personal_times,days_testing

def mkDataBase(assignment):
  database = {}
  a,b,c,d,e,staff = init_data_base(assignment)
  database['cpd'] = a #commits per day
  database['cd'] = b #checkout day
  database['cph'] = c #commits per hour
  database['fc'] = d #first commit
  database['tc'] = e #total commits?
  
  ext = ".history"
  soffset = len(assignment)
  eoffset = len(ext)

  for person in glob.glob(assignment+"/*"+ext):
    process_person(person[soffset:-eoffset],assignment,database,staff)  
  #get_checkout_days(database)
  return database

#def get_checkout_days(database):
  #with open("checkout.txt") as f:
    
    

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
