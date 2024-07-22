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

    TOKEN = 'eyJjdHkiOiJqd3QiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwiYWxnIjoiUlNBLU9BRVAtMjU2In0.uDQGhKrbLRjKwYMgSLUzcsOgnMiNraYzX7ou-UpFQGQ1zXsU-5_PtVjcvo2TuWGueEi52ESuf_W8_PkPxwyCPJt6LSZ00bvLOFMauXQLUa17-kSwvuIxMAygNJuAelnkPANKd1Z3aTEs0b-FtqBtoNAwLCj8Z2hJDFtnmQIvulYYfXFPnz_xmN0Z5h5tCa6CEZGsNjsIWrfLlTvME5VeOB2UaAZsAPnahyM1IE1Z2HUbqXA02iLR0Yg6eYieZ1O48Tlz_kOz8w9Cc6hTgP6BPwPyRZXe00wE-DZZOrpE_a5cD0ELqEQ-nzMreO6pcwSfkgAaG0-O5ufX2Ef-Tmg9Jg.gXT4-Ln9q79EPbmRpDv_Sw.thuWh32mgH5VLC8iEPeNQEWCE7CSnZ6ZntcZsChY_uFp3fGQtUCaqKWTeeRczhgI5C17BtEbxwdoZyWw_GBOCwYt6DjEkRGplzNbSbCKuj2bivpiHNjBvsmAXorkW_WaDTDuSbOSxFpoCLshOwrx6pqJ6spocBcgW2OFWpbStjisRtMNeddE92J-eIIloGZlM-chBqarjrILUnJYxaJMDUTjGAfQo_a23HRw6Cogqu9QwBtnjY9-mqP86YVko-bXSW5IDd8pMLWZfyDDifvXPrJaUwoeJE95pepnn5NG5bE86RdckPHKXREFuRHh6a1Bae1_Nyz1KWyip9drNkxguxs0s9diw_hxuSAVXFZLweRziy2Cd9r6_HYtCEDTr5a6AZ8y6PwwH9JPiryI9Nqrs_2teFMzQ3ZNyF_cn3S5SpSDaqaVw5eGV3NWQOnik3rh9Yiff5UrXJ9WWfFHzX43O7AJkZnhRzlz4wUAZG3yRxhTA52URFzfRCxWp8-NsqA9LIDRpNrB6baeifRq0M7E8fu5e8WyOQw9jXZHSYhO4LjmY-lRsse5AecWG-aPSBpKaBbAcu6bWHiKhcdzO5bgEwbn0jwpgVSHclQietIxPWOcmFVxBPfCz2wyXpDJBsO9-eKjhdFU2H8KpRN-9p_xiQNAsMssnI3ByMN7FOR38ciM61Qa3X0OBKcmFQKudH3eBLdQH6s1F3qXB9fLywn3KGBEARkZ2g05oDkveXbDSmg.7ErwWb5QOKfjSD-SWT8bB2ha6BzTSqEAZjjXPMY96Zk'
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
        
        # print(response.text, anchor_ans)


    print(good_ans / len(test_objects))
