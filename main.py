##


import asyncio
from functools import partial

import pandas as pd
from githubdata import GithubData
from mirutil import async_requests as areq
from mirutil import utils as mu
from mirutil.df_utils import save_df_as_a_nice_xl as snxl


dlist_repo_url = 'https://github.com/imahdimir/Datasets'

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


def main() :
  pass

  ##
  drp = GithubData(dlist_repo_url)
  drp.clone()

  ##
  cur_repo_url = 'https://github.com/' + drp.user_name + '/' + 'gov-' + drp.repo_name

  ##
  df = pd.read_excel('repos-list.xlsx')

  ##
  df = df[[url]]
  df = df.drop_duplicates()

  ##
  df[meturl] = df[url].str.replace(gitburl , rgburl)
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
  df['Dataset'] = df['url'].apply(get_dataset_name_from_url)

  ##
  c2k = {
      'Dataset' : None ,
      desc : None ,
      'url' : None ,
      meturl : None ,
      }

  df1 = df[c2k.keys()]

  ##
  snxl(df1 , 'repos-list.xlsx')

  ##
  df['Dataset'] = '[' + df['Dataset'] + '](' + df[url] + ')'

  ##
  df['Short Description'] = df[desc]

  ##
  df = df[['Dataset' , 'Short Description']]

  ##
  df.index = df.index + 1

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

  drp.commit_and_push(msg , user = drp.user_name , token = tok)

  ##


  drp.rmdir()

  ##

  ##

##


if __name__ == '__main__' :
  main()
  print('done')


##