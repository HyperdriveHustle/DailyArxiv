'''
读取已经爬的论文数据，根据结果筛选出与 ChatGPT / GPT / LLM 相关的论文形成报告
'''
import pickle
import os
from datetime import datetime
from paper_tools import Paper


today = datetime.today().strftime('%Y-%m-%d')


def get_paper(filename):
    with open(filename, 'rb') as f:
        result = pickle.load(f)
    cnt = 0
    for title in result:
        paper = result[title]
        if paper.ref:
            print(cnt)
            print(paper.title)
            print(paper.summary)
            print("----" * 10)
            cnt += 1


if __name__ == '__main__':
    filename = f'data/daily_paper/paper_{today}.pkl'
    get_paper(filename)