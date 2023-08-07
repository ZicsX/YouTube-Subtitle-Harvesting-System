# import nltk
import re
import random
import string

def random_sentence(subtitle):
    subList = [
        substring
        for substring in re.split(r"\s*\.\.\.\s*|\n|\xa0", subtitle)
        if substring
    ]
    return random.choice(subList)

class Tagger:
    def __init__(self, file_path):
        self.tags = set()
        self.load_tags(file_path)

    def load_tags(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                normalized_tag = self.normalize(line.strip())
                self.tags.add(normalized_tag)

    def clean_text(self, text):
        # Remove URLs
        text = re.sub(r'http\S+', '', text)

        # Sanitize hashtags
        text = text.replace("#", "")

        # Remove punctuation except for hyphens and pipes
        allowed = set('-|')
        punctuation = ''.join(ch for ch in string.punctuation if ch not in allowed)
        text = text.translate(str.maketrans('', '', punctuation))
        
        return text

    def normalize(self, text):
        text = self.clean_text(text).lower()
        return text.lower().strip()

    def tag_string(self, input_string):
        tokens = self.normalize(input_string).split()

        matched_tags = [token for token in tokens if token in self.tags]
        return ", ".join(matched_tags)
