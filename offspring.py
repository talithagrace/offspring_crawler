import requests, bs4, re
import time
from time import sleep

def geturls():
    base_url = 'https://offspring.co.uk'
    r = requests.get(base_url)
    r.raise_for_status()
    f = open('url_list.txt', 'w+')
    link_list = []

    search_results = bs4.BeautifulSoup(r.content, 'html.parser')

    for link in search_results.find_all('a', href=re.compile("^/[a-z]")):
        path = (base_url + link.get('href') + "\n")
        seen_1 = set(link_list)
        if path not in seen_1:
            link_list.append(path)
            seen_1.add(path)
            f.write(path)

    for url_next in link_list:
        r_next = requests.get(url_next)
        #r_next.raise_for_status()
        if int(r_next.status_code) < 400 and url_next != "https://offspring.co.uk/view/secured/content/login":
            search_results_next = bs4.BeautifulSoup(r_next.content, 'html.parser')
            for link in search_results_next.find_all('a', href=re.compile("^/[a-z]")):
                path_next = (base_url + link.get('href') + "\n")
                seen = set(link_list)
                if path_next not in seen:
                    link_list.append(path_next)
                    seen.add(path_next)
                    f.write(path_next)
        sleep(0.5)
    f.close

start = time.time()
geturls()
end = time.time()
print(end-start)
