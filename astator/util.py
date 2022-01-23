import docx

# Reading text file and passing it to template
# Code by: Chinmoy Panda from StackOverflow
def getText(filename):
    doc = docx.Document(filename)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    return '\n'.join(fullText)


# Getting avg rating for script
def average_rating(lst):
    return sum(lst) / len(lst)


# Getting perc of the total votes to pass as width of rating bars.
# Since this function is called only when there are ratings - meaning when 
# whole is at least one, we don't have to worry about 0 division.
def percent(part, whole):
    perc = int(100 * float(part)/float(whole))
    return perc


# Checking if a number submited is between 1 and 5
def check_rating(n):
    if isinstance(n, int) and n >= 1 and n <= 5:
        return True
    else:
        return False