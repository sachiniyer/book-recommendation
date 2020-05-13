"""
Assigns tags to books using wikipedia summaries

Sachin Iyer
"""

import numpy as np
import wikipedia, json, csv, sys, codecs, collections, functools

np.set_printoptions(threshold=sys.maxsize)

tags = np.empty(shape = 0)
fiction_books = np.empty(shape = 0)
nonfiction_books = np.empty(shape = 0)
book_tags = np.empty(shape = 0)



tags_file = open("tags.json", "r")
tags_data = tags_file.read()
tags_json = json.loads(tags_data)

tags_subjects = np.array([["Subjects", "INDULGENCES + WORLDS", "MOODS", "MIND + BODY", "IDENTITY", "POLITICS + PHILSOPHIES", "LOVE", "PROFESSIONS"], ["Style", "STYLES ", "MOVEMENTS", "EQUALS"], ["Time", "TIME"], ["Form", "FORM"],
                         ["Ethnicities and Religions", "NATIONALITIES", "RELIGION", "RACE"], ["Place", "COUNTRY", "CITY", "STATE", "REGION"], ["Reception", "RECEPTION"]])


with open('fiction.csv', newline = '\n') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',', quotechar = '\"')
    for row in reader:
        fiction_books = np.append([fiction_books], list([row, ""]))

with open('nonfiction.csv', newline = '\n') as csvfile:
    reader = csv.reader(csvfile, delimiter = ',', quotechar = '\"')
    for row in reader:
        nonfiction_books = np.append([nonfiction_books], list([row, ""]))

def multi_dict(K, type):
    if K == 1:
        return collections.defaultdict(type)
    else:
        return collections.defaultdict(lambda: multi_dict(K-1, type))

def space_tag(x):
    index = 0
    words = []
    i = 0
    index_double = 0
    while i < len(x):
        if x[i] == "\"":
            index_double = i
            i = i + 1
            while x[i] != "\"":
                i = i + 1
            index = i + 1
            words.append(x[index_double:index])
            i = i + 1
        elif x[i] == " ":
            words.append(x[index:i])
            index = i + 1
        i = i + 1
    return(words)

def process_tags(x):
    y = np.array(x[0])
    for z in range(1, len(x)):
        tags_specific = np.empty(shape = 0)
        for i in tags_json[x[0]]:
            try:
                tags_specific = np.append(tags_specific, list([space_tag(i[x[z]]+ " "), ""]))
            except(KeyError):
                continue
        y = np.append([y],list([x[z], [tags_specific]]))
    return(y)

def create_page(x):
    try:
        page = wikipedia.page(x)
        return page
    except:
        try:
            wikipedia.page(x + " (book)")
            return page
        except:
            try:
                wikipedia.page(x + " (novel)")
                return page
            except:
                return 0

def clean_tag(x):
    try:
        x.remove('')
    except ValueError:
        x = x
    try:
        x.remove(' ')
    except ValueError:
        x = x
    return (x)

def compare_tag(page, tags):
    content = page.content.split()
    tag_sep = []
    match = True
    match_num = 0
    tags = clean_tag(tags)
    for tag in tags:
        tag_sep = tag.split()
        for x in range(len(content) - len(tag_sep) - 1):
            for y in range(len(tag_sep)):
                if content[x+y] != tag_sep[y]:
                    match = False
            if match == True:
                match_num = match_num + 1
            match = True
    return(match_num)

def process_text(page):
    list1 = np.empty(shape = 0)
    list2 = np.empty(shape = 0)
    tags_agg = np.empty(shape = 0)
    num = 0
    for x in tags:
        if type(x) is str:
            tags_agg = np.append(tags_agg, x)
        else:
            for y in x:
                for z in y:
                    if z != '':
                        num = compare_tag(page, z)
                        list1 = np.append(list1, list([z, num]))
                        tags_agg = np.append(tags_agg, list1)
                        num = 0
                        list1 = np.empty(shape = 0)
    return tags_agg

def process_book(x):
    page = create_page(x)
    if page == 0:
        return 0
    else:
        return process_text(page)

def check_zero(x):
    if type(x) == str:
        if x == '0':
            return False
    if type(x) == int:
        if x == 0:
            return False
    return True

for x in tags_subjects:
    tags = np.append([tags], list([process_tags(x)]))

for x in range(5):
    if fiction_books[x] != '':
        book_tags = np.append(book_tags, list([fiction_books[x][0], process_book(fiction_books[x][0])]))


book_dict = multi_dict(4, str)

category = ""
subcategory = ""
num = 0

for x in range(len(book_tags)):
    if type(book_tags[x]) == str and check_zero(book_tags[x+1]) and check_zero(book_tags[x]):
        print(book_tags[x])
        for y in range(len(book_tags[x+1])):
            if y != len(book_tags[x+1])-2:
                if type(book_tags[x+1][y]) == str and type(book_tags[x+1][y+1]) == str:
                    category = book_tags[x+1][y]
                elif type(book_tags[x+1][y]) == str:
                    subcategory = book_tags[x+1][y]
            if type(book_tags[x+1][y]) == list:
                num = book_tags[x+1][y+1]
                book_dict[book_tags[x]][category][subcategory][functools.reduce(lambda a,b:a+', '+b, book_tags[x+1][y])] = str(num)

final = json.loads(json.dumps(book_dict))
print(json.dumps(final, indent = 4))
