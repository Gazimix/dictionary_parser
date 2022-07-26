from site import abs_paths
import zipfile
import re
import sys
import argparse
import os
from path_tools import *


UNDERLINE = "_______________________________________________________________"
LOGO_MSG = "****************************************************************************\n\
                   Welcome to Dictionary Finder 2.0                         \n\
****************************************************************************"
WELCOME_MSG = "Enter the phrase you wish to search for in the dictionary. Enter 'q' to exit.\n"
DB_FOLDER_NAME = "db"
DB_FILE_NAME = "db.txt"
dictionaries_set = set()


def preprocess_documents(documents):
    word_list = []
    par_pattern = r"<w:p.+?>[\s\w\d<>:=\"\/\\\-.\(\)\[\]\!\|\@\#\$\%\^\&\*\-\+]+?<\/w:p>"
    par_trm = re.compile(par_pattern)
    word_pattern = r'<w:t\b.*?>([\u0590-\u05fea-zA-Z\d\s=\"\'\\\;,\.!?\*&\^\\\|\$\%\^\@\#\!\*\(\)\_]+?)<\/w:t>'
    wrd_trm = re.compile(word_pattern)
    for document in documents:
        result = str(document.read(
            'word/document.xml').decode("utf-8", "strict"))
        lower_case_text = result.lower()
        match_1 = re.findall(par_trm, lower_case_text)
        for m1 in match_1:
            concatenated = ""
            match_2 = re.findall(wrd_trm, m1)
            for i in match_2:
                concatenated += i
            if len(concatenated) != 0:
                word_list.append(concatenated)
    return word_list


def get_input(msg=""):
    return input(msg).lower().strip()


def contains_hebrew_letter(trm):
    heb_trm = re.compile(r"[\u0590-\u05fe]+")
    result = re.findall(heb_trm, trm)
    if len(result):
        return True
    return False


def print_results(results):
    amount = len(results)
    if not amount:
        print(f"Couldn't find")
    else:
        print(
            f"************************ Found the word in {amount} terms ************************")
        for term in results:
            resultant_string = ""
            for word in term.split(" "):
                if contains_hebrew_letter(word):
                    # resultant_string += f"{word[::-1]} "
                    resultant_string += f"{word} "
                else:
                    resultant_string += f"{word} "
            print(resultant_string.strip())


def get_documents_from_path(dictionaries_set):
    documents = []
    print(f"Processing docx files...")
    for dict in dictionaries_set:
        path = extract_os_path_from_normalized_path(dict)
        file = zipfile.ZipFile(path, 'r')
        documents.append(file)
    return documents


def look_for_regex_in_file(str_to_find, word_list):
    results = []
    pattern = r'\b{param}\b'.format(param=str_to_find)
    srch_trm = re.compile(pattern)
    for word in word_list:
        if re.search(srch_trm, word):
            results.append(word)
    return results


def print_underline():
    print(UNDERLINE)


def loop_over_input(word_list):
    print(LOGO_MSG)
    inpt = get_input(WELCOME_MSG)
    while (inpt != 'q'):
        results = []
        if len(inpt):
            results = look_for_regex_in_file(inpt, word_list)
            print_results(results)
        print_underline()
        inpt = get_input()


def close_opened_documents(documents):
    for doc in documents:
        doc.close()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--add', type=str, required=False,
                        help="add file to the list of files to parse")
    return parser.parse_args()


def get_db_file_path(folder_name, file_name):
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    return os.path.join(folder_name, file_name)


def load_docx_file_paths_from_db():
    dictionaries_set = set()
    cur_script_env = os.path.abspath(os.path.dirname(__file__))
    folder_path = os.path.join(cur_script_env, DB_FOLDER_NAME)
    with open(get_db_file_path(folder_path, DB_FILE_NAME)) as file:
        for line in file:
            file_path = line.strip()
            dictionaries_set.add(file_path)
    return dictionaries_set


def handle_add_args(args):
    if args.add:
        attempt_to_add_file_path_to_db(args)
    else:
        print("need to give parameter after usage of -a and --add")


def attempt_to_add_file_path_to_db(args):
    file_to_keep = args.add if args.add else args.a
    file_to_keep = os.path.abspath(file_to_keep)
    if is_wsl_path(file_to_keep):
        pass
    elif is_win_path(file_to_keep):
        wsl_path_from_win_path(file_to_keep)
    else:
        print("Bad path input")
        exit(1)
    if file_to_keep:
        if os.path.exists(file_to_keep):
            path_of_write_file = get_db_file_path(DB_FOLDER_NAME, DB_FILE_NAME)
            if file_to_keep in dictionaries_set:
                print(f"Error: file: {file_to_keep} already in db")
            else:
                with open(path_of_write_file, "a") as db_file:
                    db_file.write(
                        f"{wsl_path_from_win_path(file_to_keep)}\n")
                print(
                    f"Success, updated DB file {path_of_write_file} with: \'{file_to_keep}\' to files database.")
        else:
            print(f"Given file: \'{file_to_keep}\' doesn't exists.")


def handle_args(args):
    handle_add_args(args)  # handle -a --add args


if __name__ == "__main__":
    try:
        dictionaries_set = load_docx_file_paths_from_db()
        if len(sys.argv) > 1:  # in case we run the program with parameters, don't loop over input
            args = parse_arguments()
            handle_args(args)
        else:
            documents = get_documents_from_path(dictionaries_set)
            word_list = preprocess_documents(documents)
            close_opened_documents(documents)
            loop_over_input(word_list)
    except KeyboardInterrupt:
        print("Exiting")
        exit(0)
