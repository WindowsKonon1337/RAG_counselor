import json
import requests
from uuid import uuid4
import sys

sys.path.insert(1, '../')
sys.path.insert(3, '../src/prompt_templates')

from src.prompt_templates.get_classify_chapter_prompt import configure_classify_chapter_prompt

if __name__ == '__main__':

    # with open('./data/test_queries.json') as file:
    #     test_objects = json.load(file)['test_objects']
    # good_ans = 0
    # with open('output1') as file:
    #     for line in file:
    #         str_pred, true_label = tuple(line.strip().split())
    #         pred_obj = json.loads(str_pred)['choices'][0]['message']
    #         if true_label == pred_obj['content']:
    #             good_ans += 1
    #         else:
    #             print(true_label, pred_obj['content'])

    # print(good_ans / len(test_objects))

    TOKEN = '<INSERT HERE>'
    with open('./data/test_queries.json') as file:
        test_objects = json.load(file)['test_objects']
    
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {TOKEN}'
    }

    good_ans = 0

    for test_obj in test_objects:
        anchor_ans = str(test_obj['chapter_num'])

        payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
            "role": "system",
            "content": configure_classify_chapter_prompt(test_obj['query'])
            }
        ],
        "stream": False,
        "repetition_penalty": 1
        })

        response = requests.request("POST", url, headers=headers, data=payload, verify=False)

        pred = json.loads(response.text)['choices'][0]['message']
        if pred['content'] == anchor_ans:
            good_ans += 1
        
        print(response.text, anchor_ans)


    print(good_ans / len(test_objects))
