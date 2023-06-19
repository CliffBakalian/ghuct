from database import *
from visualizer import *
import ghapi

def updateHistories(assignment):
  ghapi.project_histories(assignment) 

def updateRepoList():
  ghapi.start() 

def update_assignment_database(assignment):
  update(assignment) 

ass = "example_assignment"
updateRepoList()
updateHistories(ass)
update_assignment_database(ass)
a = getCPD(ass)
print(visCPD(a))
b = getCD(ass)
print(visCD(b))
c = getCPH(ass)
print(visCPH(c))
