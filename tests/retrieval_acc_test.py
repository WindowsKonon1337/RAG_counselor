import json
import requests


if __name__ == '__main__':
    with open('./data/test_queries.json') as file:
        test_objects = json.load(file)['test_objects']

    good_ans = 0

    for test_obj in test_objects:
        response = requests.get(
            f'http://localhost:1337/question?q_str={test_obj["query"]}&chapter_num={test_obj["chapter_num"]}'
        )

        respone_json = json.loads(
            response.text
        )

        founded_law_norms = list(
            x['law_norm'] for x in respone_json['metadatas'][0]
        )

        if test_obj['norm'] in founded_law_norms:
            good_ans += 1

    print(good_ans / len(test_objects))

