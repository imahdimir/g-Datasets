"""

  """
##
import asyncio
from functools import partial

import pandas as pd
import requests
from bs4 import BeautifulSoup
from githubdata import GithubData
from mirutil import async_requests as areq
from mirutil import utils as mu
from mirutil.df_utils import save_df_as_a_nice_xl as snxl


class Url :
    targ = 'https://github.com/imahdimir/Datasets'
    src = 'https://github.com/stars/imahdimir/lists/datasets'
    cur = 'https://github.com/imahdimir/g-Datasets'

url = Url()

class Constant :
    raw_github_url = 'https://raw.github.com/'
    github_base_url = 'https://github.com/'

cte = Constant()

class ColNames :
    relurl = 'relurl'
    url = 'url'
    desc = 'description'
    meturl = 'metaurl'
    meta = 'meta'
    dataset = 'Dataset'
    short = 'Short Description'

cn = ColNames()

def read_desc_in_meta_jsn(jsn) :
    if cn.desc in jsn.keys() :
        return jsn[cn.desc]
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

    resp = requests.get(url.src)
    ##
    # with open('resp.txt' , 'w') as fi :
    #     fi.write(resp.text)

    ##
    soup = BeautifulSoup(resp.text , "html.parser")
    ##
    la = soup.body.find_all('a')
    la = [x for x in la if x.has_attr('href') and not x.has_attr('class')]
    ##
    df = pd.DataFrame()
    df[cn.relurl] = [x['href'] for x in la]
    ##
    df['spl'] = df[cn.relurl].str.split('/')
    ##
    ptr = 'd-'
    msk = df['spl'].apply(lambda x : x[-1].startswith(ptr))

    df1 = df[msk]
    del df
    ##
    df1 = df1[[cn.relurl]]
    ##
    df1[cn.url] = cte.github_base_url + df1[cn.relurl]
    df1[cn.meturl] = cte.raw_github_url + df1[cn.relurl] + '/main/META.json'
    ##
    df1 = df1[[cn.url , cn.meturl]]
    ##
    cis = mu.return_clusters_indices(df1)
    ##
    for se in cis :
        si = se[0]
        ei = se[1] + 1
        print(se)

        inds = df1.index[si :ei]

        urls = df1.loc[inds , cn.meturl]

        out = asyncio.run(read_main(urls))

        df1.loc[inds , cn.desc] = out
    ##
    df1[cn.dataset] = df1[cn.url].apply(get_dataset_name_from_url)
    ##
    c2k = {
            cn.dataset : None ,
            cn.desc    : None ,
            cn.url     : None ,
            cn.meturl  : None ,
            }

    df1 = df1[c2k.keys()]
    ##
    df2 = df1.copy()
    ##
    df1[cn.dataset] = '[' + df1[cn.dataset] + '](' + df1[cn.url] + ')'
    ##
    df1[cn.short] = df1[cn.desc]
    df1 = df1[[cn.dataset , cn.short]]
    ##
    df1.reset_index(drop = True , inplace = True)
    df1.index = df1.index + 1
    ##
    rdme = '# Datasets List \n'
    rdme += df1.to_markdown()
    ##
    rp_targ = GithubData(url.targ)
    rp_targ.clone()
    ##
    rdmefp = rp_targ.local_path / 'README.md'
    with open(rdmefp , 'w') as fi :
        fi.write(rdme)
    ##
    fp = rp_targ.local_path / 'list.xlsx'
    snxl(df2 , fp)
    ##
    msg = 'updated README.md'
    msg += ' by: ' + url.cur
    ##
    rp_targ.commit_and_push(msg)
    ##
    rp_targ.rmdir()

    ##

##

##
if __name__ == '__main__' :
    main()

##

##
