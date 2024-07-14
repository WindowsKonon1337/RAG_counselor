import click
import asyncio
import os
import json
from asyncio import Queue
import re

import aiohttp
from bs4 import BeautifulSoup as bs


class Fetcher:
    def __init__(
            self,
            url_file: str,
            output_file: str,
            workers: int = 10
    ) -> str:
        if isinstance(url_file, str):
            self.url_file = open(url_file, encoding='utf-8')
        else:
            raise TypeError('bad urlfile type')
        if isinstance(output_file, str):
            self.output_file = open(output_file, encoding='cp1251', mode='w+')
        else:
            raise TypeError('bad output file type')

        self.workers = workers
        self.queue = Queue()

    def __get_urls_from_file(self):
        for line in self.url_file:
            yield line.strip()

    def __filter_condition(self, text_str: str) -> bool:
        if 'Утратил силу' not in text_str \
                and 'в ред. Федерал' not in text_str \
                and 'текст в предыдущей редакции' not in text_str \
                and text_str:
            return True
        return False

    async def fetch_url(self, url: str):
        async with aiohttp.ClientSession() as session:
            async with session.get('https://www.consultant.ru' + url) as response:
                data = await response.read()
                return await self.parse_response(data)

    async def parse_response(self, data):
        soup = bs(data, 'html.parser')
        law_div = soup.find('div', class_='document-page__content document-page_left-padding')

        extracted_divs = law_div.find_all('div', class_='document__edit doc-edit')
        for div in extracted_divs:
            div.extract()

        law_desc = list(
            filter(
                    lambda x: x.get('class', []) != ['no-indent'],
                    law_div.find_all('p')
            )
        )
        law_desc_list = list(filter(self.__filter_condition, [x.text for x in law_desc]))
        splitted_label = law_desc_list[0].split('.')
        tail_nums = [i for i in splitted_label[1:] if i.isdigit()]

        law_num, law_desc_str = splitted_label[0] + '.' + '.'.join(tail_nums), ' '.join(law_desc_list[1:]).strip()
        law_parts = list(
                            filter(
                                lambda x: x,
                                re.split(r'\d+\. ', law_desc_str)
                            )
                        )
        return law_num, law_parts

    async def fetch_worker(self):
        while True:
            url = await self.queue.get()
            if url is None:
                await self.queue.put(url)
                break
            try:
                law_num, law_parts = await self.fetch_url(url)
                json.dump(
                    {
                        law_num: law_parts
                    },
                    fp=self.output_file,
                    ensure_ascii=False
                )
                self.output_file.write('\n')
            except Exception as exception:
                print(f'Error fetching {url} : {exception}')

    async def batch_fetch(self):
        workers = [
            self.fetch_worker()
            for _ in range(self.workers)
        ]

        for url in self.__get_urls_from_file():
            await self.queue.put(url)
        await self.queue.put(None)

        await asyncio.gather(*workers)


@click.command('extract_law_data')
@click.option('--raw_law_links', type=click.Path())
@click.option('--output_file', type=click.Path())
def main(raw_law_links, output_file):
    FOLDER_PATH = '/'.join(
        output_file.split('/')[:-1]
    )

    if not os.path.exists(FOLDER_PATH):
        os.makedirs(FOLDER_PATH)

    fetcher = Fetcher(
        url_file=raw_law_links,
        output_file=output_file,
        workers=8,
    )

    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetcher.batch_fetch())
    loop.close()



if __name__ == '__main__':
    main()
