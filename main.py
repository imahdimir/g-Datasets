##

"""

  """


import pandas as pd
from githubdata import GithubData
import requests
import json

dlist_repo_url = 'https://github.com/imahdimir/d-Datasets-list'
cur_repo_url =

desc = 'description'




def clone_read_description_remove(url):
  print(url)

  r = requests.get(url)
  meta = r.json()

  if desc in meta.keys():
    _desc = meta[desc]
  else:
    _desc = None

  return _desc


def main() :
  pass

  ##
  drepo = GithubData(dlist_repo_url)
  drepo.clone()
  ##
  djs = drepo.meta
  ##
  for url in djs.keys():
    djs[url] = clone_read_description_remove(url)
  ##
  djsfp = drepo.meta_filepath
  with open(djsfp, 'w') as fi:
    json.dump(djs, fi)
  ##
  msg = 'read meta files'
  drepo.commit_push(msg)
  ##
  drepo.rmdir()
  ##









  ##



##
##