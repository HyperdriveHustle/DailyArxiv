import openai
import config
import json

openai.api_key = config.API_KEY

SUMMARY_PROMPT = '''
Please generate a brief paper introduction based on the provided paper title and abstract, and determine whether the paper is related to GPT/ChatGPT/LLM. 
Output the result in Chinese in a JSON format: {"summary": "论文的中文介绍", "ref": "yes/no"}. 
If the paper is related to GPT/ChatGPT/LLM, then "ref": "yes"; otherwise, "ref": "no".

The paper is as follows:

'''


def get_completion(prompt):
    '''
    获取 chatgpt 结果
    :return:
    '''
    messages = [{'role': 'user', 'content': prompt}]
    try:
        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=messages
        )
    except:
        print('>> 连接 openai 失败')
        return None
    return completion.choices[0].message


def parser_completion(message):
    '''
    解析模型生成的结果
        e.g. {"summary": "这篇论文研究如何利用领域无关的规划器和组合搜索来玩愤怒的小鸟游戏，并减少问题的复杂度。研究者使用PDDL+作为模型，提出了几个领域特定的改进措施，包括启发式和类似于首选算子的搜索技术。结果表明，在大多数级别上，我们的性能类似于这些领域特定的方法，即使不使用我们的领域特定搜索增强措施。", "ref": "no"}
    :return:
    '''
    try:
        message = json.loads(message)
        summary, ref = message['summary'], message['ref']
    except:
        summary = message
        ref = None
    return summary, ref


class Paper(object):
    def __init__(self,
                 title,
                 author=None,
                 abstract=None,
                 category=None):
        self.title = title
        self.author = author
        self.abstract = abstract
        self.category = category
        self.summary = None
        self.ref = None

    def get_summary(self):
        if self.abstract is not None:
            prompt = f"{SUMMARY_PROMPT}\n<title:\n{self.title}>\nabstract:\n{self.abstract}"
            result = get_completion(prompt)
            if result is not None:
                self.summary, ref = parser_completion(result['content'])
                self.ref = True if ref == 'yes' else False



