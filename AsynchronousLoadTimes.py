import aiohttp, asyncio, time, requests, pandas as pd
from tqdm import tqdm
from tqdm.asyncio import tqdm_asyncio
from bs4 import BeautifulSoup

# run the load checks asynchronously on CPU:
async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.text()

async def check_loading_time(url):
    async with aiohttp.ClientSession() as session:
        dummy_list = []
        web_url = [url]
        for i in web_url*5:
            start_time = time.time()
            await fetch_url(session,i)
            end_time = time.time()
            loading_time = end_time - start_time
            loading_time = round(loading_time,2)
            dummy_list.append(loading_time)
        return round(sum(dummy_list)/len(dummy_list),2)

async def main(url_list):
    urls = url_list
    results = []
    tasks = [check_loading_time(url) for url in urls]
    results = await tqdm_asyncio.gather(*tasks, ncols=100, desc = 'Checking load times...')
    return results
 
def get_all_links(full_url):
        response = requests.get(full_url)
        response_soup = BeautifulSoup(response.text, 'html.parser')
        url_dummy = []
        for link in response_soup.find_all('a'):
            url_dummy.append(link.get('href'))
        # clean the list to remove any None values
        clean_stage1 = [i for i in url_dummy if i is not None]
        # clean the list to remove any values that are not links
        clean_stage2 = [j for j in clean_stage1 if https://www in j]
        return clean_stage2

# MAIN
if __name__ == "__main__":
    test_output = get_all_links('https://www.wikipedia.org')
    results = await main(test_output)
    # package the results up into a dictionary {link:average load time}
    consolidated_dict = {}
    for key in test_output:
        for value in results:
            consolidated_dict[key] = value
            results.remove(value)
            break

    # convert the dictionary to a DataFrame:
    consolidated = pd.DataFrame(data = consolidated_dict, index = [0])
    consolidated = (consolidated.T)
    consolidated.to_excel('link_output.xlsx')
