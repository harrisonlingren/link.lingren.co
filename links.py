import shelve, BaseN, random, pprint

DIGIT_SET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_.-~'

try:
    USED_IDS = shelve.open('USED_IDS.db')
except IOError:
    print('ERROR: Could not read from USED_IDS db')

try:
    LINKS = shelve.open('LINKS.db')
except IOError:
    print('ERROR: Could not read from USED_IDS db')

def new_link(link_str):
    if link_str in LINKS.keys():
        return LINKS[link_str]['ID']

    searching = True
    while searching:
        nextIdBase = random.randint(1252332576, 82653950015)
        nextId = BaseN.DecToBaseN(str(nextIdBase), DIGIT_SET)

        if nextId not in USED_IDS:
            searching = False

    newLink = {
        'ID': nextId,
        'link': link_str,
    }

    USED_IDS[nextId] = link_str
    LINKS[link_str] = newLink

    return newLink['ID']

def get_link(link_id):
    if link_id in USED_IDS.keys():
        return USED_IDS[link_id]
    else:
        return None

def show_links():
    for link in LINKS.items():
        pprint.pprint(link)
