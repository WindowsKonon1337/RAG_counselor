import os


from bs4 import BeautifulSoup as bs
import requests
import click


CONSULTANT_PLUS_LINK = 'https://www.consultant.ru'
KOAPRF_DOC_LINK = 'document/cons_doc_LAW_34661'

def actual_law_condition(text: str):
    return not ('Утратил' in text or 'Глава' in text)


@click.command('get_act_links')
@click.option('--output_file', type=click.Path())
def get_act_links(output_file):
    try:
        r = requests.get(f'{CONSULTANT_PLUS_LINK}/{KOAPRF_DOC_LINK}')
    except Exception as e:
        print(f'Error: {CONSULTANT_PLUS_LINK}/{KOAPRF_DOC_LINK} : {e}')
        exit(1)

    parser = bs(r.text, 'html.parser')
    links_div = parser.find('div', class_='document-page__toc')
    law_links = links_div.find_all('a')

    idxs = []

    for idx, link in enumerate(law_links):
        if 'Раздел II' in link.text or 'Раздел III' in link.text:
            idxs.append(idx)

    actual_law_links = list(
        map(
            lambda x: x.get('href'),
            filter(
                lambda x: actual_law_condition(x.text),
                law_links[idxs[0] + 2: idxs[1] - 1]
            )
        )
    )

    FOLDER_PATH = '/'.join(
        output_file.split('/')[:-1]
    )

    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)
    with open(output_file, 'w+') as f:
        for link in actual_law_links:
            f.write(link + '\n')


if __name__ == '__main__':
    get_act_links()
