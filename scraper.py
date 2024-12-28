from typing import Dict, Generator, List
import json
import html
import unicodedata

from bs4 import BeautifulSoup, Tag
import requests

# Constants and global variables
PUBMED_TAG_TABLE_COLUMN_NAMES = ['Tag', 'Name', 'Description']
PUBMED_TAG_COLUMN_INDICES: Dict[int, str] = {
    PUBMED_TAG_TABLE_COLUMN_NAMES.index(col): col
    for col in PUBMED_TAG_TABLE_COLUMN_NAMES   
}
PUBMED_TAG_TABLE_TITLE = 'PubMed Format tags'
PUBMED_URL = 'https://pubmed.ncbi.nlm.nih.gov/help/'

def get_text(element: Tag) -> str:
    raw_text = element.get_text().strip()
    normalized_text = unicodedata.normalize('NFKC', raw_text)
    decoded_text = html.unescape(normalized_text)
    return decoded_text


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
    table_title = get_text(element=table_title_row)

    assert table_title == PUBMED_TAG_TABLE_TITLE

    # Retrieve the second row, corresponding to the table column names
    table_col_row = next(pubmed_tag_table_rows)
    table_col_names = [
        get_text(element=col) for col in table_col_row.find_all('th')
    ]

    assert table_col_names == PUBMED_TAG_TABLE_COLUMN_NAMES

    pubmed_tags: List[Dict[str, str]] = []
    for table_row in pubmed_tag_table_rows:
        pubmed_tag_data: Dict[str, str] = {
            PUBMED_TAG_COLUMN_INDICES[idx]: get_text(element=data)
            for idx, data in enumerate(table_row.find_all('td'))
        }
        pubmed_tags.append(pubmed_tag_data)

    return pubmed_tags


def save_pubmed_tags_to_json(pubmed_tags: List[Dict[str, str]], filename: str) -> None:
    pubmed_data = {'pubmed_tags': pubmed_tags}
    with open(filename, 'w', encoding='utf-8') as json_file:
        json.dump(pubmed_data, json_file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    pubmed_tags = fetch_pubmed_tags()
    save_pubmed_tags_to_json(pubmed_tags, 'pubmed_tags.json')