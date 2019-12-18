import re

EMPTY_REGION = {
    "name": "Other",
    "items": [],
    "description": ""

}
MAIN_DUMP = ""
def get_one_item(title, dump):
    '''
    Parse data and return only one item
    '''
    title = title.replace("(", "\(")
    title = title.replace(")", "\)")
    pattern = r"<page>\s+<title>" + title + r"</title>(?s:.)+?</page>"
    result = re.search(pattern, dump)
    return result.group(0)

def get_dump(path):
    with open(path, 'r') as f:
        return f.read()

def get_first_name_from_double_meaning_word(word):
    try:
        pattern = r"(.+?)\|"
        result = re.search(pattern, word)
        first_part = result.group(1)
        return first_part + "]]"
    except Exception as e:
        return word

def logs(text):
    with open("logs.txt", "a+") as f:
        f.write(text + "\n")