##


import asyncio
from ast import literal_eval
from functools import partial

import pandas as pd
from githubdata import GithubData
from mirutil import async_requests as areq
from mirutil import utils as mu


dlist_repo_url = 'https://github.com/imahdimir/Datasets'

rgburl = 'https://raw.github.com/'
gitburl = 'https://github.com/'

desc = 'description'
meturl = 'metaurl'
meta = 'meta'


def read_desc_in_meta_jsn(jsn) :
  if desc in jsn.keys() :
    return jsn[desc]
  else :
    return None


async def read_main(urls) :
  fu = partial(areq.get_reps_jsons_async ,
               trust_env = False ,
               params = None ,
               verify_ssl = True ,
               content_type = None)
  jsns = await fu(urls)
  out = [read_desc_in_meta_jsn(x) for x in jsns]
  return out


def get_dataset_name_from_url(url) :
  repon = url.split('/')[-1]
  return repon.split('d-' , 1)[1]


def main() :
  pass

  ##

  drp = GithubData(dlist_repo_url)
  drp.clone()

  ##
  cur_repo_url = 'https://github.com/' + drp.usr + '/' + 'gov-' + drp.repo_name

  ##
  with open('META.json' , 'r') as fi :
    jstxt = fi.read()

  js = literal_eval(jstxt)

  ##
  df = pd.DataFrame(data = js.keys())
  df = df.drop_duplicates()

  ##
  df[meturl] = df[0].str.replace(gitburl , rgburl)
  df[meturl] = df[meturl] + '/main/META.json'

  ##
  cis = mu.return_clusters_indices(df)

  ##
  df = df.reset_index(drop = True)

  for se in cis :
    print(se)

    si = se[0]
    ei = se[1]

    urls = df.loc[si : ei , meturl]

    out = asyncio.run(read_main(urls))

    df.loc[si : ei , desc] = out

  ##
  df['Dataset'] = df[0].apply(get_dataset_name_from_url)
  df['Dataset'] = '[' + df['Dataset'] + '](' + df[0] + ')'

  ##
  df['Short Description'] = df[desc]

  ##
  df = df[['Dataset' , 'Short Description']]

  ##
  rdme = '# Datasets List \n'
  rdme += df.to_markdown()

  ##
  rdmefp = drp.local_path / 'README.md'

  with open(rdmefp , 'w') as fi :
    fi.write(rdme)

  ##
  tokfp = '/Users/mahdi/Dropbox/tok.txt'
  tok = mu.get_tok_if_accessible(tokfp)

  ##
  msg = 'updated README.md'
  msg += ' by: ' + cur_repo_url

  drp.commit_push(msg , usr = drp.usr , token = tok)

  ##

  drp.rmdir()

  ##


  ##


##

##