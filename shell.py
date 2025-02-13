from database import *
from visualizer import *
import ghapi
import sys

def updateHistories(assignment):
  ghapi.project_histories(assignment) 

def updateRepoList():
  ghapi.start() 

def update_assignment_database(assignment):
  update(assignment) 

commands = ["update","help","vis"]
update_com = ["repos", "history", "db"]
vis_com = ["cpd", "cd", "cph","fc"]
help_msg = "useage: shell.py <command> [args]\n\n" + \
           "Commands:\n\n" + \
           "help: show this message\n\n" + \
           "update <argument>: will update the backend structures\n" + \
           "\tArguments:\n" + \
           "\trepos: will update all repos in the org\n" + \
           "\thistory <assignment>: will update all historys for the given assignment\n" + \
           "\tdb <assignment>: will update all database or counts for the given assignment\n" + \
           "\t<assignment>: will update repos, history and databse for the given assignment\n\n" + \
           "vis <argument>: will print our graphs for a given assignment\n" + \
           "\tArguments:\n" + \
           "\tcpd <assignment>: will show how many commits occured each day of the project\n" + \
           "\tcd <assignment>: will show how many people checked out the poject each day\n" + \
           "\tcph <assignment>: will show how many commits occured each half hour during all days of the project\n" + \
           "\tfc <assignment>: will show when the first student commit was created (this typically means first submit time to Gradescope).\n" + \
           "\t<assignment>: will pring all graphs for the given assignment"

if __name__ == "__main__":
  alen = len(sys.argv)
  if alen <= 1:
    print(help_msg)
    sys.exit(1)

  if sys.argv[1] == "update":
    if alen  <= 2:
      print("need an assignment to update") 
      sys.exit(2)
    arg = sys.argv[2]
    if arg in update_com:
      if arg == "repos":
        print("updating repos in org")
        updateRepoList()
      elif  arg == "history":
        if len(sys.argv) > 3:
          print("updating history of "+sys.argv[3])
          updateHistories(sys.argv[3])
        else:
          print("need an assignment to update")
          sys.exit(2)
      elif arg == "db":
        print("updating datebase of "+sys.argv[3])
        update_assignment_database(sys.argv[3])
      else:
        print("this should never be seen")
        sys.exit(3)
      print("updated")
    else:
      print("updating it all")
      updateRepoList()
      updateHistories(arg)
      update_assignment_database(arg)
      print("updated")

  elif sys.argv[1] == "vis":
    if alen  <= 2:
      print("need an assignment to visualize") 
      sys.exit(2)
    arg = sys.argv[2]
    if arg in update_com and alen <= 3:
      print("need an assignment to visualize")
      sys.exit(2)
    if arg in vis_com and alen > 2:
      ass = sys.argv[3]
      if arg == "cpd":
        a = getCPD(ass)
        print(visCPD(a))
      elif  arg == "cd":
        b = getCD(ass)
        print(visCD(b))
      elif arg == "cph":
        c = getCPH(ass)
        print(visCPH(c))
      elif arg == "fc":
        d = getFC(ass)
        print(visFC(d))
      else:
        print("this should never be seen")
        sys.exit(2)
    else:
      a = getCPD(arg)
      b = getCD(arg)
      c = getCPH(arg)
      d = getFC(arg)
      print(visCPD(a))
      print(visCD(b))
      print(visCPH(c))
      print(visFC(d))
  elif sys.argv[1] == "help":
    print(help_msg)
