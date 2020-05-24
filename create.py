import os
import re
import urllib
import sys
from bs4 import BeautifulSoup
import time
import urllib.request

HOMEPAGE = 'https://en.wikipedia.org'


def crawl(seed, keyword):
    crawled = []
    queue = []
    crawling = set()
    try:
        f = open('uncrawled.txt')
        f.close()
    except FileNotFoundError:
        print('File uncrawled.txt does not exist, creating file.....')
        g = open("uncrawled.txt", "w+")
        g.close()
    try:
        f = open('crawled.txt')
        f.close()
    except FileNotFoundError:
        print('File crawled.txt does not exist, creating file.....')
        g = open("crawled.txt", "w+")
        g.close()
    if(os.path.exists('uncrawled.txt')):
        print('File uncrawled.txt is present!!')
    if(os.path.exists('uncrawled.txt')):
        print('File crawled.txt is present!!')
        queue = [{'url': seed, 'depth': 1}]
    while (len(crawled)<1000 and len(queue)!=0):
        temp = queue.pop(0)
        if temp['url'] not in crawled:
            crawled.append(temp)
            append_to_file('crawled.txt', temp['url'])
            if (temp['depth'] < 5): # condition to crawl only till depth : 5
                try:
                    time.sleep(1)  # using a delay of 1 sec.
                    webtext = urllib.request.urlopen(HOMEPAGE + temp['url']).read()  # get and read the webpage
                    soup = BeautifulSoup(webtext, "html.parser")
                    for name in soup.findAll('a'):  # find all the links from seed page
                        p = name.get('href')
                        if re.search('/Main_Page', p):
                            continue
                        if re.search(':', p):  # ignore url that contains ':' (avoid administrative link)
                            continue
                        if keyword == 'None':
                            if re.search('/Main_Page', p):
                                continue
                            if re.search(':', p):  # ignore url that contains ':' (avoid administrative link)
                                continue
                            if re.search('/wiki', p):  # contains 'keyword'
                                crawling.add({'url': p, 'depth': temp['depth'] + 1})
                        else:
                            if re.search('/wiki', p):
                                if re.search(keyword, p, re.IGNORECASE):
                                    crawling.add({'url': p, 'depth': temp['depth'] + 1})
                except IOError as err:
                    print("No network route to the host".format(err))
                if len(crawling) != 0:  # add crawledUrl list to stack list only if available
                    data = queue.append(crawling) # add crawled urls list to stack list
                    append_to_file('uncrawled.txt', data['url'])

# Add data onto an existing file
def append_to_file(path, data):
    with open(path, 'a') as file:
        file.write(HOMEPAGE + data + '\n')

def main():
    a = input("Enter the website you want to get crawled")
    Webpage = a.replace(HOMEPAGE, '')
    keyword = input("Enter the Keyword else enter None")
    crawl(Webpage, keyword)


if __name__ == '__main__':
    main()