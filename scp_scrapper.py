from bs4 import BeautifulSoup  # type: ignore
import pandas as pd  # type: ignore
from SCP import SCP
import requests  # type: ignore
import math

from threading import Thread, Lock

webpage = 'https://scp-wiki.wikidot.com'

LIMIT_THREADS = 100

df = pd.DataFrame()

def state_manager(state: int, next: bool) -> bool:
    '''
    @param state: int
    @param state
    
    @return to continue or to stop'''
    pass


def add_to_df(new_df: pd.DataFrame) -> None:
    global df
    df = df.append(new_df, ignore_index=True)


def multiple_scp_scrape(ids: list) -> pd.DataFrame:
    '''
    @param ids list
    @param ids is the number of the scp

    @return pd.DataFrame
    '''
    global df
    df = pd.DataFrame()

    if len(ids) > LIMIT_THREADS:
        for x in range(math.ceil(len(ids) // LIMIT_THREADS)):
            if ((x+1)*LIMIT_THREADS > len(ids)):
                tmp = ids[(x*LIMIT_THREADS):len(ids)]
            else:
                tmp = ids[(x*LIMIT_THREADS):(LIMIT_THREADS*(x+1))]

            threads = [None] * len(tmp)  # [1,2,3] [None,None,None]
            lock = Lock()

            for i in range(len(tmp)):
                threads[i] = Thread(target=scrape_scp, args=(  # type: ignore
                    ids[i], lock))  # type: ignore
                threads[i].start()  # type: ignore

            for i in range(len(tmp)):
                threads[i].join()  # type: ignore

        return df


    else:
        threads = [None] * len(ids)  # [1,2,3] [None,None,None]
        lock = Lock()

        for i in range(len(ids)):
            threads[i] = Thread(target=scrape_scp, args=(  # type: ignore
                ids[i], lock))  # type: ignore
            threads[i].start()  # type: ignore

        for i in range(len(ids)):
            threads[i].join()  # type: ignore

        return df


def scrape_scp(id: str, lock=None) -> pd.DataFrame:
    # empty dataframe
    df = pd.DataFrame()

    # Go to content
    page = requests.get(f'{webpage}/scp-{id}')

    if page.status_code != 200:
        print(f'error with scp {id}')
        return df

    # Parse
    soup = BeautifulSoup(page.content, 'html.parser')
    body = soup.find('body')
    main = body.find("div", id="main-content")

    # Empty data
    title = ""
    item = -1
    object_class = ""
    containment_procedure = ""
    desc = ""
    image = None

    # GET CONTET OF THE PAGE

    # get title
    title = main.find('div', id="page-title").contents[0]
    title = title.strip().split('-')[1]
    title = int(title)

    # info scp
    scp_info = main.find('div', id="page-content")

    last_category = ""

    images = scp_info.find('img')
    if images:
        image = images['src']

    for p in scp_info.find_all('p'):
        # If there is just text, then it continues from the previous category
        if len(p) == 1:
            # Check if only is title
            tmp = p.find('strong')
            if tmp:
                result = tmp.contents[0]
            else:
                result = p.contents[0]

            if last_category == 'Description:':
                desc += f'\n{result}'
            elif last_category == "Special Containment Procedures:":
                containment_procedure += f'\n{result}'

        element = p.find('strong')

        if not element:
            continue

        tmp = element.contents[0].find('strong') 
        if tmp:
            name = tmp.contents[0]
        else:
            name = element.contents[0].strip()

        if name == 'Item #:':
            item = p.contents[1].strip()
        elif name == 'Object Class:':
            object_class = p.contents[1].strip()
        elif name == 'Description:':
            desc += '\n'.join(p.contents[1:])
            last_category = 'Description:'
        elif name == "Special Containment Procedures:":
            containment_procedure += '\n'.join(p.contents[1:])
            last_category = 'Special Containment Procedures:'

    scp = SCP(title, item, object_class,
              containment_procedure, desc, image)

    df = df.append(scp.get_obj(), ignore_index=True)

    # Lock the dataframe when writing on it
    # to stop others to write at the same time.
    if lock:
        lock.acquire()
        add_to_df(df)
        lock.release()
    else:
        return df