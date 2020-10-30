import sys
import os
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore, Style

init()


def navigator(url, download_mode, args1):
    if '.' in url:
        if 'https://' not in url[:8]:
            url = 'https://' + url
        # if 'www.' not in url[8:13]:
        #     url = 'www.' + url
        try:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser')
            n = soup.find_all('p')
            site_main = soup.children
            tags = ('p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ol')
            html = None
            body = None
            for element in site_main:
                if element.name == 'html':
                    html = element
                    break
            # get site body
            for element in list(html.children):
                if element.name == 'body':
                    body = element
                    break
            # resolve all <p> tags and print the text
            all_text = []
            # for element in list(body.children):
            #     print(element.name)
            for tag in body.find_all(tags):
                text_to_append = tag.get_text().strip().replace('\n', ' ')
                if tag.name == 'a':
                    all_text.append(Fore.BLUE + text_to_append)
                    all_text.append(Style.RESET_ALL)
                else:
                    all_text.append(text_to_append)
                # print(tag.name + ':           ' + tag.get_text())
            document = ''
            for line in all_text:
                document += line + '\n'
            print(document)
            if download_mode:
                f1 = open(args1[1] + '/' + url[8:] + '.txt', 'w')
                f1.write(document)
                f1.close()
        except:
            print('Error Incorrect URL')
    # elif url == 'bloomberg':
    #     try:
    #         f1 = open(args1[1] + '/bloomberg.txt')
    #         print(f1.read())
    #         f1.close()
    #     except:
    #         print('Error: Incorrect URL')
    # elif url == 'nytimes':
    #     try:
    #         f1 = open(args1[1] + '/nytimes.txt')
    #         print(f1.read())
    #         f1.close()
    #     except FileNotFoundError or IndexError:
    #         print('Error: Incorrect URL')
    else:
        print('Error Incorrect URL')


args = sys.argv
save = False
history = deque()
if len(args) == 2:
    save = True
    try:
        os.mkdir(args[1])
    except FileExistsError:
        pass
user_input = input()
while user_input != 'exit':
    if user_input == 'back':
        try:
            history.pop()
            user_input = history.pop()
            navigator(user_input, save, args)
            user_input = input()
        except IndexError:
            user_input = input()
    else:
        history.append(user_input)
        navigator(user_input, save, args)
        user_input = input()
