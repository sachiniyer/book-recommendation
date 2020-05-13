"""
Assigns tags to books using wikipedia summaries

Sachin Iyer
"""

import wikipedia
import numpy as np

#read books and tags
b = open("books.txt", "r")
t = open("tags.txt", "r")

#initialize arrays
books = []
tags = []
pages = []
page = ""
books_tags = np.array([""])

#define function to go through text and find tags
def assign_tags(content, title):
    global books_tags
    specific_tags = []
    for x in tags:
        for y in content:
            if x == y:
                specific_tags.append(y)
                break
    books_tags = np.append(books_tags, [str(title), specific_tags])

#add books to array
for x in b:
    books.append(x.strip())

#add tags to array
for x in t:
    tags.append(x.strip())

#create wikipedia pages for each book
for x in books:
    pages.append(wikipedia.page(x))

#call function to assign tags to books
for x in pages:
    page = x.content.split()
    assign_tags(page, x.title)

#print all books and tags
books_tags = np.delete(books_tags, 0, 0)

for x in books_tags:
    if type(x) == list:
        for y in range(len(x) - 1):
            print(x[y] + ", ", end = "")
        print(x[-1])

    else:
        print(x + ":")

#close files
b.close()
t.close()
