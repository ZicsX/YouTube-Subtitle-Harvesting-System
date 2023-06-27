# import nltk
import re
import random

def random_sentence(subtitle):
    subList = [substring for substring in re.split(r"\s*\.\.\.\s*|\n|\xa0", subtitle) if substring]
    return random.choice(subList)
