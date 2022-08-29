##


import asyncio
from functools import partial

import pandas as pd
from githubdata import GithubData
from mirutil import async_requests as areq
from mirutil import utils as mu
from mirutil.df_utils import save_df_as_a_nice_xl as snxl


dlist_url = 'https://github.com/imahdimir/Datasets'

rgburl = 'https://raw.github.com/'
gitburl = 'https://github.com/'

url = 'url'
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

def do_the_rest(df) :
  _df = df[[url]]
  _df = _df.drop_duplicates()

  _df[meturl] = _df[url].str.replace(gitburl , rgburl)
  _df[meturl] = _df[meturl] + '/main/META.json'

  cis = mu.return_clusters_indices(_df)

  _df = _df.reset_index(drop = True)

  for se in cis :
    print(se)

    si = se[0]
    ei = se[1]

    urls = _df.loc[si : ei , meturl]

    out = asyncio.run(read_main(urls))

    _df.loc[si : ei , desc] = out

  _df['Dataset'] = _df['url'].apply(get_dataset_name_from_url)

  c2k = {
      'Dataset' : None ,
      desc      : None ,
      'url'     : None ,
      meturl    : None ,
      }

  df1 = _df[c2k.keys()]

  snxl(df1 , 'repos-list.xlsx')

  _df['Dataset'] = '[' + _df['Dataset'] + '](' + _df[url] + ')'

  _df['Short Description'] = _df[desc]

  _df = _df[['Dataset' , 'Short Description']]

  _df.index = _df.index + 1

  rdme = '# Datasets List \n'
  rdme += _df.to_markdown()

  drp = GithubData(dlist_url)
  drp.clone()

  cur_repo_url = gitburl + drp.user_name + '/' + 'g-' + drp.repo_name

  rdmefp = drp.local_path / 'README.md'

  with open(rdmefp , 'w') as fi :
    fi.write(rdme)

  tokfp = '/Users/mahdi/Dropbox/tok.txt'
  tok = mu.get_tok_if_accessible(tokfp)

  msg = 'updated README.md'
  msg += ' by: ' + cur_repo_url

  drp.commit_and_push(msg , user = drp.user_name , token = tok)

  drp.rmdir()

def main() :
  pass

  ##


  df = pd.read_excel('repos-list.xlsx')

  ##
  do_the_rest(df)

  ##

  ##

##


if __name__ == '__main__' :
  main()
  print('done')


##