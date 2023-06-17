def visCPD(cpd,scale=8):
  days = list(cpd.keys())
  bins = len(days)
  days.sort()
  counts = []
  for x in days:
    counts.append(cpd[x])
  step = max(counts)//scale
  strlen = (bins * 6) - 1
  currline = scale
  table= ["Commits Per day"] 
  margin = len(str(step)) + 1
  while(currline >= 0):
    label = str(step*currline)
    row = label+" "*((margin-len(label))+1)
    for x in counts:
      if x/step > currline:
        row += "  X   "
      else:
        row += "      "
    table.append(row[:-1].strip())
    currline -= 1
  table.append("-"*(strlen+margin))
  axis = " "*(margin + 1)
  for x in days:
    axis+=str(x.month).zfill(2)+"/"+str(x.day).zfill(2)+" "
  table.append(axis[:-1])
  print("\n".join(table)) 

def visCD(cd,scale=8):
  days = list(cd.keys())
  bins = len(days)
  days.sort()
  counts = []
  for x in days:
    counts.append(cd[x])
  step = max(counts)//scale
  strlen = (bins * 6) - 1
  currline = scale
  table= ["Checkout Days"] 
  margin = len(str(step)) + 1
  while(currline >= 0):
    label = str(step*currline)
    row = label+" "*((margin-len(label))+1)
    for x in counts:
      if x/step > currline:
        row += "  X   "
      else:
        row += "      "
    table.append(row[:-1].strip())
    currline -= 1
  table.append("-"*(strlen+margin))
  axis = " "*(margin + 1)
  for x in days:
    axis+=str(x.month).zfill(2)+"/"+str(x.day).zfill(2)+" "
  table.append(axis[:-1])
  print("\n".join(table)) 
