'''
1. 获取每日日期，保存当日爬的论文为 paper-{date}.pkl
    1.1 爬取内容：title、author、abstract、category
    1.2 根据 title 和 abstract 让 chatgpt 生成一个简短的中文介绍，并判断该论文是否跟 gpt/llm 相关。
    1.3 按天保存结果
2. 维护一个列表，每日新增的论文加入列表中；每天爬的时候注意是否与之前有重复，重复了则不爬

数据保存在 data 目录下
- data
-- daily_paper 
'''
import os
import random
import time
import json
import requests
import pickle
import logging
from datetime import datetime
from bs4 import BeautifulSoup
from paper_tools import Paper


today = datetime.today().strftime('%Y-%m-%d')
ARXIV_CS_NEW_URL = 'https://arxiv.org/list/cs.AI/new'


logging.basicConfig(level=logging.INFO, filename=f'log/{today}.log', format='%(asctime)s - %(message)s')
loger = logging.getLogger(__name__)


def get_arxiv_papers(current_paper_list):
    '''
    获取 CS 类别的新论文（title、author、abstract，并使用 chatgpt 生成总结）
    :return:
    '''
    response = requests.get(ARXIV_CS_NEW_URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    papers = soup.find_all('div', class_='meta')

    index = 0
    cnt = len(papers)
    result = {}
    for paper in papers:
        index += 1
        title = paper.find('div', class_='list-title mathjax').text.strip().replace('Title:', '').strip()
        author = paper.find('div', class_='list-authors').text.strip().replace('Authors:', '')
        category = paper.find('div', class_='list-subjects').text.strip().replace('Subjects:', '')
        abstract = paper.find('p', class_='mathjax').text.strip()

        # 判断当前论文是否已经保存过
        if current_paper_list is not None and title in current_paper_list:
            print(f"-- <{title}> has already in the list.")
            continue

        print(f">> index = {index} / {cnt}")
        print(f">> title = {title}")

        loger.info(f"------------ {index} / {cnt} ------------")
        loger.info(f">> title = {title}")
        loger.info(f">> author = {author}")
        loger.info(f">> abstract = {abstract}")
        loger.info(f">> category = {category}")

        paper = Paper(title=title, author=author, abstract=abstract, category=category)
        paper.get_summary()
        loger.info(f">> summary = {paper.summary}")
        loger.info(f">> ref = {paper.ref}")
        result[title] = paper

        # sleep，防止被限流
        sleep_sec = random.choice([5, 7, 10])
        time.sleep(sleep_sec)
        print(f"--------------------- sleep_sec = {sleep_sec} ---------------------")
        print()

    return result


def run_daily():
    '''
    先获取已有的论文列表
    :return:
    '''
    paper_list_filename = 'data/paper_list.json'
    save_path =os.path.join('data/daily_paper', f'paper_{today}.pkl')

    current_paper_list = {}
    # 如果之前已经爬了一些论文，获取列表
    if os.path.exists(paper_list_filename):
        with open(paper_list_filename, 'r') as f:
            current_paper_list = json.load(f)

    result = get_arxiv_papers(current_paper_list)
    with open(save_path, 'wb') as f:
        pickle.dump(result, f)

    # 保存这次爬的论文 title
    for title in result:
        current_paper_list[title] = today
    with open(paper_list_filename, 'w') as f:
        json.dump(current_paper_list, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    run_daily()
