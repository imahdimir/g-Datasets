"""

  """

import asyncio
import json
from functools import partial

import pandas as pd
import requests
from bs4 import BeautifulSoup
from githubdata import GithubData
from mirutil.async_requests import get_reps_jsons_async as fu0
from mirutil.df_utils import save_df_as_a_nice_xl as snxl
from mirutil.utils import ret_clusters_indices


class GDUrl :
    with open('gdu.json' , 'r') as fi :
        gj = json.load(fi)

    selff = gj['selff']
    trg = gj['trg']

gu = GDUrl()

class Constant :
    src = 'https://github.com/stars/imahdimir/lists/datasets'
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

c = ColNames()

def read_desc_in_meta_jsn(jsn) :
    if c.desc in jsn.keys() :
        return jsn[c.desc]
    else :
        return None

async def read_main(urls) :
    fu = partial(
            fu0 ,
            trust_env = False ,
            params = None ,
            verify_ssl = True ,
            content_type = None
            )
    jsns = await fu(urls)
    out = [read_desc_in_meta_jsn(x) for x in jsns]
    return out

def get_dataset_name_from_url(url) :
    repon = url.split('/')[-1]
    return repon.split('d-' , 1)[1]

def main() :
    pass

    ##

    hdrs = {
            'User-Agent' : 'Mozilla/5.0'
            }
    resp = requests.get(cte.src , headers = hdrs)
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
    df[c.relurl] = [x['href'] for x in la]
    ##
    df['spl'] = df[c.relurl].str.split('/')
    ##
    ptr = 'd-'
    msk = df['spl'].apply(lambda x : x[-1].startswith(ptr))

    df1 = df[msk]
    del df
    ##

    df1 = df1[[c.relurl]]
    ##
    df1[c.url] = cte.github_base_url + df1[c.relurl].str[1 :]

    tl = '/main/META.json'
    df1[c.meturl] = cte.raw_github_url + df1[c.relurl].str[1 :] + tl
    ##
    df1 = df1[[c.url , c.meturl]]
    ##
    cis = ret_clusters_indices(df1)
    ##
    for se in cis :
        si = se[0]
        ei = se[1] + 1
        print(se)

        inds = df1.index[si :ei]

        urls = df1.loc[inds , c.meturl]

        out = asyncio.run(read_main(urls))

        df1.loc[inds , c.desc] = out

    ##
    df1[c.dataset] = df1[c.url].apply(get_dataset_name_from_url)
    ##
    c2k = {
            c.dataset : None ,
            c.desc    : None ,
            c.url     : None ,
            c.meturl  : None ,
            }

    df1 = df1[c2k.keys()]
    ##
    df2 = df1.copy()
    ##
    df1[c.dataset] = '[' + df1[c.dataset] + '](' + df1[c.url] + ')'
    ##
    df1[c.short] = df1[c.desc]
    df1 = df1[[c.dataset , c.short]]
    ##
    df1.reset_index(drop = True , inplace = True)
    df1.index = df1.index + 1
    ##
    rdme = '# Datasets List \n'
    rdme += df1.to_markdown()
    ##

    gdt = GithubData(gu.trg)
    gdt.overwriting_clone()
    ##

    rdmefp = gdt.local_path / 'README.md'
    with open(rdmefp , 'w') as fi :
        fi.write(rdme)
    ##
    fp = gdt.local_path / 'list.xlsx'
    snxl(df2 , fp)

    ##
    msg = 'updated README.md'
    msg += ' by: ' + gu.selff
    ##

    gdt.commit_and_push(msg)
    ##

    gdt.rmdir()

    ##

##
if __name__ == '__main__' :
    main()
    print('Done!')
