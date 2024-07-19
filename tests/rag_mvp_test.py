import json
import requests


if __name__ == '__main__':
    with open('./data/test_queries.json') as file:
        test_objects = json.load(file)['test_objects']

    with open('./data/pred_resps', mode='w+') as output_file:
        for test_obj in test_objects:
            response = requests.get(
                f'http://localhost:1337/question?q_str={test_obj["query"]}'
            )

            response_parts = response.text.strip().split("\\n")

            for response_part in response_parts:
                output_file.write(
                    response_part + '\n'
                )

            output_file.write(
                test_obj['query'] + '\n' + \
                test_obj['norm'] + '\n' + \
                test_obj['answer'] + '\n'
            )

            output_file.write('=' * 30 + '\n')
