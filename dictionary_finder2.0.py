import platform
import zipfile
import re

UNDERLINE = "_______________________________________________________________"
LOGO_MSG = "****************************************************************************\n\
                   Welcome to Dictionary Finder 2.0                         \n\
****************************************************************************"
WELCOME_MSG = "Enter the phrase you wish to search for in the dictionary. Enter 'q' to exit.\n"
# PATH_TO_DICTIONARIES = "D:\\Projects\\Python\\dictionary_finder\\"
# DICTIONARIES_TO_SEARCH = ['English Dictionary 2.docx'] \

SYSTEM = platform.system()
DICTIONARIES_TO_SEARCH = ["Complete Dictionary.docx", 'English III.docx']

if SYSTEM == 'Windows':
    PATH_TO_DICTIONARIES = "D:\\Google Drive\\Documents\\Linguistics\\"
elif SYSTEM == 'Linux':
    PATH_TO_DICTIONARIES = "/mnt/d/Projects/Python/dictionary_finder/dictionary_finder2.0.py/"
else:
    print(f"This script doesn't support the {SYSTEM} operating system.")
    exit(0)


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


def get_documents_from_path(PATH_TO_DICTIONARIES, DICTIONARIES_TO_SEARCH):
    documents = []
    for dict in DICTIONARIES_TO_SEARCH:
        path = PATH_TO_DICTIONARIES + dict
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


if __name__ == "__main__":
    try:
        documents = get_documents_from_path(
            PATH_TO_DICTIONARIES, DICTIONARIES_TO_SEARCH)
        word_list = preprocess_documents(documents)
        close_opened_documents(documents)
        loop_over_input(word_list)
    except KeyboardInterrupt:
        print("Exiting")
        exit(0)
