import os
import re
import urllib
import sys
import time
import urllib.request
from bs4 import BeautifulSoup

base_url = "http://en.wikipedia.org"

def crawl(seed, keyword):
    crawled = []
    queue = [{'url': seed, 'depth': 1}]
    while (len(queue)!=0 and len(crawled)<1000):
        node = queue.pop(0)                             # select first dict of stack list
        if node['url'] not in crawled:  # to check if url is not already visited
            crawled.append(node)
            # mark node as visited by appending it to visited list
            with open('bfs_' + str(keyword) + '_' + '.txt', 'a') as myfile:  # append node in file
                myfile.write(base_url + node['url'] + '\n')
            if (node['depth'] < 5):                     # condition to crawl only till depth : 5
                urls = findurl(node, keyword)           # find all url in given node (from top to bottom of the page)
                if len(urls)!=0:                        #add crawledUrl list to stack list only if available
                    queue = queue + urls                # add crawled urls list to stack list
    print('----------The number of pages crawled are {}----------'.format(len(crawled)))

'''
 findurl(node, keyword) Function
 description : Function to crawl the node with given keyword (focus crawling)
 Input:
    node: The Url with depth in dict format
    keyword:The keyword to filter the crawled urls
 Output: Example is[{'url':'/wiki/Sustainable1', depth: '2' }, {'url':'/wiki/Sustainable2', depth: '2' }, etc]
 Example:
 Input:
    node: {'url':'/wiki/Sustainable_energy', depth: '1' }
    keyword:(optional) 'solar
 Output: [{'url':'/wiki/Sustainable1', depth: '2' }, {'url':'/wiki/Sustainable2', depth: '2' }, etc]
'''


def findurl(node, keyword):
    try:
        time.sleep(1)   # using a delay of 1 sec.
        htmltext = urllib.request.urlopen(base_url + node['url']).read()   # get and read the file from webpage
        soup = BeautifulSoup(htmltext, "html.parser")
        output = []
        for link in soup.findAll('a', href=True):   # find all the links from seed page
            if re.search('#', link['href']):        # ignore url that contains '#' (properly treat URLs with #)
                continue
            if re.search(':', link['href']):        # ignore url that contains ':' (avoid administrative link)
                continue
            if link['href'].startswith('/Main_Page') :
                continue
            if keyword is not None:
                if link['href'].startswith('/wiki') and re.search(keyword, link['href'],re.IGNORECASE):  # contains 'keyword'
                    output.append({'url': link['href'], 'depth': node['depth'] + 1})    #append urls to output list
            if keyword is None:
                if link['href'].startswith('/Main_Page'):
                    continue
                if link['href'].startswith('/wiki'):  # contains 'keyword'
                    output.append({'url': link['href'], 'depth': node['depth'] + 1})    #append urls to output list
        return output
    except IOError as err:
        print("No network route to the host".format(err))


# To put the data into the file
def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)


def main():
    '''
     Input: python filename <seed> <bfs/dfs> <keyword>
     Then: sys.argv = [filename, <seed>, <bfs/dfs>, <keyword>]
     Answers:
         1. python crawler.py /wiki/Sustainable_energy bfs
         2a. python crawler.py /wiki/Sustainable_energy bfs solar
         2b. python crawler.py /wiki/Sustainable_energy dfs solar
         3. python crawler.py /wiki/Solar_power bfs
    '''
    if len(sys.argv) > 3:
        keyword = sys.argv[3]
    elif len(sys.argv) < 3:
        sys.exit('Format to run: python {0} <seed> <bfs/dfs> <key>(optional)'.format(sys.argv[0]))
    else:
        keyword = None
    seed = sys.argv[1]
    if sys.argv[2] == 'crawl':
        crawl(seed, keyword)


if __name__ == '__main__':
    main()