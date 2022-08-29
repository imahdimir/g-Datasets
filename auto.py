##

"""

  """

import requests
import pandas as pd

from bs4 import BeautifulSoup
from by_repos_list_with_order import dlist_url , gitburl
from by_repos_list_with_order import do_the_rest


def main() :
  pass

  ##
  url = 'https://github.com/stars/imahdimir/lists/datasets'
  resp = requests.get(url)
  ##
  soup = BeautifulSoup(resp.text , "html.parser")
  ##
  la = soup.body.find_all('a')
  la = [x for x in la if x.has_attr('href') and not x.has_attr('class')]
  ##
  lb = [x for x in la if x.find('span') is not None]
  ##
  df = pd.DataFrame()
  df['rurl'] = [x['href'] for x in lb]

  ##
  df['url'] = gitburl + df['rurl'].str[1 :]

  ##
  do_the_rest(df)

  ##

##


if __name__ == '__main__' :
  main()

##