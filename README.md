# marcmatchcheck
Compares MARC records across key fields (ISBN, author, title, edition, publisher, publication date, and physical description) by matching on 001. Requires input of two .mrc files with matching 001s and returns .csv with key fields and similarity score using fuzz.WRatio.
