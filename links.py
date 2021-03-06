import BaseN, random, os
from pymongo import MongoClient

DIGIT_SET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_.-~'

# get connection string
DB_CONN_STR = os.environ.get('DB_CONN_STR')

# connect to mongo and get collection
dbc = MongoClient(DB_CONN_STR)
link_db = dbc.fastlink
LINKS = link_db.LINKS

# create a new shortlink ID for URI link_str
def new_link(link_str):
    # check if shortlink exists for URI
    link_found = uri_search(link_str)
    print('existing link found: %s' % link_found)
    if link_found is not None:
        return link_found['short_id']
    else:
        nextId = generate_new_id()
        next_link = {
            'short_id': nextId,
            'uri': link_str,
            'clicks': 0
        }

        LINKS.insert_one(next_link)
        return next_link['short_id']

# search mongo collection for id = link_id
def find_link(link_id):
    # if link exists, update click count
    check = LINKS.find_one({'short_id': link_id})
    if check is not None:
        return check
    else:
        return None

def click_link(link_id):
    # if link exists, update click count
    check = LINKS.find_one({'short_id': link_id})
    if check is not None:
        print(LINKS.find_one({'short_id': link_id}))
        LINKS.update_one({'short_id': link_id}, {'$inc': {'clicks': 1}})
        print(LINKS.find_one({'short_id': link_id}))
        return check
    else:
        return None

# search mongo collection for uri = link_uri
def uri_search(link_uri):
    return LINKS.find_one({'uri': link_uri})

# generate random ID, search mongo collection (until a unique ID is found)
def generate_new_id():
    searching = True
    while searching:
        nextIdBase = random.randint(1252332576, 82653950015)
        nextId = BaseN.DecToBaseN(str(nextIdBase), DIGIT_SET)
        if nextId[-1] not in ['.', '-', '_', '~']:
            print('searching for %s' % nextId)
            if LINKS.find_one({'short_id': nextId}) is None:
                searching = False
    return nextId
