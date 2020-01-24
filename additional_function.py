import re
from functools import wraps
from time import time
EMPTY_REGION = {
    "name": "Other",
    "items": [],
    "description": ""

}
MAIN_DUMP = ""




def timing(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time()
        result = f(*args, **kw)
        te = time()
        print('func:%r args: %r] took: %2.4f sec' % (f.__name__, kw, te-ts))
        return result
    return wrap

# Too long time for parse should be improve
def get_one_item(title, dump):
    '''
    Parse data and return only one item
    '''
    if "[[" in title and "]]" in title:
        title = title[2:-2]
    title = get_first_name_from_double_meaning_word(title)
    try:
        title = title.replace("(", "\(")
        title = title.replace(")", "\)")
        ts = time()
        pattern = r"<page>\s+<title>" + title + r"</title>(?s:.)+?</page>"
        result = re.search(pattern, dump)
        te = time()
        # print('func:  took: %2.4f sec' % ( te - ts))
        return result.group(0)
    except:
        return ""

def get_dump(path):
    with open(path, 'r') as f:
        return f.read()

def get_first_name_from_double_meaning_word(word):
    try:
        pattern = r"(.+?)(\s+)?\|"
        result = re.search(pattern, word)
        first_part = result.group(1)
        return first_part
    except Exception as e:
        return word


def logs(text):
    with open("logs.txt", "a+") as f:
        f.write(text + "\n")