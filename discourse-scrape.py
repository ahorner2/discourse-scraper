import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import datetime
from _utils import print_full, scrolling

'''
Data for all posts links scraped in MAP.

Output: Links, titles, main tags, sub tags, replies, views, and dates
'''

MAP = {
    'mips': 'https://forum.makerdao.com/tag/mips',
    'public_calls': 'https://forum.makerdao.com/tag/public-call',
    'signals': 'https://forum.makerdao.com/tag/signaling',
    'endgame': 'https://forum.makerdao.com/tag/endgame',
    'informal_polls': 'https://forum.makerdao.com/tag/informal-poll'
}

for doc in MAP.keys():
    url = MAP[doc]

    res = requests.get(url).text
    soup = BeautifulSoup(res, 'html.parser')

    links = []
    titles = []
    replies = []
    views = []

    # top line post links
    top_line = [a['href'] for a in soup.findAll(
        'a', class_='title') if a.stripped_strings]  # first page post links
    for line in top_line:
        links.append(line)

    # post titles raw text
    for title in soup.findAll('span', class_='link-top-line'):
        raw_title = title.text.split('\n')
        ttl = ''.join(raw_title)
        cl_title = ttl.splitlines()
        titles.append(cl_title)

    # replies per post
    for reply in soup.findAll('span', class_='posts'):
        rep = reply.text.split(',')
        reps = ''.join(rep)
        replies.append(reps)

    for view in soup.findAll('span', class_='views'):
        views.append(view.text)

    ## ---- merge and frame ---- ##

    merged_data = list(zip(titles, links, replies, views))

    df = pd.DataFrame.from_dict(merged_data)

    df2 = pd.DataFrame({
        'titles': titles,
        'links': links,
        'replies': replies,
        'views': views
    })

    df2['titles'] = df2['titles'].astype(str).str.strip('[]')
    df2 = df2.replace("'", "", regex=True)

    # cast to proper dtypes
    df2['replies'] = df2['replies'].astype(int)
    df2['views'] = df2['views'].astype(int)

    current_date = f'gov_{datetime.datetime.now().strftime("%m.%d.%Y")}.csv'
    # df2.to_csv(current_date, mode='a', encoding='utf-8')

    print_full(df2)
