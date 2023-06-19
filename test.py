from database import *
def testCliff():
  database = {}
  assignment="project-1"
  repo = "project-1-CliffBakalian"
  a,b,c = init_data_base(assignment)
  database['cpd'] = a
  database['cd'] = b
  database['cph'] = c
  checkout_day,commits,days_worked,d = process_person(repo,assignment,database)
  assert(checkout_day == date(year=2023,day=6,month=6))
  assert(commits == 3)
  assert(days_worked == 4)
  assert(d[time(hour=23,minute=30,second=0)] == 2)
  assert(d[time(hour=22,minute=30,second=0)] == 1)
  t = 0
  for x in d:
    t+=d[x] 
  assert(t == 3)
  
def test():
  times = get_times()
  start1 = times[0]
  end1 = times[1]
  assert (start1 < time(hour=0,minute=23,second=0) < end1 )
  assert not (start1 < time(hour=1,minute=23,second=0) < end1 )

test()
testCliff()
