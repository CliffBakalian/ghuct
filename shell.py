from database import *
from visualizer import *
import ghapi

def updateHistories(assignment):
  ghapi.project_histories(assignment) 

def updateRepoList():
  ghapi.start() 

def update_assignment_database(assignment):
  update(assignment) 

visCPD(getCPD("project-1"))
visCD(getCD("project-1"))
