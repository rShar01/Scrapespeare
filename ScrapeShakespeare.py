from bs4 import BeautifulSoup
from requests import get
from warnings import warn
from heapq import nlargest
import matplotlib.pyplot as plt


"""
To be honest, I don't have any meaningful analysis of this information. If you do, go right ahead and use this code

I just did this as practice
"""
print("Welcome to the Shakespeare word counter!")
print("Enter a word you want to see the frequency of")
print("Alternatively enter 'ALL_WORDS' to get a bar graph of the 75 most used words")
search_word = input()


headers = {"Accept-Language": "en-US, en;q=0.5"}
url = "http://shakespeare.mit.edu/"
response = get(url, headers=headers)
if response.status_code != 200:
    warn("Did not connect properly")

main_page_parser = BeautifulSoup(response.text, 'html.parser')
all_works_html = main_page_parser.findAll('a')
all_works_html.pop(0)
all_works_html.pop(0)
all_works_html.pop(-1)
all_works_html.pop(-1)

all_works_links = []

for a in all_works_html:
    all_works_links.append(a['href'])

"""
sample code of one instance I based my loop around



first_link = all_works_links[0]
response = get("http://shakespeare.mit.edu/" + first_link[0:-10] + "full.html")
html_parser = BeautifulSoup(response.text, 'html.parser')
all_sentences = html_parser.findAll('blockquote')

for sentence in all_sentences:
    list_of_words = sentence.text.split()
    for word in list_of_words:
        if word in dict_of_words.keys():
            dict_of_words[word] = dict_of_words[word] + 1
        else:
            dict_of_words[word] = 1
"""

if search_word == 'ALL_WORDS':
    dict_of_words = {}
    for url in all_works_links:
        print("working on " + url[0:-11])
        response = get("http://shakespeare.mit.edu/" + url[0:-10] + "full.html", headers=headers)
        html_parser = BeautifulSoup(response.text, 'html.parser')
        all_sentences = html_parser.findAll('blockquote')
        for sentence in all_sentences:
            list_of_words = sentence.text.split()
            for word in list_of_words:
                if word in dict_of_words.keys():
                    dict_of_words[word] = dict_of_words[word] + 1
                else:
                    dict_of_words[word] = 1
    most_common = nlargest(75, dict_of_words, key=dict_of_words.get)
    dict_of_most_common = {}

    for word in most_common:
        dict_of_most_common[word] = dict_of_words.get(word)

    plt.bar(list(dict_of_most_common.keys()), dict_of_most_common.values(), color='g')
    plt.xticks(rotation=45, horizontalalignment='right', fontweight='light')
    plt.show()

else:
    dict_of_count = {}
    for url in all_works_links:
        current_work = url[0:-11]
        print("working on " + current_work)
        dict_of_count[current_work] = 0
        response = get("http://shakespeare.mit.edu/" + url[0:-10] + "full.html", headers=headers)
        html_parser = BeautifulSoup(response.text, 'html.parser')
        all_sentences = html_parser.findAll('blockquote')
        for sentence in all_sentences:
            list_of_words = sentence.text.split()
            for word in list_of_words:
                if word == search_word:
                    dict_of_count[current_work] = dict_of_count[current_work] + 1

    plt.bar(list(dict_of_count.keys()), dict_of_count.values(), color='g')
    plt.xticks(rotation=45, horizontalalignment='right', fontweight='light')
    plt.show()
