##


import asyncio
from ast import literal_eval

import nest_asyncio
import pandas as pd
from aiohttp import ClientSession
from githubdata import GithubData
from mirutil import funcs as mf


nest_asyncio.apply()

dlist_repo_url = 'https://github.com/imahdimir/Datasets'

rgburl = 'https://raw.github.com/'
gitburl = 'https://github.com/'

desc = 'description'
meturl = 'metaurl'
meta = 'meta'

async def get_json_by_its_url(url) :
  async with ClientSession() as ses :
    async with ses.get(url) as resp :
      return await resp.json(content_type = None)

async def a_task(url) :
  jsn = await get_json_by_its_url(url)
  return await read_desc_in_meta_jsn(jsn)

async def read_desc_in_meta_jsn(jsn) :
  if desc in jsn.keys() :
    return jsn[desc]
  else :
    return None

async def read_main(urls) :
  tasks = [a_task(x) for x in urls]
  return await asyncio.gather(*tasks)

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

  ##
  df[meturl] = df[0].str.replace(gitburl , rgburl)
  df[meturl] = df[meturl] + '/main/META.json'

  ##
  cis = mf.return_clusters_indices(df)

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
  msg = 'updated README.md'
  msg += ' by: ' + cur_repo_url

  drp.commit_push(msg)

  ##


  drp.rmdir()

  ##


  ##


##

##