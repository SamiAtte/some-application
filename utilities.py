

def multi_list(query,ixt):
  mlist = []
  if query:
    for x in query:
      element = []
      for i in ixt:
        element.append(x[i])
      mlist.append(element)
  return mlist


