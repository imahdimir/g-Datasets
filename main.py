##

"""

  """

from githubdata import GithubData
import requests
import json


dlist_repo_url = 'https://github.com/imahdimir/d-Datasets-list'
cur_repo_url = 'https://github.com/imahdimir/gov-d-Datasets-list'

desc = 'description'
rgburl = 'https://raw.github.com/'
gitburl = 'https://github.com/'

def read_description_remove_from_meta(url) :
  print(url)

  r = requests.get(url)
  meta = r.json()

  if desc in meta.keys() :
    _desc = meta[desc]
  else :
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
  for url in djs.keys() :
    djs[url] = read_description_remove_from_meta(url)
  ##
  djsfp = drepo.meta_filepath
  with open(djsfp , 'w') as fi :
    json.dump(djs , fi)

  ##
  rdme = '| DataSet | Short Description |\n'
  rdme += '| --- | --- |\n'

  for ky , val in djs.items() :
    rpun = ky.replace(rgburl , '')
    rpunspl = rpun.split('/')
    rpun = '/'.join(rpunspl[:2])
    _url = gitburl + rpun
    rpn = rpunspl[1].split('d-' , 2)[1]
    nln = '| [' + rpn + '](' + _url + ') | ' + val + ' |\n'
    print(nln)
    rdme += nln
  ##
  rdmefp = drepo.local_path / 'README.md'

  with open(rdmefp , 'w') as fi :
    fi.write(rdme)
  ##
  msg = 'updated README.md'
  msg += ' by: ' + cur_repo_url

  drepo.commit_push(msg)

  ##
  drepo.rmdir()

  ##

##