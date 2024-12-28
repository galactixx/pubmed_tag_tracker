from typing import Dict, Generator, Iterable, List
import json
import html
import unicodedata
from dataclasses import dataclass

from bs4 import BeautifulSoup, ResultSet, Tag
import requests

@dataclass(frozen=True)
class PubMedColumns:
    tag: str = 'Tag'
    name: str = 'Name'
    desc: str = 'Description'

PUBMED_COLUMNS = PubMedColumns()

# Constants and global variables
PUBMED_TAG_TABLE_COLUMN_NAMES = [
    PUBMED_COLUMNS.tag, 
    PUBMED_COLUMNS.name, 
    PUBMED_COLUMNS.desc
]
PUBMED_TAG_COLUMN_INDICES: Dict[int, str] = {
    PUBMED_TAG_TABLE_COLUMN_NAMES.index(col): col
    for col in PUBMED_TAG_TABLE_COLUMN_NAMES   
}
PUBMED_TAG_TABLE_TITLE = 'PubMed Format tags'
PUBMED_URL = 'https://pubmed.ncbi.nlm.nih.gov/help/'

def clean_html_text(raw_text: ResultSet[str]) -> str:
    stripped_text = join_text(join_text(text.split()) for text in raw_text)
    normalized_text = unicodedata.normalize('NFKC', stripped_text)
    decoded_text = html.unescape(normalized_text)
    return decoded_text  


def get_element_text(element: Tag) -> str:
    raw_text = element.find_all(string=True, recursive=True)
    cleaned_text = clean_html_text(raw_text=raw_text)
    return cleaned_text


def join_text(text: Iterable[str]) -> str:
    return ' '.join(text).strip()


def fetch_pubmed_tags() -> List[Dict[str, str]]:
    response = requests.get(PUBMED_URL)
    response_html = response.text

    soup = BeautifulSoup(response_html, 'html.parser')
    pubmed_tag_table = soup.find('table')
    pubmed_tag_table_rows: Generator[Tag, None, None] = (
        tr for tr in pubmed_tag_table.find_all('tr')
    )

    # Retrieve the first row, which corresponds to the table title
    table_title_row = next(pubmed_tag_table_rows)
    table_title = get_element_text(element=table_title_row)

    assert table_title == PUBMED_TAG_TABLE_TITLE

    # Retrieve the second row, corresponding to the table column names
    table_col_row = next(pubmed_tag_table_rows)
    table_col_names = [
        get_element_text(element=col)
        for col in table_col_row.find_all('th')
    ]

    assert table_col_names == PUBMED_TAG_TABLE_COLUMN_NAMES

    pubmed_tags: List[Dict[str, str]] = []
    for table_row in pubmed_tag_table_rows:
        pubmed_tag_data: Dict[str, str] = dict()
        table_data: enumerate[Tag] = enumerate(table_row.find_all('td'))

        for idx, data in table_data:
            data_text = str()
            pubmed_column_name = PUBMED_TAG_COLUMN_INDICES[idx]

            unordered_list = data.find('ul')
            if unordered_list is not None:
                del_unordered_list = unordered_list.extract()
                list_items = '\n'.join(
                    get_element_text(item) for item in del_unordered_list.find_all('li')
                )
                data_text = data_text + '\n' + list_items

            data_text = get_element_text(element=data) + data_text
            pubmed_tag_data.update({pubmed_column_name: data_text})
        pubmed_tags.append(pubmed_tag_data)

    return pubmed_tags


def save_pubmed_tags_to_json(pubmed_tags: List[Dict[str, str]], filename: str) -> None:
    pubmed_data = {'pubmed_tags': pubmed_tags}
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(pubmed_data, json_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    pubmed_tags = fetch_pubmed_tags()
    save_pubmed_tags_to_json(pubmed_tags, 'pubmed_tags.json')