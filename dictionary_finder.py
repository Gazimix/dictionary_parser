import sys
import os
import docx
import re

FIRST_ARG = 1

SEARCH_REGEX = r'\b{param}\b'
PATH_TO_DICTIONARIES = "D:\\Projects\\Python\\dictionary_finder\\"
DICTIONARIES_TO_SEARCH = ['Irrigation.docx',
                          'Test.docx', 'English Dictionary 2.docx']
# DICTIONARIES_TO_SEARCH = ['English Dictionary 2.docx']


def look_for_regex_in_file(inpt, documents):
    res = []
    for doc in documents:
        res.extend(find_in_document(doc, inpt))
    return res


def print_rows(rows):
    for row in rows:
        str = ""
        for i, cell in enumerate(row.cells):
            if i == len(row.cells) - 1:
                str += f"{cell.text}"
            else:
                str += f"{cell.text} | "
        print(str)


def find_in_document(document, str_to_find):
    pattern = SEARCH_REGEX.format(param=str_to_find)
    prog = re.compile(pattern)
    results = []
    tables = document.tables
    for table in tables:
        rs = table.rows
        for i, row in enumerate(rs):
            for cell in row.cells:
                text_in_lowercase = cell.text.lower()
                result = prog.search(text_in_lowercase)
                print(row)
                if result:
                    results.append(row)
    return results


def get_input(msg=""):
    return input(msg).lower().strip()


if __name__ == "__main__":
    docs = []
    for dict_name in DICTIONARIES_TO_SEARCH:
        docs.append(docx.Document(PATH_TO_DICTIONARIES + dict_name))
    inpt = get_input(
        "Enter the phrase you wish to search for in the dictionary. Enter 'q' to exit.\n")
    while (inpt != 'q'):
        if len(inpt):
            rows = look_for_regex_in_file(inpt, docs)
            if len(rows) != 0:
                print_rows(rows)
            else:
                print(f"Couldn't find the word: {inpt}")
        inpt = get_input()
